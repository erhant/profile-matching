import webbrowser
import path

BOILERPLATE = "ux/boilerplate.html"

def prepareHTML():
  '''
  fields are to be replace as {{fieldName}}.
  these are: title, description, twName, twBio, twImageURL, fbName, fbBio, fbImageURL
  for the features, add <tr><td>featureName</td><td>featureContent</td><td>weight</td><td>score</td></tr>
  '''
  with open(BOILERPLATE) as f:
    html = f.read()
  
  # Add statics
  
  # Add feature rows
def openHTML(name):
  new = 2 # open in a new tab, if possible  
  # open an HTML file on my own (Windows) computer
  url = "file://" + "ux/"+ name + ".html"
  webbrowser.open(url,new=new)
