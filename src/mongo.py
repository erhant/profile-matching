from sshtunnel import SSHTunnelForwarder
import pymongo
from dateutil.parser import parse as parseDate
import requests
import re

# adapted from https://gist.github.com/JinhaiZ/3ad536870b9853dbff11ab4241380c0d

## PARAMS
defaultCreds = {
    "MONGO_HOST": "209.250.251.192",
    "MONGO_USER": "root",
    "MONGO_PASS": "PASSWORD",
    "PKEY_PATH": "C:/Users/ASUS/.ssh/id_rsa",
    "PKEY_PASS" : "",
    "MONGO_DB": "new-facebook-twitter"
}
FACEBOOK = "Facebook"
TWITTER = "Twitter"

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
            
    # Get few records for testing
    def getTopN(self, n, coll = FACEBOOK):
        ans = []
        for data in self.db[coll].find().limit(n):
            ans.append(data)
        return ans
    
    # Get and prepare a facebook user
    def getFacebookUser(self, username):
        doc = self.db[FACEBOOK].find_one({"_id": username})
        user = {}
        
        # Commons
        user['username'] = doc['_id']
        user['name'] = doc['name']
        user['locaton'] = doc['location']
        user['website'] = doc['website']
        user['bio'] = doc['bio']
        if doc['photo'] != "":
            user['profileImage'] = requests.get(doc['photo']) # todo process image
        else:
            user['profileImage'] = None
        user['matchedTo'] = doc['matched']
        user['sourceCollection'] = FACEBOOK
        
        # Specials
        user['headline'] = doc['site']
        if doc['bg'] != "":
            user['backgroundImage'] = requests.get(doc['bg'])
        else:
            user['backgroundImage'] = None
        user['education'] = ""
        if (len(doc['education']) > 0):
            user['education'] += doc['education'][0] + "\n"
        if (len(doc['education1']) > 0):
            user['education'] += doc['education1'][0] + "\n"
        if (len(doc['education2']) > 0):
            user['education'] += doc['education2'][0] + "\n"
        user['education'] = user['education'].strip()
        user['work'] = ""
        if (len(doc['work']) > 0):
            user['work'] += doc['work'][0] + "\n"
        if (len(doc['work1']) > 0):
            user['work'] += doc['work1'][0] + "\n"
        if (len(doc['work2']) > 0):
            user['work'] += doc['work2'][0] + "\n"
        user['work'] = user['work'].strip()
        return (user, doc)
        
    # Get and prepare a twitter user
    def getTwitterUser(self, username):
        doc = self.db[TWITTER].find_one({"_id": username})
        user = {}
        
        # Commons
        user['username'] = doc['_id']
        user['name'] = doc['name']
        user['locaton'] = doc['location']
        user['website'] = doc['site'] # can perhaps crawl there and check for facebook / twitter links?
        user['bio'] = doc['bio']
        if doc['photo'] != "":
            user['profileImage'] = requests.get(doc['photo']) # todo process image
        else:
            user['profileImage'] = None
        user['matchedTo'] = doc['matched']
        user['sourceCollection'] = TWITTER
        
        # Specials
        user['username'] = doc['_id']
        user['tweets'] = doc['tweets']
        user['followers'] = [] # todo @Mandana
        user['following'] = [] #todo @Mandana
        #user['handle'] = doc['handle'] # Redundant
        if doc['joined'] != "":
            user['joinedAt'] = parseDate(doc['joined'][7:]) # todo: remove Joined and convert to date
        else:
            user['joinedAt'] = None
        if doc['born'] != "":
            user['bornAt'] = parseDate(doc['born'][5:]) # todo: remove Born and convert to date
        else:
            user['bornAt'] = None
        
        return (user, doc) # doc is returned for debug purposes
    
    # Get raw document data of a user
    def getUser(self, username, coll = FACEBOOK):
        return self.db[coll].find_one({"_id": username})
    
    def find(self, query = {}, coll = FACEBOOK):
        return self.db[coll].find(query)
    
    