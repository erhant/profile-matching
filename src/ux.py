import os
import pathlib

BOILERPLATE = "ux/boilerplate.html"
TOKENS = {
    'title': '{{title}}',
    'description': '{{description}}',
    'twName': '{{twName}}',
    'twBio': '{{twBio}}',
    'twImageURL': '{{twImageURL}}',
    'fbName': '{{fbName}}',
    'fbBio': '{{fbBio}}',
    'fbImageURL': '{{fbImageURL}}',
    'rows': '{{tableRows}}',
    'feature': lambda feat, weight, score : "<tr><td>"+str(feat)+"</td><td>"+str(weight)+"</td><td>"+str(score)+"</td></tr>" 
}

def outputHTML(twitterUser, facebookUser, score, similarities, title = "Direct Matching"):
  '''
  fields are to be replace as {{fieldName}}.
  these are: title, description, twName, twBio, twImageURL, fbName, fbBio, fbImageURL
  for the features, add <tr><td>featureName</td><td>featureContent</td><td>weight</td><td>score</td></tr>
  '''
  #if (twitterUser['sourceCollection'] != 'Twitter') or (facebookUser['sourceCollection'] != 'Facebook'):
  #  raise Exception("Collection mismatch.")
    
  with open(BOILERPLATE, "r") as f:
    html = f.read()
  html = html.replace(TOKENS['title'], title)
  html = html.replace(TOKENS['description'], "Profile matched with score " + str(score))
  html = html.replace(TOKENS['twName'], twitterUser['username'])
  html = html.replace(TOKENS['twBio'], twitterUser['bio'])
  html = html.replace(TOKENS['twImageURL'], twitterUser['profileImage'])
  html = html.replace(TOKENS['fbName'], facebookUser['username'])
  html = html.replace(TOKENS['fbBio'], facebookUser['bio'])
  html = html.replace(TOKENS['fbImageURL'], facebookUser['profileImage'])
  rows = ""
  for feat in similarities:
    rows += TOKENS['feature'](feat, similarities[feat]['weight'], similarities[feat]['score'])
  html = html.replace(TOKENS['rows'], rows)
  filename = twitterUser['username'] + "-" + facebookUser["username"]
  with open("ux/"+filename+".html", "w") as f:
    f.write(html)
  
  os.startfile(str(pathlib.Path(__file__).parent.absolute()) + "\\ux\\"+ filename + ".html")
  
if __name__ == "__main__":
  outputHTML(ans[0], ans[0], ans[1], ans[2])