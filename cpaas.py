from setupform import SetupForm
from logger import log

from cpaassdk import Client
from flask import request
from game import Chategory
import sys
import weakref

simulation = True

class Cpaas:
    status = "Not Ready"
    projectTN = "unk"

    def __init__(self):
        log('cpaas init')
        # Initialize
        self.game = Chategory(self)
        self.status = "Init"
        self.register()

    def register(self):
        log('cpaas register')

        setup = SetupForm()
        setup.loadSetup()
        if setup.data['project_TN'] is None:
            log( "no setup data yet")
            return

        try:
            self.client = Client({
                'client_id': setup.private_key.data,
                'client_secret': setup.client_secret.data,
                'base_url': setup.apim_url.data
            })
            log('type of Client ', type(self.client))
            log(self.client)

            self.projectTN = setup.project_TN.data
            response = self.client.conversation.subscribe({
                'webhook_url': setup.public_url.data + '/inbound-sms/webhook',
                'type': 'sms',
                'destination_address': self.projectTN
            })
            log(response)
            self.status = "Ready"
        except Exception as e:
            print(e)
            self.status = "Register Error"


    def getStatus(self):
        return self.status

    def sendMsg(self, to, msg):
        log('sending msg: ' + msg + ' to ' + to)
        if simulation:
            return
        response = self.client.conversation.create_message(
            dict(type='sms', destination_address=to, sender_address=self.projectTN, message=msg))
        log(response)

    # def determinReply(self, msg):
    #     return "OK"

    def post(self):
        log("post");
        sys.stdout.flush()
        log(request.json)
        try:
            inboundNotification = request.json['inboundSMSMessageNotification']

            if inboundNotification is not None:
                parsed_response = inboundNotification['inboundSMSMessage']

                log(parsed_response)
                plist, reply = self.game.command(parsed_response['senderAddress'], parsed_response['message'])
                for tn in plist:
                    self.sendMsg( tn, reply)
                return '{"success":"true"}'
        except Exception as e:
            print(e)
        return '{"success":"false"}'


