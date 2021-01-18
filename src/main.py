from mongo import Mongo
from matcher import Matcher

METHOD = "ML_direct_fb" # edit this depending on your need

mon = Mongo()
mon.connect()
###############

if METHOD == "getuser_fb":
  (f, fd) = mon.getFacebookUser('MayorMurielBowser', returnDoc = True)
elif METHOD == "getuser_tw":
  (t, td) = mon.getTwitterUser('PerlmanOfficial', returnDoc = True)
else:
  matcher = Matcher(mon) # note that this takes a bit of time to load
  
  if METHOD == "direct_fb":
    match = matcher.findMatchForFacebookUser('Itzhakperlmanofficial', useML=False)
    
  elif METHOD == "direct_tw":
    match = matcher.findMatchForTwitterUser('PerlmanOfficial', useML=False)
    
  elif METHOD == "indirect_fb":
    match = matcher.findIndirectMatchForFacebookUser('Itzhakperlmanofficial', useML=False)
    
  elif METHOD == "indirect_tw":
    match = matcher.findIndirectMatchForTwitterUser('PerlmanOfficial', useML=False)
    
  elif METHOD == "ML_direct_fb":
    match = matcher.findMatchForFacebookUser('pwnslinger')
    
  elif METHOD == "ML_direct_tw":
    match = matcher.findMatchForTwitterUser('PerlmanOfficial')
    
  elif METHOD == "ML_indirect_fb":
    match = matcher.findIndirectMatchForFacebookUser('Itzhakperlmanofficial')
    
  elif METHOD == "ML_indirect_tw":
    match = matcher.findIndirectMatchForTwitterUser('PerlmanOfficial')
    
  else:
    print("Unknown method: "+METHOD)

###############  
mon.terminate()

'''
Some example users:
  Twitter:
    PerlmanOfficial
    waitbutwhy
    pwnslinger
    
  Facebook:
    Itzhakperlmanofficial
    timurban80
    pwnslinger
    
'''