import json
from logger import log

dataStore = "data/alphabet.json"

class Alphabet():
    status = "Empty"
    data = dict()

    def getStatus(self):
        return self.status

    def save(self):
        with open( dataStore, 'w' ) as outfile:
            jstr = json.dumps( self.data )
            outfile.write(jstr)

    def load(self):
        try:
            with open(dataStore) as json_file:
                self.data = json.load( json_file )
            log( self.data )

            self.status = "Ready"
        except Exception as e:
            print( e )
            self.status = "Read Error"




