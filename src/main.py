from mongo import Mongo
from matcher import Matcher

MONGO_CREDS = {
    "MONGO_HOST": "209.250.251.192",
    "MONGO_USER": "root",
    "MONGO_PASS": "PASSWORD",
    "PKEY_PATH": "C:/Users/ASUS/.ssh/id_rsa",
    "PKEY_PASS" : "",
    "MONGO_DB": "last-facebook-twitter"
}
FACEBOOK = "Facebook"
TWITTER = "Twitter"

mon = Mongo()
mon.connect()
matcher = Matcher(mon)

TEST_TYPE = "direct_fb" # edit this depending on your need

###############

if TEST_TYPE == "direct_fb":
  match = matcher.findMatchForFacebookUser('Itzhakperlmanofficial')
  matcher.outputMatch(match)
elif TEST_TYPE == "direct_tw":
  match = matcher.findMatchForTwitterUser('PerlmanOfficial')
  matcher.outputMatch(match)
elif TEST_TYPE == "indirect_fb":
  match = matcher.findIndirectMatchForFacebookUser('Itzhakperlmanofficial')
  matcher.outputMatch(match)
elif TEST_TYPE == "indirect_tw":
  match = matcher.findIndirectMatchForTwitterUser('PerlmanOfficial')
  matcher.outputMatch(match)
elif TEST_TYPE == "getuser_fb":
  (f, fd) = mon.getFacebookUser('Itzhakperlmanofficial', returnDoc = True)
elif TEST_TYPE == "getuser_tw":
  (t, td) = mon.getTwitterUser('PerlmanOfficial', returnDoc = True)
#elif TEST_TYPE == "direct_eval":
#  
else:
  print("Arbitrary test.")

###############
  
mon.terminate()

