# Profile Matching
Term project for COMP530 - Data Privacy and Security.

## Dataset

### Facebook User
A facebook user document has:
- 3 fields for `education`
- 3 fields for `work`
- Location
- Name
- Photo
- Site (more like headline)
- Website
- Background Photo
- Biography
- Username

### Twitter User
A facebook user document has:
- Followings array
- Followers array
- Location
- Name
- Photo
- Site (more like headline)
- Website
- Background Photo
- Biography
- Username

## TODOs
-  Look at how social media sites' APIs work currently, as they tend to change in time. These APIs provide opportunity for you to crawl users' profiles.
Some users tend to link their social media profiles explicitly, e.g., they give a URL to their Twitter account on Instagram. You can assume these are your ground truth. Then attempt to perform profile matching as if these URLs did not exist. Check whether your profile matching algorithm can detect if these accounts indeed belong to the same user. (ie: compare your output with the ground truth)

## Resources
- [Jain et al. "@I seek 'fb.me': Identifying users across multiple online social networks"](https://github.com/erhant/profile-matching/blob/main/resources/Jain%20et.%20al.%20-%20I%20seek%20fbme%20Identifying%20Users%20across%20Multiple%20Online%20Social%20Networks%20(2013).pdf)
- [Halimi and Ayday. "Profile matching across online social networks"](https://github.com/erhant/profile-matching/blob/main/resources/Halimi%2C%20Ayday%20-%20Profile%20Matching%20Across%20Online%20Social%20Networks%20(2020).pdf)
