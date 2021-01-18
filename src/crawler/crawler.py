
# This is a library for extracting Facebook and Twitter profile information
# developed by Mandana Bagheri Marzijarani (mmarzijrani@ku.edu.tr)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
import json

debug = print
debug = lambda x: None

def file_get_contents(filename):
	with open(filename, 'r') as file:
		return file.read()

def jquery_code():
	return file_get_contents("jquery.js")

def scroll_down(driver, page_count = 15, wait = 5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait)
        new_height = driver.execute_script("return document.body.scrollHeight")
        page_count-=1
        if new_height == last_height or page_count <= 0:
            break
        last_height = new_height

def scroller_code(page_count):
	return """
var lastHeight = 0;
var scrollMaxCount = "{}"*1;
var scrollingDone = 0;
function scrollIt()
{{
	if (scrollMaxCount-- > 0 && lastHeight < document.body.scrollHeight)
	{{
		window.scrollTo(0,document.body.scrollHeight);
		lastHeight = document.body.scrollHeight;
		setTimeout(scrollIt, 5000);
		return;
	}}
	scrollingDone = 1;
}}
scrollIt();
""".format(page_count);

def wait_for_ready(driver, js, match = None, timeout = 10):
	for i in range(1, timeout*20): # Wait timeout
		r = driver.execute_script(js)
		debug (r)
		if match is None and r != "": break; # non-empty result
		if match is not None and r == match: break; # result matches expected
		time.sleep(50/1000)
	time.sleep(.5)
	return r

def twitter_login(driver, username, password):
	driver.get("https://twitter.com/login")
	driver.execute_script(jquery_code()); # Inject jquery

	wait_for_ready(driver, 'return document.readyState', 'complete')
	# wait_for_ready(driver, 'return jQuery("div:contains(\'Log Into Facebook\')").text()')
	print ("Please login manually :(")
	print ("User creds:\n\tUsername: {}\n\tPassword: {}".format(username, password))

	for i in range(15,0,-1):
		print (i, "...")
		time.sleep(1)
	# wait_for_ready(driver, 'return jQuery("div").filter(function(){return $(this).text()=="Log in to Twitter";}).text()')
	# print ("Login page ready.")
	# js = """
	# 	jQuery('input[name="session[username_or_email]"]').val('{}')
	# 	jQuery('input[name="session[password]"]').val('{}')
	# 	jQuery('input[name="session[password]"]').change()
	# 	jQuery('form[action="/sessions"]').submit()

	# """.format(username, password)

	# x=driver.execute_script(js)
	time.sleep(3)
	return True


def twitter_extract(driver, twitter_user):
	print("-----starting to extract information from Twitter profile-----")
	data = {}

	driver.get("https://twitter.com/"+twitter_user)

	driver.execute_script(jquery_code()); # Inject jquery

	wait_for_ready(driver, 'return document.readyState', 'complete')
	print (twitter_user, "Page ready!")

	wait_for_ready(driver, 'return jQuery("main>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(1)>div:eq(0)>div:eq(0)>div:eq(1)").text()')
	time.sleep(1)
	print (twitter_user, "Feed ready!")

	js = """
var root = jQuery("main>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(1)>div:eq(0)>div:eq(0)");
var bio = root.find(">div:eq(0)>div:eq(0)");
data = {}
data['photo'] = bio.find(">div:eq(0)>a>div>div:eq(1)>div>img").attr("src")

data['name'] = bio.find(">div:eq(1)>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)").text()
data['handle'] = bio.find(">div:eq(1)>div:eq(0)>div:eq(0)>div:eq(1)").text()

data['bio'] = bio.find(">div:eq(2)").text()

data['joined'] = bio.find(">div:eq(3)>div>*:contains('Joined')").text()
data['born'] = bio.find(">div:eq(3)>div>*:contains('Born')").text()
data['location'] = bio.find(">div:eq(3)>div>*:not(:contains(Born)):not(:contains(.)):not(:contains(Joined))").text()
data['site'] = bio.find(">div:eq(3)>div>*:contains(.):not(:contains(Born)):not(:contains(Joined))").text()

data['following'] = bio.find(">div:eq(4)>div>*:eq(0)").text()
data['followers'] = bio.find(">div:eq(4)>div>*:eq(1)").text()

var feed = root.find(">div:eq(1)");
if (feed.text()=="Something went wrong.Try again") // Rate limit
	data['tweets'] = undefined;
else
{
	tweets = feed.find(">section>div>div")
	data['tweets'] = [];
	for (i=0; i<5; ++i)
	{
		var tweet = tweets.find(">div:eq("+i+")")
		var info = tweet.find(">div>div>article>div>div>div>div[data-testid=tweet]>div:eq(1)>div:eq(0)")
		// Info is not utilized yet.
		var body = tweet.find(">div>div>article>div>div>div>div[data-testid=tweet]>div:eq(1)>div:eq(1)")
		data['tweets'].push(body.text())
	}
}
return data;
"""

	x=driver.execute_script(js)
	data = {**data, **x} # join

	# This part of code extracts follower and following list of Twitter user but since
	# it takes too many requests to Twitter to extract a fraction of a user follower/following list
	# and Twitter immediately blocks the user account, I have disabled this feature from twitter_extract function.

	# for page in ["followers", "following"]:
	# 	# twitter followers/following
	# 	driver.get("https://twitter.com/"+twitter_user+"/"+page)
	# 	driver.execute_script(jquery_code()); # Inject jquery
	# 	wait_for_ready(driver, 'return document.readyState', 'complete')
	# 	print (twitter_user, page + " page ready.")

	# 	time.sleep(3)
	# 	scroll_down(driver, 10, 3) # 15 pages, 3 seconds wait for each scroll
	# 	print (twitter_user, page + " scroll done.")

	# 	driver.execute_script("document.body.style.zoom = '.25' // Zoom out")
	# 	time.sleep(2)

	# 	js = """

	# 	var root = jQuery("main");
	# 	var content = root.find(">div:eq(0)".repeat(5))
	# 	var list = content.find(">div:eq(1)>section>div:eq(0)>div:eq(0)")

	# 	var friendsUrls = list.find(">div".repeat(6) + ">a").map(function() {{
	# 			return this.href;
	# 		}}).get();
	# 	data = {{}}
	# 	data['{}'] = friendsUrls;
	# 	return data;
	# 	""".format(page)
	# 	x=driver.execute_script(js)
	# 	data = {**data, **x} # join
	# print(x)
	print("-----end of extracting information from Twitter profile-----")
	return data

def facebook_login(driver, username, password):
	print("-----starting to extract information from Facebook profile-----")
	driver.get("https://facebook.com/login")
	driver.execute_script(jquery_code()); # Inject jquery

	wait_for_ready(driver, 'return document.readyState', 'complete')
	# wait_for_ready(driver, 'return jQuery("div:contains(\'Log Into Facebook\')").text()')
	wait_for_ready(driver, 'return jQuery("div").filter(function(){return $(this).text()=="Log Into Facebook";}).text()')
	print ("Login page ready.")

	js = """
		jQuery('input[name=email]').val('{}')
		jQuery('input[name=pass]').val('{}')
		jQuery('button[type=submit]').click()

	""".format(username, password)

	x=driver.execute_script(js)
	time.sleep(3)
	return True

def facebook_extract(driver, facebook_user):
	# start
	driver.get("https://facebook.com/"+facebook_user+"")
	driver.execute_script(jquery_code()); # Inject jquery
	wait_for_ready(driver, 'return document.readyState', 'complete')


	wait_for_ready(driver, 'return jQuery("div.w0hvl6rk.qjjbsfad:contains(\'Do you know \')").text()')
	print (username, "Feed ready!")

	data = {}

	js = """
	var page = jQuery("div[data-pagelet=page]")
	var header = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)")
	var body = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(3)")
	data = {}

	data['bg'] = header.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(1) img").attr("src")
	data['photo'] = header.find(">div:eq(1) image").attr("xlink:href")
	data['name'] = header.find(">div:eq(1) >div:eq(0) >div:eq(0) >div:eq(1) >div:eq(0) >div:eq(0) >div:eq(0)").text()
	data['site'] = header.find(">div:eq(1) >div:eq(0) >div:eq(0) >div:eq(1) >div:eq(0) >div:eq(0) >div:eq(1)").text()
	return data
	"""
	x=driver.execute_script(js)
	data = {**data, **x} # join



	driver.get("https://facebook.com/"+facebook_user+"/about")
	driver.execute_script(jquery_code()); # Inject jquery
	wait_for_ready(driver, 'return document.readyState', 'complete')
	js = """
	var page = jQuery("div[data-pagelet=page]")
	var header = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)")
	var body = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(3)")
	var content = body.find(">div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(1) >div:eq(0) >div:eq(0) >div:eq(0) ")

	data = {}
	data['location'] = content.find("div:contains('Lives in ')>a").text()
	function text_as_array(selector) {
		var arr = selector.find("div,span")//.find(":not(:has(*))")
			.map(function(){
				return $(this).text();
			}).get().filter(function (x) { return x.length>2; })

   	return jQuery.unique(arr)
	}
	data['work'] = text_as_array(content.find(">div:eq(0) >div:eq(0)"))
	data['education'] = text_as_array(content.find(">div:eq(1) >div:eq(0)"))
	return data
	"""
	x=driver.execute_script(js)
	data = {**data, **x} # join

	driver.get("https://facebook.com/"+facebook_user+"/about_contact_and_basic_info")
	driver.execute_script(jquery_code()); # Inject jquery
	wait_for_ready(driver, 'return document.readyState', 'complete')
	js = """
	var page = jQuery("div[data-pagelet=page]")
	var header = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)")
	var body = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(3)")
	var content = body.find(">div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(1) >div:eq(0) >div:eq(0)")

	data = {}
	data['website'] = content.find(">div:eq(1) >div:eq(1)").text()
	data['birthdate'] = content.find(">div:eq(2) >div:eq(2)").text()
	// content.find(">div:eq(2) div:contains('of birth'):not(:has(:contains('of birth'))) ")
	return data
	"""
	x=driver.execute_script(js)
	data = {**data, **x} # join

	driver.get("https://facebook.com/"+facebook_user+"/about_details")
	driver.execute_script(jquery_code()); # Inject jquery
	wait_for_ready(driver, 'return document.readyState', 'complete')
	js = """
	var page = jQuery("div[data-pagelet=page]")
	var header = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)")
	var body = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(3)")
	var content = body.find(">div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(1) >div:eq(0) >div:eq(0)")

	data = {}
	data['bio'] = content.find(">div:eq(0) >div:eq(1)").text()
	return data
	"""
	x=driver.execute_script(js)
	data = {**data, **x} # join

	driver.get("https://facebook.com/"+facebook_user+"/about_work_and_education")
	driver.execute_script(jquery_code()); # Inject jquery
	wait_for_ready(driver, 'return document.readyState', 'complete')
	js = """
	var page = jQuery("div[data-pagelet=page]")
	var header = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)")
	var body = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(3)")
	var content = body.find(">div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(0) >div:eq(1) >div:eq(0) >div:eq(0)")

	function text_as_array(selector) {
		var arr = selector.find("div,span")//.find(":not(:has(*))")
			.map(function(){
				return $(this).text();
			}).get().filter(function (x) { return x.length>2; })

   	return jQuery.unique(arr)
	}
	data = {}
	data['work1'] = text_as_array(content.find(">div:eq(0) >div:eq(1)"))
	data['work2'] = text_as_array(content.find(">div:eq(0) >div:eq(1)"))
	data['education1'] = text_as_array(content.find(">div:eq(1) >div:eq(1)"))
	data['education2'] = text_as_array(content.find(">div:eq(1) >div:eq(2)"))
	return data
	"""
	x=driver.execute_script(js)
	data = {**data, **x} # join

	# facebook friends
	driver.get("https://facebook.com/"+facebook_user+"/friends")
	driver.execute_script(jquery_code()); # Inject jquery
	wait_for_ready(driver, 'return document.readyState', 'complete')

	time.sleep(10) # initial friends list load
	scroll_down(driver, 15, 5) # 15 pages, 5 seconds wait for each scroll

	js = """
	var page = jQuery("div[data-pagelet=page]")
	var header = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)")
	var body = page.find(">div:eq(0)>div:eq(0)>div:eq(0)>div:eq(3)")
	var content = body.find(">div:eq(0)".repeat(7))
	var friendsDiv = content.find(">div:eq(2)");
	var friendsUrls = friendsDiv.find(">div >div >a").map(function() {
			return this.href;
		}).get();
	data = {}
	data['friends'] = friendsUrls;
	return data;
	"""
	x=driver.execute_script(js)
	data = {**data, **x} # join

	# pprint (data)
	print("-----end of extracting information from Facebook profile-----")
	return data

def save_as_json(filename, data):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36")
opts.add_argument("--disable-notifications");

# opts.add_argument("--headless") Headless loads do not improve the speed surprisingly


#Selenium Driver_____________________________________________________________
driver=webdriver.Chrome(options=opts)
driver.implicitly_wait(1)

#twitter_login(driver, username='Mandana92078897', password='yehajiboodyegorbedasht')


# output Data ______________________________________________________________
data = {}


#Facebook
#facebook login ____________________________________________________________
facebook_login(driver, username='mmarzijarani20@ku.edu.tr', password='Gholigholi1')
username="evansde"
#Extracting the Facebook information _______________________________________
data = facebook_extract(driver, username)
#Saving the output as json file ____________________________________________
save_as_json(username+".json", data)



# Twitter
# Twitter login ____________________________________________________________
# twitter_login(driver, username='Mandana92078897', password='yehajiboodyegorbedasht')
username="qureshiprinc"
# Extracting the Twitter information _______________________________________
data = twitter_extract(driver, username)
#Saving the output as json file ____________________________________________
save_as_json(username+".json", data)


driver.quit()

