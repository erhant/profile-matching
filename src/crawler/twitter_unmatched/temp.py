#location, email, name, verified (true, false),
# created at, followers count ,following count, 
#  description, profile image(there is a url pointing 
#  to profile image), birthday(if applicable)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
import json
import string

debug = print
debug = lambda x: None

def file_get_contents(filename):
	with open(filename, 'r') as file:
		return file.read()

def jquery_code():
	return file_get_contents("jquery.js")

def wait_for_ready(driver, js, match = None, timeout = 10):
	for i in range(1, timeout*20): # Wait timeout
		r = driver.execute_script(js)
		debug (r)
		if match is None and r != "": break; # non-empty result
		if match is not None and r == match: break; # result matches expected
		time.sleep(50/1000)
	time.sleep(.5)
	return r

def twitter_extract(driver, twitter_user):
	driver.get("https://twitter.com/"+twitter_user)

	driver.execute_script(jquery_code()); # Inject jquery

	wait_for_ready(driver, 'return document.readyState', 'complete')
	print (str.rstrip(users[i]), "Page ready!")

	wait_for_ready(driver, 'return jQuery("main>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(0)>div:eq(1)>div:eq(0)>div:eq(0)>div:eq(1)").text()')
	time.sleep(1)
	print (str.rstrip(users[i]), "Feed ready!")

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
	# print(x)
	return x

def facebook_login(driver, username, password):
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
	driver.get("https://facebook.com/"+facebook_user+"")
	driver.execute_script(jquery_code()); # Inject jquery
	wait_for_ready(driver, 'return document.readyState', 'complete')


	wait_for_ready(driver, 'return jQuery("div.w0hvl6rk.qjjbsfad:contains(\'Do you know \')").text()')
	print (user, "Feed ready!")

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

	pprint (data)
	# time.sleep(20)
	return data

def save_as_json(filename, data):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36")
# opts.add_argument("--headless")

driver=webdriver.Chrome(options=opts)
driver.implicitly_wait(1)

data = {}
users = []
with open('twitter_usernames.txt') as my_file:
    for line in my_file:
        users.append(line)
print(len(users))

#facebook
# facebook_login(driver, username='mmarzijarani20@ku.edu.tr', password='Gholigholi1')

# for user in users:
# 	data[user] = facebook_extract(driver, user)
# 	save_as_json(user+".txt", data[user])


# Twitter
# for i in range(31,865):
# 	print(i)
# 	data[str.rstrip(users[i])] = twitter_extract(driver, str.rstrip(users[i]))
# 	save_as_json(str.rstrip(users[i])+".txt", data[str.rstrip(users[i])])

jdata={}
empty=0
null=0
for i in range(0,863):
	with open(str.rstrip(users[i])+".txt") as file:
  		jdata = json.load(file)
  		# print(str.rstrip(users[i]))
  		if jdata['tweets'] is None:
  			null+=1
  			# data[str.rstrip(users[i])] = twitter_extract(driver, str.rstrip(users[i]))
  			# save_as_json(str.rstrip(users[i])+".txt", data[str.rstrip(users[i])])
  			print(str.rstrip(users[i])+"null")
  			continue
  		elif jdata['tweets'][0]=="":
  			empty+=1
  			print(str.rstrip(users[i])+"empty")
  			# data[str.rstrip(users[i])] = twitter_extract(driver, str.rstrip(users[i]))
  			# save_as_json(str.rstrip(users[i])+".txt", data[str.rstrip(users[i])])
print(empty)
print(null)


driver.quit()

# twitter_extract("abiusx")
# twitter_extract("jack")