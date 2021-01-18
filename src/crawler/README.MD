# Facebook & Twitter Crawler
This python script is used for extracting Facebook & Twitter profile information as an alternative to using Facebook and Twitter APIs.

## Requirements
- Selenium Webdriver 
- jQuery.js


## How to extract a Facebook profile using the cralwer
Since there is no way to extract whole Facebook information without loging in, we have defined a function called `facebook_login(driver, username, password)` that takes in selenuim webdriver, the username and password you want to use to login and performs the logging in step automatically, so before extracting Facebook information the first step is to call this function with an active facebook username/password.

`facebook_login(driver, "yourusername"', "yourpassword")`

After loggging in youto extract facebook information call the function `facebook_extract(driver, facebook_user)` that takes a Selenium Webdriver and a facebook username, extract user's profile information and returns a python dictionary.

`data=facebook_extract(driver, "The facebook username that you want to extract its information")`

To save the output, we have defined a function called `save_as_json(filename, data)` that takes the output dictionary and name of the output file and saves the dictionary in a json file called filename.

`save_as_json("name of outputfile", data)`


## How to extract a Twitter profile using the cralwer
All Twitter information other than the list of follower/following can be extracted from Twitter without logging in. The first step you need to do to exract the Twitter's information is to call the function `twitter_extract(driver, twitter_user)` that takes a Selenium Webdriver and a Twitter username, extract user's profile information and returns a python dictionary.

`data=twitter_extract(driver, "The Twitter username that you want to extract its information")`

again to save the output, we have defined a function called `save_as_json(filename, data)` that takes the output dictionary and name of the output file and saves the dictionary in a json file called filename.

`save_as_json("name of outputfile", data)`

## How to run the crawler
To run the crawler, you need Selenium installed and you also need the jquery.js file pressent in the same folder as crawler.py, to run the crawler simply run the command below:

`python3 crawler.py`
