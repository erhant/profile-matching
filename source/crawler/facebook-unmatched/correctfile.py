from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
import json
import string
import os

def save_as_json(filename, data):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)

olddata = {}
newdata={}
users = []
with open('facebook_usernames.txt') as my_file:
    for line in my_file:
        users.append(line)
print(len(users))

for user in users:
	with open(str.rstrip(user)+".txt") as f:
		olddata=json.load(f)
		newdata["_id"]=str.rstrip(user)
		newdata["matched"]=None
		newdata.update(olddata)
		save_as_json(str.rstrip(user)+".json", newdata)