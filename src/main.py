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

###############
#(f, fd) = mon.getFacebookUser('Itzhakperlmanofficial', returnDoc = True)
#(t, td) = mon.getTwitterUser('PerlmanOfficial', returnDoc = True)
#users = mon.getManyUsers(5, 10)

# matched user: PerlmanOfficial < -- > Itzhakperlmanofficial
matcher = Matcher(mon)
#matcher.populateNERs()
ans = matcher.findMatchForFacebookUser('Itzhakperlmanofficial')

###############

mon.terminate()

