from mongo import Mongo
from matcher import Matcher

MONGO_CREDS = {
    "MONGO_HOST": "209.250.251.192",
    "MONGO_USER": "root",
    "MONGO_PASS": "PASSWORD",
    "PKEY_PATH": "C:/Users/ASUS/.ssh/id_rsa",
    "PKEY_PASS" : "",
    "MONGO_DB": "facebook-twitter"
}
FACEBOOK = "facebook"
TWITTER = "twitter"

mon = Mongo()
mon.connect()
###############

matcher = Matcher(mon.db)
(f, _) = matcher.getFacebookUser('anu.sethi.188')
(t, _) = matcher.getTwitterUser('abnicken')

###############
mon.terminate()