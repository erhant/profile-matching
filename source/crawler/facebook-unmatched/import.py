from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
import json
import string
import os

import os, sys

# Open a file
path = "."
dirs = os.listdir( path )

# This would print all the files and directories
for file in dirs:
	os.system("mongoimport --db facebook-twitter --collection facebook --file "+str.rstrip(user)+".json")
