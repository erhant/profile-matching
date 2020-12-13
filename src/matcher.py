#%%
import re
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer, util
import torch


def imageSimilarity(image1, image2): # compare profile images
    return 1 # todo

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
    return cosine_scores[0]

def textSummarizatin(text):
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
    
    label, score = textSemantic("hello! I am not happy")
    print(label, score)
    text= ' New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.  A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.  Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.  In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.  Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the  2010 marriage license application, according to court documents.  Prosecutors said the marriages were part of an immigration scam.  On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.  After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective  Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.  All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.  Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.  Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.  The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s  Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.  Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.  If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18. '
    summary = textSummarizatin(text)
    print(summary)
    score = textSimilarity(text,summary)
    print(score)
    
    

    


# %%
