from mongo import Mongo

mongoCreds = {
    "MONGO_HOST": "209.250.251.192",
    "MONGO_USER": "root",
    "MONGO_PASS": "PASSWORD",
    "PKEY_PATH": "C:/Users/ASUS/.ssh/id_rsa",
    "PKEY_PASS" : "",
    "MONGO_DB": "facebook-twitter"
}

m = Mongo()
m.connect()
###############

m.listCollections()

###############
m.terminate()