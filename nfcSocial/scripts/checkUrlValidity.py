import requests
from bs4 import BeautifulSoup

"""
instaId = "kavyakhurana"

page = requests.get("https://www.instagram.com/" + instaId)
soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

title = soup.find("title")

if "Page Not Found " in title.text.strip():
	print "Invalid ID"
else:
	print "Valid ID"

tubeUserId = "allindiabakchod"

page = requests.get("https://www.youtube.com/user/" + tubeUserId)
soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

title = soup.find("title")


if "YouTube" == title.text.strip():
	print "Invalid ID"
else:
	print "Valid ID"


tubeChannelId = "UCAuUUnT6oDeKwE6v1NGQxug"

page = requests.get("https://www.youtube.com/channel/" + tubeChannelId)
soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

title = soup.find("title")


if "YouTube" == title.text.strip():
        print "Invalid ID"
else:
        print "Valid ID"



tubeVideoId = "J_Sc7hYKstI"

page = requests.get("https://www.youtube.com/watch?v=" + tubeVideoId)
soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

title = soup.find("title")


if "YouTube" == title.text.strip():
        print "Invalid ID"
else:
        print "Valid ID"



tweetUserId = "rahulyadav360"

page = requests.get("https://twitter.com/intent/user?screen_name=" + tweetUserId)
soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

title = soup.find("title")

print title.text.strip()

if "Twitter / ?" == title.text.strip():
        print "Invalid ID"
else:
        print "Valid ID"



"""

tweetUserId = "rahulyadav360"

page = requests.get("https://twitter.com/intent/user?screen_name=" + tweetUserId)
soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

title = soup.find("title")

print title.text.strip()

if "Twitter / ?" == title.text.strip():
        print "Invalid ID"
else:
        print "Valid ID"




