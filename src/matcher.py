#%%
import re
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer, util
import torch
# import tensorflow as tf
from SSIM_PIL import compare_ssim
from PIL import Image
from skimage.measure import compare_ssim
# import matplotlib.pyplot as plt
import nltk
from nltk.util import ngrams

import numpy as np
import cv2
from pyjarowinkler import distance

from strsimpy.cosine import Cosine




def imageSimilarity(image1_path, image2_path): # compare profile images
    # im1 = None
    # im2 = None

    # # if image_path.split(".")[-1]=="jpg":
    # #     tf.io.decode_j
    # print(image1_path, image2_path)
    # im1 = tf.io.decode_jpeg(image1_path)
    # im2 = tf.io.decode_jpeg(image2_path)
    # im1 = tf.image.convert_image_dtype(im1, tf.float32)
    # im2 = tf.image.convert_image_dtype(im2, tf.float32)
    # ssim2 = tf.image.ssim(im1, im2, max_val=1.0, filter_size=11,
    #                       filter_sigma=1.5, k1=0.01, k2=0.03)

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
    # tokenizer = AutoTokenizer.from_pretrained("bert-base-cased-finetuned-mrpc")
    # model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased-finetuned-mrpc")
    # classes = ["not paraphrase", "is paraphrase"]
    # sequence_0 = "The company HuggingFace is based in New York City"
    # sequence_1 = "Apples are especially bad for your health"
    # sequence_2 = "HuggingFace's headquarters are situated in Manhattan"

    # paraphrase = tokenizer(sequence_0, sequence_2, return_tensors="pt")
    # not_paraphrase = tokenizer(sequence_0, sequence_1, return_tensors="pt")

    # paraphrase_classification_logits = model(**paraphrase).logits
    # not_paraphrase_classification_logits = model(**not_paraphrase).logits

    # paraphrase_results = torch.softmax(paraphrase_classification_logits, dim=1).tolist()[0]
    # not_paraphrase_results = torch.softmax(not_paraphrase_classification_logits, dim=1).tolist()[0]

    # # Should be paraphrase
    # for i in range(len(classes)):
    #     print(f"{classes[i]}: {int(round(paraphrase_results[i] * 100))}%")


    # # Should not be paraphrase
    # for i in range(len(classes)):
    #     print(f"{classes[i]}: {int(round(not_paraphrase_results[i] * 100))}%")
    
    
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
    classifier = pipeline('sentiment-analysis')
    r_dict = classifier(text)[0]
    return r_dict["label"],r_dict["score"] 


def usernameSimilarityScore(uname1, uname2):
    """
        Return score between 0 and 1. 
    """
 
    # score = nltk.edit_distance(uname1, uname2,transpositions=True)
    # score = 1-nltk.jaccard_distance(set(ngrams('waris.gill', 2)), set(ngrams('gill.waris', 2)))
    
    score = distance.get_jaro_distance(uname1,uname2,winkler=False)
    
    return score

def locationSimilarityScore(l1, l2):

    if l1 == l2:
        return 1 # matched exatcly
    else:
        return usernameSimilarityScore(l1,l2) # or return 0

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


def getProfileComparisonScore(u1,u2):
    score = 0
    uname_score  = usernameSimilarityScore(u1["username"],u2["username"])
    loc_socre = locationSimilarityScore(u1["location"],u2["location"])
    img_sim_score = imageSimilarity(u1["image"],u2["image"])
    ner_score = cosineSimilarityScore(u1["ner"],u2["ner"]) # preprocess "ner" for each user and store in the database
    bio_score = textSimilarity(u1["bio"],u2["bio"])

    print(f"uscore={uname_score},lscore={loc_socre},img_score={img_sim_score},ner_score={ner_score},bio_score={bio_score}")

    score = uname_score + loc_socre+ img_sim_score + ner_score + bio_score
    score /= len(u1.keys()) # normalizing the score between 0 and 1

    return score

    
def findNaiveSimilar():
    return 1 # todo

class Matcher:
    def __init__(self, db):
        self.db = db # connection to be used by matcher
        
    def findMatchForTwitter(twitterUser):
        return 1 # todo
    
    def findMatchForFacebook(facebookUser):
        return 1 # todo


if __name__ == "__main__":

    u1 = {"username":"waris.gill","location":"Istanbul","image":"./images/i1.jpg","ner":["Lahore","Istanbul"],"bio":"I live in lahore."}
    u2 = {"username":"gil.waris","location":"Istanbl","image":"./images/i2.jpg","ner":["Lahore","Istanbul","Turkey"],"bio":"My hometown is lahore."}

    score = getProfileComparisonScore(u1,u2)
    print(f"Score={score}")


    
    # # label, score = textSemantic("hello! I am not happy")
    # # print(f"\n>Text Semantic Score: {score} and label: {label} ")
    # text= ' New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.  A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.  Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.  In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.  Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the  2010 marriage license application, according to court documents.  Prosecutors said the marriages were part of an immigration scam.  On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.  After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective  Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.  All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.  Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.  Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.  The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s  Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.  Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.  If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18. '
    # summary = textSummarization(text)
    # # print(f"\n>Text Summary: {summary}" )

    # score = textSimilarity(text,summary)
    # print(f"\n>Text Similarity Score: {score}")

    # score = imageSimilarity("./images/i1.jpg","./images/i2.jpg")
    # # print(f"\n>Image Similarity Score: {score}")
    # # s1 = "waris.gill"
    # # s2 = "gil.waris"
    # # score = usernameSimilarityScore(s1,s2)
    # print(f"ner 2= {namedEntityRecogntion(text)}")
    # print(f"ner 1 = {namedEntityRecogntion(summary)}")
   


#     print(f"Score={score}")
    

    
    

    


#%%

 # label, score = textSemantic("hello! I am not happy")
    # print(f"\n>Text Semantic Score: {score} and label: {label} ")
# text= ' New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.  A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.  Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.  In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.  Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the  2010 marriage license application, according to court documents.  Prosecutors said the marriages were part of an immigration scam.  On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.  After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective  Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.  All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.  Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.  Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.  The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s  Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.  Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.  If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18. '
# summary = textSummarization(text)
# print(f"\n>Text Summary: {summary}" )

# score = textSimilarity(text,summary)
# print(f"\n>Text Similarity Score: {score}")

# score = imageSimilarity("./images/i1.jpg","./images/i2.jpg")
# print(f"\n>Image Similarity Score: {score}")
# s1 = "waris.gill"
# s2 = "gil.waris"
# score = usernameSimilarityScore(s1,s2)


#%%


# %%
