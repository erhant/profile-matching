import os
import pathlib

BOILERPLATE = "ux/boilerplate.html"
TOKENS = {
  'title': '{{title}}',
  'description': '{{description}}',
  'twName': '{{twName}}',
  'twBio': '{{twBio}}',
  'twImageURL': '{{twImageURL}}',
  'twProfileURL': '{{twProfileURL}}',
  'fbName': '{{fbName}}',
  'fbBio': '{{fbBio}}',
  'fbImageURL': '{{fbImageURL}}',
  'fbProfileURL': '{{fbProfileURL}}',
  'rows': '{{tableRows}}',
  'feature': lambda feat, score : "<tr><td>"+str(feat)+"</td><td>"+str(score)+"</td></tr>" 
}

def outputHTML(twitterUser, facebookUser, score, similarities, title = "Direct Matching"):
  '''Creates an HTML output, and then opens it with os.startfile command.
  
  Fields are to be replaced as {{fieldName}}. In particular these are: title, description, twName, twBio, twImageURL, fbName, fbBio, fbImageURL.
  For features and their scores, table rows are generated as <tr><td>featureName</td><td>score</td></tr>
  '''
  #if (twitterUser['sourceCollection'] != 'Twitter') or (facebookUser['sourceCollection'] != 'Facebook'):
  #  raise Exception("Collection mismatch.")
    
  with open(BOILERPLATE, "r") as f:
    html = f.read()
  html = html.replace(TOKENS['title'], title)
  html = html.replace(TOKENS['description'], "Profile matched with score (or probability) " + str(score))
  html = html.replace(TOKENS['twName'], twitterUser['username'])
  html = html.replace(TOKENS['twBio'], twitterUser['bio'])
  html = html.replace(TOKENS['twImageURL'], twitterUser['profileImage'])
  html = html.replace(TOKENS['twProfileURL'], "https://twitter.com/"+twitterUser['username'])
  html = html.replace(TOKENS['twName'], twitterUser['username'])
  html = html.replace(TOKENS['fbName'], facebookUser['username'])
  html = html.replace(TOKENS['fbBio'], facebookUser['bio'])
  html = html.replace(TOKENS['fbImageURL'], facebookUser['profileImage'])
  html = html.replace(TOKENS['fbProfileURL'], "https://www.facebook.com/"+facebookUser['username'])
  rows = ""
  for feat in similarities:
    rows += TOKENS['feature'](feat, similarities[feat])
  html = html.replace(TOKENS['rows'], rows)
  filename = twitterUser['username'] + "-" + facebookUser["username"]
  with open("ux/"+filename+".html", "w") as f:
    f.write(html)
  
  os.startfile(str(pathlib.Path(__file__).parent.absolute()) + "\\ux\\"+ filename + ".html")
