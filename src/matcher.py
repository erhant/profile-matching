#from mongo import Mongo
from dateutil.parser import parse as parseDate
import requests

class Matcher:
    def __init__(self, db):
        self.db = db # connection to be used by matcher
        
    # Get raw document data of a user
    def getUser(self, username, coll = 'facebook'):
        return self.db[coll].find_one({"_id": username})
        
    # Get few records for testing
    def getTopN(self, n, coll = 'facebook'):
        ans = []
        for data in self.db[coll].find().limit(n):
            ans.append(data)
        return ans
    
    # Get and prepare a facebook user
    def getFacebookUser(self, username):
        doc = self.db['facebook'].find_one({"_id": username})
        user = {}
        
        # Commons
        user['username'] = doc['_id']
        user['name'] = doc['name']
        user['locaton'] = doc['location']
        user['website'] = doc['website']
        user['bio'] = doc['bio']
        if doc['photo'] != "":
            user['profileImage'] = requests.get(doc['photo'])
        else:
            user['profileImage'] = None
        
        # Specials
        user['headline'] = doc['site'] # todo: what is this?
        if doc['bg'] != "":
            user['backgroundImage'] = requests.get(doc['bg'])
        else:
            user['backgroundImage'] = None
        user['educations'] = [doc['education'],doc['education1'],doc['education2']] # todo what is this
        user['works'] = [doc['work'],doc['work1'],doc['work2']] # todo what is this
        return (user, doc)
        
    # Get and prepare a twitter user
    def getTwitterUser(self, username):
        doc = self.db['twitter'].find_one({"_id": username})
        user = {}
        
        # Commons
        user['username'] = doc['_id']
        user['name'] = doc['name']
        user['locaton'] = doc['location']
        user['website'] = doc['site'] # can perhaps crawl there and check for facebook / twitter links?
        user['bio'] = doc['bio']
        if doc['photo'] != "":
            user['profileImage'] = requests.get(doc['photo'])
        else:
            user['profileImage'] = None
            
        # Specials
        user['tweets'] = doc['tweets']
        user['followers'] = [] # todo @Mandana
        user['following'] = [] #todo @Mandana
        user['handle'] = doc['handle']
        if doc['born'] != "":
            #user['born'] = parseDate(doc['born'][5:]) # 5: to remove "Born "
            user['born'] = parseDate("1991")
        else:
            user['born'] = None
        if doc['matched'] == None:
            user['matched'] = False
        else:
            user['matched'] = True
            
        return (user, doc) # doc is returned for debug purposes
    