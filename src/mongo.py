from sshtunnel import SSHTunnelForwarder
import pymongo
from dateutil.parser import parse as parseDate

# connection script adapted from https://gist.github.com/JinhaiZ/3ad536870b9853dbff11ab4241380c0d

## PARAMS
DEFAULT_MONGO_CREDS = {
  "MONGO_HOST": "209.250.251.192",
  "SSH_USER": "demouser",
  "SSH_PASS" : "thanksgoditsfriday",
  "MONGO_DB": "last-facebook-twitter"
}
FACEBOOK = "Facebook"
TWITTER = "Twitter"

class Mongo:
    def __init__(self, creds = DEFAULT_MONGO_CREDS):
      self.tunnel = None
      self.connection = None
      self.db = None
      self.creds = creds
      self.FACEBOOK = FACEBOOK
      self.TWITTER = TWITTER
    
    def connect(self):
      # define ssh tunnel
      self.tunnel = SSHTunnelForwarder(
        self.creds['MONGO_HOST'],
        ssh_username=self.creds['SSH_USER'],
        ssh_password=self.creds['SSH_PASS'],
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
    
    # Get and prepare a facebook user
    def getFacebookUser(self, username, returnDoc = False):
      doc = self.db[FACEBOOK].find_one({"_id": username})
      user = self.__processFacebookDoc(doc)
      if returnDoc:
        return (user, doc)
      return user
        
    # Get and prepare a twitter user
    def getTwitterUser(self, username, returnDoc = False):
      doc = self.db[TWITTER].find_one({"_id": username})
      user = self.__processTwitterDoc(doc)
      if returnDoc:
        return (user, doc)
      return user
    
    # Updates NER field of a user @Waris
    def updateNERofUser(self, username, ner, coll = FACEBOOK):
      return 1 #TODO TODO
      
    # Count the number of records in a collection
    def getCount(self, coll = FACEBOOK, query = {}):
      return self.db[coll].find(query).count()
    
    # Get a batch of users
    def getManyUsers(self, batchNo, batchSize, coll = FACEBOOK, query = {}, process=True):
      if process:
        if coll == FACEBOOK:
          return list(map(lambda doc: self.__processFacebookDoc(doc), list(self.db[coll].find(query).sort("_id").skip(batchNo * batchSize).limit(batchSize))))
        else:
          return list(map(lambda doc: self.__processTwitterDoc(doc), list(self.db[coll].find(query).sort("_id").skip(batchNo * batchSize).limit(batchSize))))
      else:
        return list(self.db[coll].find(query).sort("_id").skip(batchNo * batchSize).limit(batchSize))
      
    def getAllUsers(self, coll = FACEBOOK):
      '''Returns all users from database.
      
      '''
      if coll == FACEBOOK:
        return list(map(lambda doc: self.__processFacebookDoc(doc), list(self.db[coll].find({}))))
      else:        
        return list(map(lambda doc: self.__processTwitterDoc(doc), list(self.db[coll].find({}))))
      
    
    def getMatchedGroundtruth(self):
      '''Returns matched users from database.
      
      The result is a dictionary with keys twitter and faceook, each having an equal length array where the same index on both arrays correspond to a matching user.
      '''
      # Returns a tuple as (twitterUser, facebookUser)
      print("Getting Twitter users with known matches...")
      twitterUsers = list(map(lambda doc: self.__processTwitterDoc(doc), list(self.db[TWITTER].find({"matched": {"$ne": None}}))))
      print("Getting the corresponding Facebook users...")
      facebookUsers = list(map(lambda tu : self.getFacebookUser(tu['matched']), twitterUsers))
      return {'twitter': twitterUsers, 'facebook': facebookUsers}
    
    def __processFacebookDoc(self, doc):
      '''Converts a mongo document into user dictionary for matcher.
      
      It appends the headline to biography of the user.
      '''
      user = {}
      if doc == None:
        return None
      
      # Commons
      user['username'] = doc['_id']
      user['name'] = doc['name']
      user['location'] = doc['location'] 
      user['website'] = doc['website'] 
      user['bio'] = doc['bio'] + doc['site'] # 'site' is like a short biography
      if doc['photo'] != "" and doc['photo'] != None:
        user['profileImage'] = doc['photo']
      else:
        user['profileImage'] = ""
      try:
        user['matched'] = doc['matched']
      except:
        user['matched'] = None
      user['sourceCollection'] = FACEBOOK
      try:
        user['bornAt'] = parseDate(doc['birthdate'][:-10]) # remove Born and convert to date
      except:
        user['bornAt'] = None
      
      # Specials
      try:
        user['friends'] = list(map(lambda f : f[25:], doc['friends']))
      except:
        user['friends'] = []
      if doc['bg'] != "" and doc['bg'] != None:
        user['backgroundImage'] = doc['bg']
      else:
        user['backgroundImage'] = ""
      user['education'] = ""
      if ('education' in doc and len(doc['education']) > 0):
        user['education'] += doc['education'][0] + "\n"
      if ('education1' in doc and len(doc['education1']) > 0):
        user['education'] += doc['education1'][0] + "\n"
      if ('education2' in doc and len(doc['education2']) > 0):
        user['education'] += doc['education2'][0] + "\n"
      user['education'] = user['education'].strip()
      user['work'] = ""
      if ('work' in doc and len(doc['work']) > 0):
        user['work'] += doc['work'][0] + "\n"
      if ('work1' in doc and len(doc['work1']) > 0):
        user['work'] += doc['work1'][0] + "\n"
      if ('work2' in doc and  len(doc['work2']) > 0):
        user['work'] += doc['work2'][0] + "\n"
      user['work'] = user['work'].strip()
      
      return user
    
    def __processTwitterDoc(self, doc):
      '''Converts a mongo document into user dictionary for matcher.
      
      '''
      user = {}
      if doc == None:
        return None
      
      # Commons
      user['username'] = doc['_id']
      user['name'] = doc['name']
      user['location'] = doc['location'] 
      user['website'] = doc['site'] 
      user['bio'] = doc['bio']
      if doc['photo'] != "" and doc['photo'] != None:
        user['profileImage'] = doc['photo']
      else:
        user['profileImage'] = ""
      try:
        user['matched'] = doc['matched']
      except:
        user['matched'] = None
      user['sourceCollection'] = TWITTER
      try:
        user['bornAt'] = parseDate(doc['born'][5:]) # removes "Born " string
      except:
        user['bornAt'] = None
          
      # Specials
      user['username'] = doc['_id']
      user['tweets'] = doc['tweets']
      user['followers'] = doc['followerids']
      if doc['joined'] != "":
        user['joinedAt'] = parseDate(doc['joined'][7:])
      else:
        user['joinedAt'] = None
        
      return user
    
    # Just for testing purposes
    def __listCollections(self):
      print("Listing collections:")
      for coll in self.db.list_collection_names():
        print("\t",coll)
            
    # Get few records for testing
    def __getTopN(self, n, coll = FACEBOOK):
      return list(self.db[coll].find().limit(n))
    
    # Get raw document data of a user
    def __getUser(self, username, coll = FACEBOOK):
      return self.db[coll].find_one({"_id": username})
      