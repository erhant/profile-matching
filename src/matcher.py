
def textSimilarity(text1, text2): # compare locations, educations etc.
    return 1 # todo

def imageSimilarity(image1, image2): # compare profile images
    return 1 # todo

def textSemantic(text): # maybe compare headline with tweets?
    return 1 # todo


class Matcher:
    def __init__(self, db):
        self.db = db # connection to be used by matcher
        
    def findMatchForTwitter(twitterUser):
        return 1 # todo
    
    def findMatchForFacebook(facebookUser):
        return 1 # todo