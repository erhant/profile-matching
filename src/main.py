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
TEST_TYPE = "indirect_tw" # edit this depending on your need

mon = Mongo()
mon.connect()


if TEST_TYPE == "getuser_fb":
  (f, fd) = mon.getFacebookUser('Itzhakperlmanofficial', returnDoc = True)
elif TEST_TYPE == "getuser_tw":
  (t, td) = mon.getTwitterUser('PerlmanOfficial', returnDoc = True)
else:
  matcher = Matcher(mon)
  if TEST_TYPE == "direct_fb":
    match = matcher.findMatchForFacebookUser('Itzhakperlmanofficial')
  elif TEST_TYPE == "direct_tw":
    match = matcher.findMatchForTwitterUser('PerlmanOfficial')
  elif TEST_TYPE == "indirect_fb":
    match = matcher.findIndirectMatchForFacebookUser('Itzhakperlmanofficial')
  elif TEST_TYPE == "indirect_tw":
    match = matcher.findIndirectMatchForTwitterUser('PerlmanOfficial')
  elif TEST_TYPE == "ML_direct_fb":
    match = matcher.findMatchForFacebookUser('Itzhakperlmanofficial', useML=True)
  elif TEST_TYPE == "ML_direct_tw":
    match = matcher.findMatchForTwitterUser('PerlmanOfficial', useML=True)
  elif TEST_TYPE == "ML_indirect_fb":
    match = matcher.findIndirectMatchForFacebookUser('Itzhakperlmanofficial', useML=True)
  elif TEST_TYPE == "ML_indirect_tw":
    match = matcher.findIndirectMatchForTwitterUser('PerlmanOfficial', useML=True)
  else:
    print("Arbitrary test.")


###############



###############
  
mon.terminate()

