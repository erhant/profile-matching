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

(f, fd) = mon.getFacebookUser('anu.sethi.188')
(t, td) = mon.getTwitterUser('abnicken')
matcher = Matcher(mon.db)

###############

mon.terminate()