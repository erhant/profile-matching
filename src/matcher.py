#import re
from transformers import pipeline
#from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer, util
#import torch
# import tensorflow as tf
from SSIM_PIL import compare_ssim
from PIL import Image
#from skimage.measure import compare_ssim
#import matplotlib.pyplot as plt
#import nltk
#from nltk.util import ngrams
#import numpy as np
import cv2
from pyjarowinkler import distance
from strsimpy.cosine import Cosine

def imageSimilarity(image1_path, image2_path):
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

def textSummarization(text):
    #text:  concatenated posts and tweets as a single string
    summarizer = pipeline("summarization")
    # print("hello how are you")
    str_l = len(text.split(' '))
    min_len =int(str_l* 0.95)
    max_len = str_l
    summary = summarizer(text,max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
    return summary


def textSemantic(text=None): # maybe compare headline with tweets?
    """Conducts semantic analysis on a text
       
    TODO: Returns what?
    """
    classifier = pipeline('sentiment-analysis')
    r_dict = classifier(text)[0]
    return r_dict["label"],r_dict["score"] 


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
    TODO: Google API can be used to obtain coordinates and measure similarity with that too.
    """
    if loc1 == loc2:
        return 1 # matched exatcly
    else:
        return distance.get_jaro_distance(loc1,loc2,winkler=False)


def namedEntityRecogntion(text):
    ner = pipeline("ner")
    output = ner(text)
    
    result = [d["word"] for d in output]
    return result

def cosineSimilarityScore(l1,l2):
    d1 = {k:1 for k in l1}
    d2 = {k:1 for k in l2}
    cosine = Cosine(2)

    score =  cosine.similarity_profiles(d1,d2)
    return score


def getProfileCommonComparisonScore(u1,u2):
    """Compares two profiles with their common features.
    
    The features are: username, biography, location, ner
    Profile image is not done yet.
    """
    score = 0
    
    uname_score  = usernameSimilarityScore(u1["username"],u2["username"])
    loc_score =  0 if u1["location"] == '' or u2["location"] == '' else locationSimilarityScore(u1["location"],u2["location"])
    website_score =  0 if u1["website"] == '' or u2["website"] == '' else usernameSimilarityScore(u1["website"],u2["website"])
    bio_score = 0 if u1["bio"] == '' or u2["bio"] == '' else textSimilarity(u1["bio"],u2["bio"])
    #img_sim_score = imageSimilarity(u1["profileImage"],u2["profileImage"]) # TODO
    #ner_score = cosineSimilarityScore(u1["ner"],u2["ner"]) # TODO: preprocess "ner" for each user and store in the database
    #print(f"uscore={uname_score},loc_score={loc_score},bio_score={bio_score}")

    score = (1.55 * uname_score + 0.65 * loc_score + bio_score + 0.8 * website_score) / 4
    
    return score


class Matcher:
    def __init__(self, mongo):
        self.mongo = mongo # mongo interface to be used by matcher
        
    def findMatchForTwitterUser(self, username, batchSize = 64):
      sourceUser = self.mongo.getTwitterUser(username)
      
      # Search the DB batch by batch
      maxScore = 0
      mostSimilarUser = None
      batchNo = 0
      userCount = self.mongo.getCount(self.mongo.FACEBOOK)
      while batchNo * batchSize < userCount:
        print("Processing [",batchNo * batchSize,"/",userCount,"]")
        users = self.mongo.getManyUsers(batchNo, batchSize, coll=self.mongo.FACEBOOK)
        for targetUser in users:
          score = getProfileCommonComparisonScore(sourceUser,targetUser)
          if score > maxScore:
            print("\tBetter match found with score",score)
            mostSimilarUser = targetUser
            maxScore = score
        batchNo += 1
          
      return (mostSimilarUser, maxScore)
    
    def findMatchForFacebookUser(self, username, batchSize = 64):
      sourceUser = self.mongo.getFacebook(username)
      
      # Search the DB batch by batch
      maxScore = 0
      mostSimilarUser = None
      batchNo = 0
      userCount = self.mongo.getCount(self.mongo.TWITTER)
      while batchNo * batchSize < userCount:
        print("Processing [",batchNo * batchSize,"/",userCount,"]")
        users = self.mongo.getManyUsers(batchNo, batchSize, coll=self.mongo.TWITTER)
        for targetUser in users:
          score = getProfileCommonComparisonScore(sourceUser,targetUser)
          if score > maxScore:
            print("\tBetter match found with score",score)
            mostSimilarUser = targetUser
            maxScore = score
        batchNo += 1
          
      return (mostSimilarUser, maxScore)
    
    # @Mandana (you can rename the function of course)
    def populateNERs(self):
      twitterDocs = self.mongo.getUsersWithoutNER(coll=self.mongo.TWITTER)
      facebooDocs = self.mongo.getUsersWithoutNER(coll=self.mongo.FACEBOOK)
      # For twitter, extract ner from biography
      # For facebook, extract ner from biography+"\n"+education+"\n"+work
      # Update the user docs with the ners, the field ise "ner".
      
      # get ner with: namedEntityRecogntion(texthere)
      
      # thank you!

if __name__ == "__main__":

    u1 = {"username":"waris.gill","location":"Istanbul","ner":["Lahore","Istanbul"],"bio":"I live in lahore."}
    u2 = {"username":"gil.waris","location":"Istanbl","ner":["Lahore","Istanbul","Turkey"],"bio":"My hometown is lahore."}

    score = getProfileCommonComparisonScore(u1,u2)
    print(f"Score={score}")


