from sshtunnel import SSHTunnelForwarder
import pymongo

# adapted from https://gist.github.com/JinhaiZ/3ad536870b9853dbff11ab4241380c0d

## PARAMS
defaultCreds = {
    "MONGO_HOST": "209.250.251.192",
    "MONGO_USER": "root",
    "MONGO_PASS": "PASSWORD",
    "PKEY_PATH": "C:/Users/ASUS/.ssh/id_rsa",
    "PKEY_PASS" : "",
    "MONGO_DB": "facebook-twitter"
}


class Mongo:
    def __init__(self, creds = defaultCreds):
        self.tunnel = None
        self.connection = None
        self.db = None
        self.creds = creds
    
    def connect(self):
        # define ssh tunnel
        self.tunnel = SSHTunnelForwarder(
            self.creds['MONGO_HOST'],
            ssh_username=self.creds['MONGO_USER'],
            ssh_pkey=self.creds['PKEY_PATH'],
            ssh_private_key_password=self.creds['PKEY_PASS'],
            remote_bind_address=('127.0.0.1', 27017)
        )
    
        # start ssh tunnel first
        self.tunnel.start()
        # start connection next
        self.connection = pymongo.MongoClient('127.0.0.1', self.tunnel.local_bind_port) # 2nd param is important 
        self.db = self.connection[self.creds['MONGO_DB']]
        print("Connected to mongo! Dont forget to close it when you are done :)")
        
    def terminate(self):
        # close connection first
        self.connection.close()
        # close ssh tunnel next
        self.tunnel.stop()
        print("bye bye..")
     
    # Just for testing purposes
    def listCollections(self):
        print("Listing collections:")
        for coll in self.db.list_collection_names():
            print("\t",coll)