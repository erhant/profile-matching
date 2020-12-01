from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
import json
import string
import os


data = {}
users = []
with open('facebook_usernames.txt') as my_file:
    for line in my_file:
        users.append(line)
print(len(users))

for user in users:
	print(user)
	s="mv "+str.rstrip(user)+"*.txt "+str.rstrip(user)+".txt"
	print(s)
	os.system(s)



