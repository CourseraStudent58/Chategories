from logger import log, error
from categories import Categories
from alphabet import Alphabet

from random import seed, randint
import re

seed()

class Round():
    def __init__(self):
        self.categories = Categories()
        self.categories.load()
        self.alphabet = Alphabet()
        self.alphabet.load()
        self.responses = []
        self.nextRound()


    def allResponses(self):
        return [d['response'] for d in self.responses]

    def getResponse(self, ptn):
        log( 'getResponse for ' + ptn )
        try:
            pr = [d for d in self.responses if d['tn'] == ptn]
            return pr[0]
        except Exception as e:
            return { 'tn': ptn, 'valid': False, 'response': 'UNK' }

    def nextRound(self):
        self.cat_index = randint( 0, len(self.categories.data)-1)
        log( self.cat_index)
        self.alpha_index = randint( 0, len(self.alphabet.data)-1)
        log( self.alpha_index )
        self.responses = []

    def describe(self):
        alpha = self.alphabet.data[self.alpha_index]
        return  self.categories.data[self.cat_index]['category'] + " that " + alpha['position'].lower() + " " + alpha['letter']

round = Round()


def usage(players, tn, args):
    return [tn], "Usage: \nTo join the current game\njoin: YourName\n\nTo start the game once people have joined\nnew:\n\nTo reset scores for all players to 0\nreset:\n\nTo see this help\nhelp:\n\nOtherwise, just type your answer"

def validate( args ):
    r = True
    alpha = round.alphabet.data[round.alpha_index]
    v = args[0]
    if alpha['position'] == 'Begins with':
        r = v.lower().startswith( alpha['letter'].lower() )
    elif alpha['position']  == 'Ends with':
        r = v.lower().endswith( alpha['letter'].lower() )
    return r

def guess(players, tn, args):
    v = validate(args)

    round.responses.append( { 'tn': tn, 'valid': v, 'response': args[0] })

    # the end of the round occurs when # responses equals # players
    # in which case we need to score the round
    if len( round.responses) >=  players.numPlayers() :
        # make a list of the responses
        allresp = [d['response'] for d in round.responses ]
        tnlist = players.allPlayerTNs()
        answers = ""
        try:
            for p in players.getPlayers():
                pr = round.getResponse(p.tn)
                c = allresp.count( pr['response'])
                if pr['valid'] is False:
                    p.increment(-1)
                    answers +=  'Invalid response ' + pr['response'] + ' from ' + p.name + '\n'
                elif c == 1:
                    p.increment(1)
                    answers += 'Unique response ' + pr['response'] + ' from ' + p.name + '\n'
                else:
                    answers += 'Duplicate response ' + pr['response'] + ' from ' + p.name + '\n'
        except Exception as e:
            log( e )
            return tnlist, "Ugh, Scoring Error"
        round.nextRound()

        return tnlist, answers + players.currentScore() + "\n\nNext category!\n" + round.describe()
    return [tn], "Noted"

def join(players, tn, args):
    log("join")
    try:
        p = Player(tn, args[1])
        log(p)
        players.append(p)
        log(players)
        tnlist = players.allPlayerTNs()
        return tnlist, p.name + " joined"
    except Exception as e:
        error("join", e)
        return [tn], "We had a join problem"

def drop(players, tn, args):
    log("drop")
    try:
        p = players.remove(tn)
        log(players)
        tnlist = players.allPlayerTNs()
        return tnlist, p.name + " left"
    except Exception as e:
        error("join", e)
        return [tn], "We had a drop problem"


def reset(players, tn, args):
    log("reset")
    plist = players.allPlayerTNs()
    players.reset()
    round.responses = {}
    round.nextRound()
    return plist, "New game! " + round.describe()






commands = {'help': usage,
            'join': join,
            'new': reset,
            'reset': reset,
            'drop': drop
            }


class Player:

    def __init__(self, tn, name):
        self.tn = tn
        self.name = name
        self.score = 0

    def reset(self):
        self.score = 0

    def increment(self, amt):
        self.score += amt

class Players():
    def __init__(self):
        self.players = []

    def numPlayers(self):
        return len( self.players )

    def allPlayerTNs(self):
        tnlist = []
        for p in self.players:
            tnlist.append( p.tn )
        return tnlist

    def append(self, p):
        return self.players.append(p)

    def remove(self, tn):
        for p in self.players:
            if p.tn == tn:
                self.players.remove(p)
                return p
        return Player(tn, "Unknown")

    def reset(self):
        for p in self.players:
            p.reset()

    def getPlayers(self):
        return self.players

    def currentScore(self):
        res = "Current Score: "
        sep = ""
        for p in self.players:
            res += sep + p.name + " " + str(p.score)
            sep = ", "
        return res

class Chategory(object):

    def __init__(self, parent):
        self.players = Players()
        self.parent = parent

    def allPlayerTNs(self):
        tnlist = []
        for p in self.players:
            tnlist.append( p.tn )
        return tnlist

    def command(self, tn, msg):
        log('command')
        # lookup first arg in the msg, and map it to a function
        words = msg.split(':')
        func = commands.get(words[0].lower(), guess)
        log(func)
        # remove all special chars from words before invoking func
        fargs=[]
        for w in words:
            fargs.append(re.sub( '[^A-Za-z0-9 ]+', '', w ))
        plist, result = func(self.players, tn, fargs )
        log(result)
        return plist, result

    def sendAll(self, msg ):
        for p in self.players:
            self.parent.sendMsg( p.tn, msg )