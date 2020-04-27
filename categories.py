import json
from logger import log
from os import path

dataStore = "data/categories.json"

class Categories():
    status = "Empty"
    data = dict()

    def getStatus(self):
        return self.status

    def save(self):
        with open( dataStore, 'w' ) as outfile:
            jstr = json.dumps( self.data )
            outfile.write(jstr)

    def load(self):
        if not path.isfile(dataStore):
            self.data = {}
            self.status = "Empty"
            return
        try:
            with open(dataStore) as json_file:
                self.data = json.load( json_file )
            log( self.data )

            self.status = "Ready"
        except Exception as e:
            print( e )
            self.status = "Read Error"




