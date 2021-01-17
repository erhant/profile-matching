from sklearn import datasets
from transformers import pipeline
from mongo import Mongo
from sentence_transformers import SentenceTransformer, util
from SSIM_PIL import compare_ssim
from PIL import Image
import numpy as np
import pandas as pd
import random
import cv2
from pyjarowinkler import distance
from strsimpy.cosine import Cosine
from ux import outputHTML
from ml import Classifier

# Not used because facebook URLs are expired.
def __imageSimilarity(image1_path, image2_path):
    """Compares two images using SSIM.
    
    The images must be JPG (TODO: Improve this to work with any of them). 
    """
    
    Image.open(image1_path).resize((224,224)).save(image1_path)
    Image.open(image2_path).resize((224,224)).save(image2_path)

    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    
    # convert the images to grayscale
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    ssim_score = compare_ssim(image1,image2)  

    return ssim_score

# Not used by our work.
def __textSummarization(text):
    #text:  concatenated posts and tweets as a single string
    summarizer = pipeline("summarization")
    # print("hello how are you")
    str_l = len(text.split(' '))
    min_len =int(str_l* 0.95)
    max_len = str_l
    summary = summarizer(text,max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
    return summary

# Not used by our work.
def __textSemantic(text):
    classifier = pipeline('sentiment-analysis')
    r_dict = classifier(text)[0]
    return r_dict["label"],r_dict["score"] 

# Not used by our work. 
def __namedEntityRecogntion(text):
    ner = pipeline("ner")
    output = ner(text)
    
    result = [d["word"] for d in output]
    return result
  
def textSimilarity(text1, text2): # get the similarity score.
    """Compare two texts using BERT model. 
    
    Returns the Cosine Similarity of the embeddings obtained by BERT.
    """
    
    model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
    embeddings1 = model.encode([text1], convert_to_tensor=True)
    embeddings2 = model.encode([text2], convert_to_tensor=True)

    #Compute cosine-similarits
    cosine_scores = util.pytorch_cos_sim(embeddings1,embeddings2)
    # cosine_scores
    return cosine_scores[0].item()
  
def usernameSimilarityScore(uname1, uname2):
    """Compare usernames using Jaro distance.
       
    Returns a score between 0 and 1, where 1 means exact match.
    """
    if uname1 == uname2:
        return 1 # matched exatcly
    else:
        return distance.get_jaro_distance(uname1,uname2,winkler=False)

def locationSimilarityScore(loc1, loc2):
    """Compare location texts using Jaro distance.
       
    Returns a score between 0 and 1, where 1 means exact match.
    """
    if loc1 == loc2:
        return 1 # matched exatcly
    else:
        return distance.get_jaro_distance(loc1,loc2,winkler=False)

def cosineSimilarityScore(l1,l2):
    d1 = {k:1 for k in l1}
    d2 = {k:1 for k in l2}
    cosine = Cosine(2)

    score =  cosine.similarity_profiles(d1,d2)
    return score


def getProfileCommonComparisonScore(u1,u2):
    
    weights = {
      'username': 0.85,
      'name': 0.8,
      'location': 0.65,
      'website':  0.4,
      'bio': 0.65,
      'birthday': 0.4
    }
    
    similarities = {
      'username': usernameSimilarityScore(u1["username"],u2["username"]),
      'name':  0 if u1["name"] == '' or u2["name"] == '' else usernameSimilarityScore(u1["name"],u2["name"]),
      'location':  0 if u1["location"] == '' or u2["location"] == '' else locationSimilarityScore(u1["location"],u2["location"]),
      'website':  0 if u1["website"] == '' or u2["website"] == '' else usernameSimilarityScore(u1["website"],u2["website"]),
      'bio':  0 if u1["bio"] == '' or u2["bio"] == '' else textSimilarity(u1["bio"],u2["bio"]),
      'birthday': 0 if u1["bornAt"] == '' or u2["bornAt"] == '' else (1 if u1['bornAt'] == u2['bornAt'] else 0)
    }
    
    totalScore = sum([similarities[f]*weights[f] for f in similarities]) / sum([weights[f] for f in similarities])
      
    return totalScore, similarities

def trainModel(ground_truth, save_dataset_csv=True, use_existing=True):
      def makePair(f_user, t_user):
        _, d = getProfileCommonComparisonScore(f_user,t_user)
        d["fb_id"] = f_user["username"]
        d["tw_id"] = t_user["username"]
        d["fb_match"] = f_user["matched"]
        d["tw_match"] = t_user["matched"]
        d["Label"] = int(f_user["username"] == t_user["matched"]) # labels are 1 or 0
        return d

      def prepareDatset(fb_users, twitter_users, num_random_samples=6):
        li = []
        num_users = min(len(fb_users),len(twitter_users))
        for i in range(num_users):
          # 1 matching pair
          f_user = fb_users[i]
          t_user = twitter_users[i]
          assert t_user["username"] == f_user["matched"]
          
          # num_random_samples non-matching pairs
          randomlist = random.sample(range(0, len(fb_users)), num_random_samples)
          randomlist.append(i)
          randomlist =  list(set(randomlist)) # avoid duplicates
          li += [makePair(fb_users[i],twitter_users[j]) for j in randomlist]
          
          if i % int(num_users / 10) == 0:
            print("Processed [",i,"/",num_users,"]")
          
        return li
    
      ####
      print("Preparing dataset.")
      if use_existing:
        df = pd.read_csv("dataset.csv") # dataset.csv
      else:
        d_set = prepareDatset(fb_users=ground_truth["facebook"], twitter_users=ground_truth["twitter"])
        df = pd.DataFrame.from_records(d_set)
        print("Created dataset:",df.shape)
        if save_dataset_csv:
          print("Saving csv...")
          df.to_csv("dataset.csv",index=False)
      featureNames = ['username', 'name', 'location', 'website', 'bio', 'birthday']
      labelName = 'Label'
      classifier = Classifier(df, featureNames, labelName)
      model = classifier.makeModel()
      return model
    
class Matcher:
    def __init__(self, mongo):
        self.mongo = mongo # mongo interface to be used by matcher
        self.Twitter = mongo.getAllUsers(coll=mongo.TWITTER) # twitter data
        self.Facebook = mongo.getAllUsers(coll=mongo.FACEBOOK) # facebook data
        self.model = trainModel(mongo.getMatchedGroundtruth()) # ML model for direct matching
        
    def findMatchForTwitterUser(self, username, useML=False):
      print("Finding a direct match for Twitter user:",username)
      sourceUser = self.mongo.getTwitterUser(username)
      
      maxScore = 0
      maxSims = {}
      targetUser = None
      count = 1
      for candidate in self.Facebook:        
        if useML:
          _, sims = getProfileCommonComparisonScore(sourceUser,candidate)
          f = []
          for s in sims:
            f.append(sims[s])
          f = np.array(f).reshape((1, -1))
          pred = self.model.predict_proba(f)
          pred = pred[0]
          if pred[1] > pred[0]:
            if pred[1] > maxScore:              
              print("\tBetter match found with probability",pred[1])
              targetUser = candidate
              maxScore = pred[1]
              maxSims = sims
        else:
          score, sims = getProfileCommonComparisonScore(sourceUser,candidate)
          if score > maxScore:
            print("\tBetter match found with score",score)
            targetUser = candidate
            maxScore = score
            maxSims = sims
        if count % 75 == 0:
          print("\tProcessed [",count,",",len(self.Twitter),"]")
        count += 1
        
      if targetUser == None:
        print("Could not match this user!")
        return {}
      else:
        print("Match found!")
        outputHTML(sourceUser, targetUser, maxScore, maxSims, title = "Direct Match" + (" with ML" if useML else ""))
        return {'facebookUser': targetUser, 'twitterUser': sourceUser, 'score': maxScore, 'similarities': maxSims}
    
    def findMatchForFacebookUser(self, username, useML=False):
      print("Finding a direct match for Facebook user:",username)
      sourceUser = self.mongo.getFacebookUser(username)
      
      maxScore = 0
      maxSims = {}
      targetUser = None
      count = 1
      for candidate in self.Twitter:
        if useML:
          _, sims = getProfileCommonComparisonScore(sourceUser,candidate)
          f = []
          for s in sims:
            f.append(sims[s])
          f = np.array(f).reshape((1, -1))
          pred = self.model.predict_proba(f)
          pred = pred[0]
          if pred[1] > pred[0]:
            if pred[1] > maxScore:              
              print("\tBetter match found with probability",pred[1])
              targetUser = candidate
              maxScore = pred[1]
              maxSims = sims
        else:
          score, sims = getProfileCommonComparisonScore(sourceUser,candidate)
          if score > maxScore:
            print("\tBetter match found with score",score)
            targetUser = candidate
            maxScore = score
            maxSims = sims
        if count % 75 == 0:
          print("\tProcessed [",count,",",len(self.Twitter),"]")
        count += 1
        
      if targetUser == None:
        print("Could not match this user!")
        return {}
      else:
        print("Match found!")
        outputHTML(targetUser, sourceUser, maxScore, maxSims, title = "Direct Match" + (" with ML" if useML else ""))
        return {'facebookUser': sourceUser, 'twitterUser': targetUser, 'score': maxScore, 'similarities': maxSims}
    
    
    def findIndirectMatchForTwitterUser(self, username, useML=False):
      print("Finding an indirect match for Twitter user:",username)
      sourceUser = self.mongo.getTwitterUser(username)
      
      # Get friends
      followers = [u for u in self.Twitter if u['username'] in sourceUser['followers']]
      if len(followers) == 0:
        print("No followers of this profile is present in DB.")
        return {}
      
      # Find direct matches of the followers
      print("Found",len(followers),"followers in DB. Finding their direct matches...")
      candidateMatches = [self.findMatchForTwitterUser(f, useML=useML) for f in followers]
      candidateMatches = [c['facebookUser'] for c in candidateMatches]
      
      # Find common friends on all matched facebook profiles
      candidates = {}
      for facebookFriendCandidate in candidateMatches:
        for f in facebookFriendCandidate['friends']:
          if f in candidates:
            candidates[f] += 1
          else:
            candidates[f] = 1
            
      # Find the "most common" common friend
      maxCandidate = 0
      targetUsername = None
      for c in candidates:
        if candidates[c] > maxCandidate:
          maxCandidate = candidates[c]
          targetUsername = c
          
      if targetUsername == None:
        print("Could not match this user!")
        return {}
      else:
        print("Match found!")
        # Retrieve the target
        mostSimilarUser = self.mongo.getFacebookUser(targetUsername)        
        # Also calculate their similarity
        score, sims = getProfileCommonComparisonScore(sourceUser, mostSimilarUser, weighted=(not useML))        
        outputHTML(sourceUser, mostSimilarUser, score, sims, title = "Indirect Match" + (" with ML" if useML else ""))
        return {'facebookUser': mostSimilarUser, 'twitterUser': sourceUser, 'score': score, 'similarities': sims}
    
    def findIndirectMatchForFacebookUser(self, username, useML=False):    
      print("Finding an indirect match for Facebook user:",username)
      sourceUser = self.mongo.getFacebookUser(username)
      
      # Get friends
      friends = [u for u in self.Facebook if u['username'] in sourceUser['friends']]
      if len(friends) == 0:
        print("No friends of this profile is present in DB.")
        return {}
      
      # Find direct matches of the friends
      print("Found",len(friends),"friends in DB. Finding their direct matches...")
      candidateMatches = [self.findMatchForFacebookUser(f, useML=useML) for f in friends]
      candidateMatches = [c['twitterUser'] for c in candidateMatches]
      
      # Find common followers on matched twitter profiles
      candidates = {}
      for twitterFollowerCandidate in candidateMatches:
        for f in twitterFollowerCandidate['followers']:
          if f in candidates:
            candidates[f] += 1
          else:
            candidates[f] = 1
            
      # Find the "most common" common follower
      maxCandidate = 0
      targetUsername = None
      for c in candidates:
        if candidates[c] > maxCandidate:
          maxCandidate = candidates[c]
          targetUsername = c
          
      if targetUsername == None:
        print("Could not match this user!")
        return {}
      else:
        print("Match found!")
        # Retrieve the target
        mostSimilarUser = self.mongo.getTwitterUser(targetUsername)        
        # Also calculate their similarity
        score, sims = getProfileCommonComparisonScore(sourceUser, mostSimilarUser, weighted=(not useML))        
        outputHTML(mostSimilarUser, sourceUser, score, sims, title = "Indirect Match" + (" with ML" if useML else ""))
        return {'facebookUser': sourceUser, 'twitterUser': mostSimilarUser, 'score': score, 'similarities': sims}    
      
if __name__ == "__main__":
  print("main")












