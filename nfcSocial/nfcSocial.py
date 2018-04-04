# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify, send_from_directory
from pymongo import MongoClient
import pymongo
import datetime
import requests
import json
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from bs4 import BeautifulSoup
import base64
import random,string

encryption = "Dumisani Nthanda"

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)




client = MongoClient("192.168.10.150", 27017 )
db = client["nfcSocialCards"]


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

photos = UploadSet('photos', IMAGES)
# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='nfcSocialSecretKey',
    USERNAME='admin',
    PASSWORD='default',
    
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/image'
configure_uploads(app, (photos,))

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

def convert_and_save(b64_string,filePath):
    with open(filePath, "wb") as fh:
	print b64_string.encode()
        fh.write(base64.b64decode(b64_string.strip().split(",")[-1].encode()))

availableSchemes = ["snapchat","facebook","twitter","instagram","linkedin","youtube","uploads"]
typeList = [{"scheme" : "snapchat" , "text" : "Snapchat"},{"scheme" : "instagram" , "text" : "Instagram"},{"scheme" : "twitter" , "text" : "Twitter"},{"scheme" : "facebook" , "text" : "Facebook"},{"scheme" : "linkedin" , "text" : "LinkedIn"},{"scheme" : "youtube" , "text" : "Youtube"}]
def cssChecker(keyword):
	keyword = keyword.strip()
	if keyword == "snapchat":
		return "agency_snapChat.min.css"
	elif keyword == "facebook":
		return "agency_faceBook.min.css"
	elif keyword == "twitter":
		return "agency_twitter.min.css"
	elif keyword == "instagram":
		return "agency_instagram.min.css"
	elif keyword == "linkedin":
		return "agency_linkedIn.min.css"
	elif keyword == "youtube":
		return "agency_youtube.min.css"
	else:
		return "agency.min.css"

def collectionNameGetter(keyword):
	keyword = keyword.strip()
        if keyword == "snapchat":
		return "snapUserData","snapTrackingData","snapCardPassword"
	elif keyword == "facebook":
                return "faceUserData","faceTrackingData","faceCardPassword"
        elif keyword == "twitter":
                return "tweetUserData","tweetTrackingData","tweetCardPassword"
        elif keyword == "instagram":
                return "instaUserData","instaTrackingData","instaCardPassword"
	elif keyword == "linkedin":
		return "linkedUserData" , "linkedTrackData","linkedCardPassword"
	elif keyword == "youtube":
		return "tubeUserData" , "tubeTrackData" , "tubeCardPassword"



def logoImageGetter(keyword):
        keyword = keyword.strip()
        if keyword == "snapchat":
		return "snapchat-1360003_640.png"
        elif keyword == "facebook":
		return "facebook-2429746_640.png"
        elif keyword == "twitter":
                return "twitter-2430933_640.png"
        elif keyword == "instagram":
                return "instagram-1882330_640.png"
        elif keyword == "linkedin":
                return "linkedin-2815969_640.jpg"
        elif keyword == "youtube":
                return "youtube-1837872_640.png"



def userNameGetter(keyword,userName):
	keyword = keyword.strip()
        if keyword == "snapchat":
		return userName,0
	if keyword == "facebook":
		sauce = requests.get('https://www.facebook.com/' + userName).content
		soup = BeautifulSoup(sauce,'html')
		a = soup.find("meta", property="al:ios:url")
		try:
			return str(a['content'].split('=',1)[1]),"page"
		except:
			try:
				return str(a['content'].split('/')[-1]),"profile"
			except:
				return 0,0
	if keyword == "instagram":
		return userName,0
	if keyword == "twitter":
                return userName,0
	if keyword == "linkedin":
		return userName,0
	if keyword == "youtube":
		return userName,0

def schemeUsageTextGetter(keyword,url):
        keyword = keyword.strip()
        if keyword == "snapchat":
                return "Add me"
        elif keyword == "facebook":
                return ""
        elif keyword == "twitter":
                return ""
        elif keyword == "instagram":
                return "Follow"
        elif keyword == "linkedin":
                return "Connect"
        elif keyword == "youtube":
		if "https://www.youtube.com/user/" in url:
                	return "Subscribe"
		elif "https://www.youtube.com/channel/" in url:
                	return "Subscribe"
		elif "https://www.youtube.com/watch?v=" in url:
			return "Watch"

def schemeUsageTypeGetter(keyword):
	keyword = keyword.strip()
        if keyword == "snapchat":
		return 0
	elif keyword == "facebook":
		return 1
	elif keyword == "twitter":
		return 1
	elif keyword == "instagram":
		return 0
        elif keyword == "linkedin":
                return 0
	elif keyword == "youtube":
		return 0




def urlGetter(keyword,userName,extra = ""):
	keyword = keyword.strip()
	if keyword == "snapchat":
		browserUrl = "https://www.snapchat.com/add/" + userName.strip()
		iPhoneUrl = "snapchat://add/" + userName.strip()    
		androidUrl = "http://www.snapchat.com/add/" + userName.strip()
	elif keyword == "facebook":
		if extra == "page":
			androidUrl = "fb://page/" + userName.strip()
		elif extra == "profile":
			androidUrl = "fb://profile/" + userName.strip()
		browserUrl = "https://www.facebook.com/profile.php?id=" + userName.strip()
		iPhoneUrl = "fb://profile/" + userName.strip()    
	elif keyword == "twitter":
                browserUrl = "http://twitter.com/intent/user?screen_name=" + userName.strip()
                iPhoneUrl = "twitter://user?user_id=" + userName.strip()  
                androidUrl = "http://twitter.com/intent/user?screen_name=" + userName.strip()
	elif keyword == "instagram":
		browserUrl = "https://www.instagram.com/" + userName.strip()
                iPhoneUrl = "instagram://user?username=" + userName.strip()
                androidUrl = "instagram://user?username=" + userName.strip()
	elif keyword == "linkedin":
		browserUrl = "http://www.linkedin.com/in/"  + userName.strip()
                iPhoneUrl = "linkedin://profile/" + userName.strip()
                androidUrl = "http://www.linkedin.com/in/" + userName.strip()
	elif keyword == "youtubeVideo":
		browserUrl = "https://www.youtube.com/watch?v="  + userName.strip()
                iPhoneUrl = "https://www.youtube.com/watch?v=" + userName.strip()
                androidUrl = "https://www.youtube.com/watch?v=" + userName.strip()
	elif keyword == "youtubeUser":
		browserUrl = "https://www.youtube.com/user/"  + userName.strip()
                iPhoneUrl = "vnd.youtube://user/" + userName.strip()
                androidUrl = "vnd.youtube://user/" + userName.strip()
	elif keyword == "youtubeChannel":
		browserUrl = "https://www.youtube.com/channel/"  + userName.strip()
                iPhoneUrl = "youtube://www.youtube.com/channel/" + userName.strip()
                androidUrl = "https://www.youtube.com/channel/" + userName.strip()



	return browserUrl,iPhoneUrl,androidUrl


def getNameFromUrl(keyword,url):
	keyword = keyword.strip()
        if keyword == "snapchat":
		userName = url.split("/")[-1]		
        elif keyword == "facebook":
		userName = url.split("=")[-1]
        elif keyword == "twitter":
                userName = url.split("=")[-1]
        elif keyword == "instagram":
                userName = url.split("/")[-1]
        elif keyword == "linkedin":
                userName = url.split("/")[-1]
        elif keyword == "youtubeVideo":
                userName = url.split("=")[-1]
        elif keyword == "youtubeUser":
                userName = url.split("/")[-1]
        elif keyword == "youtubeChannel":
                userName = url.split("/")[-1]
	else:
		userName = ""
	return userName



def getYouTubeContentType(url):
	if "user" in url:
		contentType = "User"
	elif "channel" in url:
		contentType = "Channel"
	elif "watch" in url:
		contentType = "Video"
	else:
		contentType = "User"
	return contentType

def variableFound(keyword):
	keyword = keyword.strip()
	if keyword in availableSchemes:
		return False
	else:
		return True


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', cssName="agency.min.css"), 404

@app.route('/stats', methods=['GET'])
def showStats():
        legend = 'Monthly Data'
        labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
        values = [10, 9, 8, 7, 6, 4, 7, 8]
	return render_template('statsPage.html',cssName="agency.min.css", values=values, labels=labels, legend=legend)




@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
    	img = request.files['photo']
    	img_name = secure_filename(img.filename)
    	create_new_folder(app.config['UPLOAD_FOLDER'])
    	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
	img.save(saved_path)


#	filename = request.files['photo']
#       filename = photos.save(request.files['photo'])
#       destination = "/".join([target, filename])
#       print("Accept incoming file:", filename)
#       print(destination)
#       file.save(destination)   


#        filename = photos.save(request.files['photo'])
#	print "Filename",filename
#	print request.files
        return render_template('uploadTest.html')
    return render_template('uploadTest.html')




@app.route('/newRegistration', methods=['GET' , 'POST'])
def showRegistrationFormSelector(): 
    if session.get('logged_in') and session.get('userName') == "admin":
	return render_template('newRegsiterPage.html', types = typeList , cssName="agency.min.css")	
    else:
	return redirect(url_for("login"), code=302)	


@app.route('/<scheme>/newRegistration', methods=['GET' , 'POST'])
def showRegistrationForm(scheme): 
    if variableFound(scheme):
                print "redirecting"
                return redirect("/newRegistration", code=302)
    cssName = cssChecker(scheme)
    print cssName
    userCollection,_,cardPassCollection = collectionNameGetter(scheme)
    print userCollection
    if session.get('logged_in') and session.get('userName') == "admin":
        if request.method == 'POST':
		cardId = request.form['cardId']
		userId = request.form['name']
		shortMessage = request.form['shortMessage']
		print request.files
		try:
			img = request.files['file-input']
			imageData = request.form['croppedImage']	
			print "Image" , img
			#img_name = secure_filename(img.filename)
			img_name = cardId + str(secure_filename(img.filename))
			create_new_folder(app.config['UPLOAD_FOLDER'])
			saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
	#        	img.save(saved_path)
			convert_and_save(imageData,saved_path)
			imageUrl = "/uploads/" + img_name
		except:
			imageUrl = ""
		userName = request.form['snapchatUserName']
		userName,userType = userNameGetter(scheme,userName.strip())
		if userName == 0:
                        flash("Inavlid " + scheme + " ID","#ff0000")
			return render_template('userAddForm.html', status = "Inavlid " + scheme + " ID" , cssName=cssName , scheme = scheme)
		
	  	collection = db[userCollection]
		userInfo = collection.find({"id" : cardId.strip()})
		if userInfo.count() == 0:

			if scheme == "youtube":
				contentType = request.form['contentType']
				if contentType == "Video":
					newScheme = scheme + "Video"
				elif contentType == "Channel":
                                        newScheme = scheme + "Channel"
				elif contentType == "User":
                                        newScheme = scheme + "User"
				browserUrl,iPhoneUrl,androidUrl = urlGetter(newScheme,userName.strip(),userType)
			else:
				browserUrl,iPhoneUrl,androidUrl = urlGetter(scheme,userName.strip(),userType)
			randomPassword = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))
			print randomPassword
			cardPassword = encode(encryption,randomPassword)
			idEncoded = encode(encryption,cardId.strip())
			cardPassCollection = db[cardPassCollection]
			cardPassCollection.insert({"id" : idEncoded,"password" : cardPassword})
			cardPasswordHash = generate_password_hash(randomPassword)
			insertData = {
					"id" : cardId.strip(),
					"name" : userId.strip(),
					"imageUrl" : imageUrl.strip(),
					"shortDesc" : shortMessage.strip(),
					"iPhoneLink" : iPhoneUrl,
					"androidLink" : androidUrl,
					"browserLink" : browserUrl,
					"state" : "active",
					"password" : cardPasswordHash

				     }
			collection.insert(insertData)
			if scheme == "youtube":
				flash("User Added Successfully","#00ff00")
				return render_template('userAddForm.html', status = "User Added Successfully" , cssName=cssName , scheme = scheme , ftype = "youtube")	
			flash("User Added Successfully","#00ff00")
			return render_template('userAddForm.html', status = "User Added Successfully" , cssName=cssName , scheme = scheme)	
		else:
			if scheme == "youtube":
                                return render_template('userAddForm.html', status = "User Already registered" , cssName=cssName , scheme = scheme , ftype = "youtube")
				flash("User Added Successfully","#00ff00")
			flash("User Added Successfully","#00ff00")
			return render_template('userAddForm.html', status = "User Already registered" , cssName=cssName , scheme = scheme)
	
	else:
		if scheme == "youtube":
			return render_template('userAddForm.html' , cssName=cssName,  scheme = scheme , ftype = "youtube")
		else:		
			return render_template('userAddForm.html' , cssName=cssName,  scheme = scheme)
    else:
	return redirect(url_for("login"), code=302)

@app.route('/everything', methods=['GET', 'POST'])
def testEverything():
	return render_template('everything.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('logged_in'):
	session['logged_in'] = False
	session['cardLogin'] = False
	session['cardID'] = ""
	return redirect(url_for("login"), code=302)
#        return render_template('loginPage.html')
    else:
	return redirect(url_for("login"), code=302)



@app.route('/login', methods=['GET', 'POST'])
def login():
    print "IN LOGIN"
    print session.get('logged_in')
    if not session.get('logged_in'):
	    print "IN LOGIN 1"
	    if request.method == 'POST':
		print "IN LOGIN 2"
		username = request.form['userName']
		password = request.form['password'] 
		collection = db['snapLoginData']
		userInfo = collection.find({"userName" : username.strip()})
		if userInfo.count() == 0:
			flash("No such user registered","#ff0000")
			return render_template('loginPage.html',status = "No such user registered" , cssName="agency.min.css")
		else:
			userInfo = userInfo[0]
			if check_password_hash(userInfo['password'], password.strip()):
				session['logged_in'] = True
				session['userName'] = username.strip()
				return redirect('/newRegistration', code=302)
			else:
				flash("Invalid password","#ff0000")
				return render_template('loginPage.html',status = "Invalid password", cssName="agency.min.css")
			

		return render_template('loginPage.html',status = "\n                      ", cssName="agency.min.css")
	    else:
		return render_template('loginPage.html',status = "\n                      ", cssName="agency.min.css")
    else:
        return redirect('/', code=302)




@app.route('/<scheme>/<variable>/admin/stats/', methods=['GET'])
def showUserTrackData(variable,scheme):
    if session.get('cardID') == variable.strip():
        pass
    else:
        session['cardLogin'] = False
        session['cardID'] = None
    if session.get('cardLogin'):

	    if variableFound(scheme):
			print "redirecting"
			return redirect("/"+scheme.strip(), code=302)
	    cssName = cssChecker(scheme)
	    userCollection,trackCollection,_ = collectionNameGetter(scheme)

	    hitsOneHour = 0
	    hitsTwentyFourHour = 0
	    hitsSevenDays = 0
	    hitsThirtyDays = 0
	    hitsAndroid = 0
	    hitsIPhone = 0
	    hitsBrowser = 0
	    collection = db[userCollection]
	    userInfo = collection.find({"id" : variable})
	    
	    if userInfo.count() == 0:
		image = logoImageGetter(scheme)
		return render_template('invalidId.html' , cssName=cssName, imageUrl = "/uploads/" + image)
	
	
	    collection = db[trackCollection]
	    userTrackingData = collection.find({"userID" : variable}).sort("timestamp" ,pymongo.DESCENDING)
	    timeOneHour = int((datetime.datetime.now() - datetime.timedelta(hours = 1)).strftime('%s'))
	    timeTwentyFourHour = int((datetime.datetime.now() - datetime.timedelta(hours = 24)).strftime('%s'))
	    timeSevenDays = int((datetime.datetime.now() - datetime.timedelta(days = 7)).strftime('%s'))
	    timeThirtyDays = int((datetime.datetime.now() - datetime.timedelta(days = 30)).strftime('%s'))
	    currentTime = int(datetime.datetime.now().strftime('%s'))
	    try:
	    	lastTime = userTrackingData[userTrackingData.count() -1]['timestamp']
	    except:
		lastTime = currentTime
	    timeList = []
	    while lastTime < currentTime:
		  timeList.append(lastTime)
		  lastTime = int((datetime.datetime.fromtimestamp(lastTime) + datetime.timedelta(minutes = 15)).strftime('%s'))
	    timeList.append(currentTime)
	    timeCount = 0
	    hitCount = 0
            timeList = timeList[::-1]
	    upper = timeList[timeCount]
	    try:
	    	lower = timeList[timeCount + 1]
	    except:
		lower = upper
	    allData = []
	    countList = []
	    for data in userTrackingData:
		
		if data['timestamp'] > timeOneHour:
			print data['timestamp'] > timeOneHour
			print data['timestamp']
			print timeOneHour
			hitsOneHour = hitsOneHour + 1
		if data['timestamp'] > timeTwentyFourHour:
			hitsTwentyFourHour = hitsTwentyFourHour + 1
		if data['timestamp'] > hitsSevenDays:
			hitsSevenDays = hitsSevenDays + 1
		if data['timestamp'] > hitsThirtyDays:
			hitsThirtyDays = hitsThirtyDays + 1
		if data['userType'] == "android":
			hitsAndroid = hitsAndroid + 1
		elif data['userType'] == "iPhone":
			hitsIPhone = hitsIPhone + 1
		else:
			hitsBrowser = hitsBrowser + 1 
		del data["_id"]
		allData.append(data)
		status = 1
	        while status == 1:
		    if data['timestamp'] <= upper and data['timestamp'] >= lower:
 			hitCount = hitCount + 1
			status = 2
			if data['timestamp'] == lower:
				countList.append(hitCount)
		    else:
			countList.append(hitCount)
			timeCount = timeCount + 1
			try:
				upper = timeList[timeCount]
				lower = timeList[timeCount + 1]
			except:
				countList.append(0)
				status = 2
			hitCount = 0

	    
	    returnData = {
		"dataJson" : allData,
		"hitsOneHour" : hitsOneHour,
		"hitsTwentyFourHour" : hitsTwentyFourHour,
		"hitsSevenDays" : hitsSevenDays,
		"hitsThirtyDays" : hitsThirtyDays,
		"hitsIPhone" : hitsIPhone,
		"hitsAndroid" : hitsAndroid,
		"hitsBrowser" : hitsBrowser
			 }
	    usageData = [
			{ "y": hitsAndroid, "label": "Android" ,"color" : "#a4c639"},
			{ "y": hitsIPhone, "label": "iPhone" ,"color" : "#a6b1b7"},
			{ "y": hitsBrowser, "label": "Personal Computer" ,"color" : "#f35022"},
			]
	    print countList
	    print len(timeList)
	    print len(countList)
	    timeListPerHour = []
	    perHourData = []
	    perHourCount = 0
	    for count in range(len(countList)):
		if count%4 == 3:
			timeListPerHour.append(timeList[count + 1])
			perHourCount = perHourCount + countList[count]
			perHourData.append(perHourCount)
			perHourCount = 0
		else:
			perHourCount = perHourCount + countList[count]
	    print perHourData
	    print timeListPerHour	
	    print len(perHourData)
	    print len(timeListPerHour)	

	    timeListPerDay = []
            perDayData = []
            perDayCount = 0
            for count in range(len(perHourData)):
                if count%24 == 23:
                        timeListPerDay.append(timeListPerHour[count])
                        perDayCount = perDayCount + perHourData[count]
                        perDayData.append(perDayCount)
                        perDayCount = 0
                else:
                        perDayCount = perDayCount + perHourData[count]
            print perDayData
            print timeListPerDay

	    timeListPerWeek = []
            perWeekData = []
            perWeekCount = 0
            for count in range(len(perDayData)):
                if count%7 == 6:
                        timeListPerWeek.append(timeListPerDay[count])
                        perWeekCount = perWeekCount + perDayData[count]
                        perWeekData.append(perWeekCount)
                        perWeekCount = 0
                else:
                        perWeekCount = perWeekCount + perDayData[count]
            print perWeekData
            print timeListPerWeek
	    print "EXPERIMENT START"
	    hTl,hDl = getPerIntervalData(timeList,countList,"hour") 
	    dTl,dDl = getPerIntervalData(hTl,hDl,"day") 
	    wTl,wDl = getPerIntervalData(dTl,dDl,"week") 
	    mTl,mDl = getPerIntervalData(wTl,wDl,"month")
	    print hTl,hDl
	    print dTl,dDl
            print wTl,wDl
            print mTl,mDl 
	    



	    print "EXPERIMENT END"
	    sendData = []
	    for dataNumber in range(len(hTl)):
		sendData.append({"x" : datetime.datetime.fromtimestamp(hTl[dataNumber]).strftime('%Y-%m-%dT%H:%M:%S') , "y" : hDl[dataNumber]})
	    
	    print sendData
	    print returnData
  	    legend = 'User Interaction Data'
            labels = timeList
            values = countList
	    cssName = cssChecker(scheme)
            return render_template('statsPage.html',cssName=cssName, values=values, labels=labels, legend=legend, sendData = sendData, usageData = usageData, returnData = returnData,manage = True, manageLink = "/" + scheme.strip() + "/" + variable.strip() + "/admin", buttonText = "UPDATE" , scheme = scheme , cardID = variable.strip())

	    return jsonify(returnData)
    else:
	    return redirect("/"+scheme.strip() + "/" + variable + "/admin", code=302)

def getPerIntervalData(timeList,countList,interval):
    timeListPerInterval = []
    perIntervalData = []
    perIntervalCount = 0
    if interval == "hour":
	div = 4
	rem = 3
    if interval == "day":
	div = 24
	rem = 3
    if interval == "week":
	div = 7
	rem = 6
    if interval == "month":
	div = 30
	rem = 29
    print len(countList) 
    for count in range(len(countList)):
	if count%div == rem:
		if interval == "hour":
			timeListPerInterval.append(timeList[count + 1])
		else:
			timeListPerInterval.append(timeList[count])

		perIntervalCount = perIntervalCount + countList[count]
		perIntervalData.append(perIntervalCount)
		perIntervalCount = 0
	else:
		perIntervalCount = perIntervalCount + countList[count]
    if perIntervalData == [] and timeListPerInterval == []:
	print "EMPTY"
	try:
		timeListPerInterval.append(timeList[count])
		perIntervalData.append(perIntervalCount)
	except:
		pass
    return timeListPerInterval,perIntervalData


@app.route('/', methods=['GET'])
def showHomePage():
	return render_template('mainPage.html',name = "Canatech",imageUrl = "/uploads/logo.png",appLink = "Buy Here" , browserLink = "Buy NOw", description = "Eco friendly connecting solutions" , cssName="agency.min.css",buttonText = "Buy now")



@app.route('/uploads/<path:path>')
def send_uploads(path):
    return send_from_directory('uploads', path)
	


@app.route('/<variable>/', methods=['GET'])
def showHomeData(variable):
	print variableFound(variable)
	if variableFound(variable):
		print "redirecting"
		return redirect("/", code=302)	
	else:	
		cssName = cssChecker(variable)
		image = logoImageGetter(variable)	
		return render_template('mainPage.html',name = "Canatech",imageUrl = "/uploads/" + image,appLink = "Buy Here" , browserLink = "Buy NOw", description = "Social media cards" , cssName=cssName , buttonText = "Buy now")



@app.route('/<scheme>/cardSettings', methods=['GET','POST'])
def showCardSettingsPage(scheme):
   cardID = session.get('cardID')
   if session.get('cardLogin'):
	if variableFound(scheme):
		print "redirecting"
		return redirect("/"+scheme.strip(), code=302)
	cssName = cssChecker(scheme)
        userCollection,trackCollection,_ = collectionNameGetter(scheme)
        collection = db[userCollection]
        userInfo = collection.find({"id" : cardID})
        if userInfo.count() == 0:
            image = logoImageGetter(scheme)
            return render_template('invalidId.html' , cssName=cssName, imageUrl = "/uploads/" + image)
        userInfo = userInfo[0]
        if request.method == 'POST':
		userId = request.form['name']
                shortMessage = request.form['shortMessage']
		if len(request.files) == 0:
			imageUrl = request.form['imageContain']
		else:
			img = request.files['file-input']
			imageData = request.form['croppedImage']
			#img_name = secure_filename(img.filename)
#			img_name = cardID + str(secure_filename(cardID + ".png"))
			img_name = cardID + str(secure_filename(img.filename))
			create_new_folder(app.config['UPLOAD_FOLDER'])
			saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
	#               img.save(saved_path)
			convert_and_save(imageData,saved_path)
			imageUrl = "/uploads/" + img_name
                userName = request.form['snapchatUserName']
		userNameOld = userName
                userName,userType = userNameGetter(scheme,userName.strip())
		if userName == 0:
			flash("Inavlid " + scheme + " ID","#ff0000")
			return render_template('cardSettings.html',scheme = scheme, cssName=cssName ,buttonText = "ACTIVATE CARD" ,cardID = cardID,name = userId.strip(),imageUrl = imageUrl.strip(),shortDesc = shortMessage.strip(),userName = userNameOld,status = "Inavlid " + scheme + " ID")
		if scheme == "youtube":
				
                                contentType = request.form['contentType']
                                if contentType == "Video":
                                        newScheme = scheme + "Video"
                                elif contentType == "Channel":
                                        newScheme = scheme + "Channel"
                                elif contentType == "User":
                                        newScheme = scheme + "User"
                                browserUrl,iPhoneUrl,androidUrl = urlGetter(newScheme,userName.strip(),userType)
		else:
                                browserUrl,iPhoneUrl,androidUrl = urlGetter(scheme,userName.strip(),userType)
		updateData = {
                                        "name" : userId.strip(),
                                        "imageUrl" : imageUrl.strip(),
                                        "shortDesc" : shortMessage.strip(),
                                        "iPhoneLink" : iPhoneUrl,
                                        "androidLink" : androidUrl,
                                        "browserLink" : browserUrl,
                                        "state" : "active",

                                     }
		collection.update({"id" : cardID},{"$set" : updateData})
		buttonText = "UPDATE CARD"
		if userInfo["state"] == "active":
			flash("Card Updated successfully","#00ff00")
			statusText = "Card Updated successfully"
		else:
			flash("Card Activated successfully","#00ff00")
			statusText = "Card Activated successfully" 
		if scheme == "youtube":
                        return render_template('cardSettings.html',scheme = scheme, cssName=cssName ,buttonText = buttonText,cardID = cardID,name = updateData["name"],imageUrl = imageUrl.strip(),shortDesc = updateData["shortDesc"],userName = userName,ftype = "youtube",status = statusText,contentType = contentType, stats = True,statsLink = "/" + scheme.strip() + "/" + cardID.strip() + "/admin/stats/")
                else:
                        return render_template('cardSettings.html',scheme = scheme, cssName=cssName ,buttonText = buttonText,cardID = cardID,name = updateData["name"],imageUrl = imageUrl.strip(),shortDesc = updateData["shortDesc"],userName = userName,status = statusText, stats = True,statsLink = "/" + scheme.strip() + "/" + cardID.strip() + "/admin/stats/")

	else:
		name = userInfo["name"]
		imageUrl = userInfo["imageUrl"]
		shortDesc = userInfo["shortDesc"]
		url = userInfo["browserLink"]
		if url.strip() == "":
			userName = ""
		else:	
			print url
			if scheme == "youtube":
				contentType = getYouTubeContentType(url)
				print "Content type" , contentType
				newScheme = scheme + contentType
				userName = getNameFromUrl(newScheme,url)
			else:
				userName = getNameFromUrl(scheme,url)
		try:
			if userInfo["state"] == "inactive":
				buttonText = "ACTIVATE CARD"
				status = "Card not activated"
			elif userInfo["state"] == "active":
				buttonText = "UPDATE CARD"
				status = "Card already activated"
		except:
			status = "Card already activated"
			buttonText = "UPDATE CARD"
		if scheme == "youtube":
			contentType = getYouTubeContentType(url)
			return render_template('cardSettings.html',scheme = scheme, cssName=cssName ,buttonText = buttonText,cardID = cardID,name = name,imageUrl = imageUrl,shortDesc = shortDesc,userName = userName,ftype = "youtube",status = status,contentType = contentType, stats = True,statsLink = "/" + scheme.strip() + "/" + cardID.strip() + "/admin/stats/")
		else:	
			return render_template('cardSettings.html',scheme = scheme, cssName=cssName ,buttonText = buttonText,cardID = cardID,name = name,imageUrl = imageUrl,shortDesc = shortDesc,userName = userName,status = status, stats = True,statsLink = "/" + scheme.strip() + "/" + cardID.strip() + "/admin/stats/")
	
   else:
	try:
		return redirect("/"+scheme.strip() + "/" + cardID + "/admin", code=302)
	except:
		return redirect("/"+scheme.strip()  , code=302)


@app.route('/<scheme>/<variable>/admin/', methods=['GET','POST'])
def showUserAdminPage(variable,scheme):
    if session.get('cardID') == variable.strip():
	pass
    else:
	session['cardLogin'] = False
	session['cardID'] = None
    if not session.get('cardLogin'):
	    if variableFound(scheme):
			print "redirecting"
			return redirect("/"+scheme.strip(), code=302)
	    cssName = cssChecker(scheme)
	    userCollection,trackCollection,_ = collectionNameGetter(scheme)
	    collection = db[userCollection]
	    userInfo = collection.find({"id" : variable})
            image = logoImageGetter(scheme)
	    if userInfo.count() == 0:
                image = logoImageGetter(scheme)
                return render_template('invalidId.html' , cssName=cssName, imageUrl = "/uploads/" + image)
	    userInfo = userInfo[0]
	    try:
		if userInfo["state"] == "inactive":
			buttonText = "ACTIVATE CARD"
			status = "Card not Activated"
		elif userInfo["state"] == "active":
			status = "Card already Activated"
			buttonText = "UPDATE CARD"
	    except:
		buttonText = "UPDATE CARD"
	 
	    if request.method == 'POST':	
		password = request.form['password']			
		if check_password_hash(userInfo['password'], password.strip()):
                                session['cardLogin'] = True
                                session['cardID'] = variable
                                return redirect( '/' + scheme.strip() + '/cardSettings', code=302)
		else:
				flash("Invalid Password","#ff0000")
                                return render_template('cardAdminPage.html',status = "Invalid password",buttonText = buttonText,cssName = cssName,cardID = variable,scheme = scheme.strip(), imageUrl = "/uploads/" + image)
	    else:
		return render_template('cardAdminPage.html',buttonText = buttonText,cssName = cssName,cardID = variable,scheme = scheme.strip(),status = status, imageUrl = "/uploads/" + image)
	    return render_template("cardAdminPage.html",buttonText = buttonText,cssName = cssName,cardID = variable,scheme = scheme.strip() , status = status, imageUrl = "/uploads/" + image)	
    else:
	    return redirect('/' + scheme.strip() + '/cardSettings', code=302)






@app.route('/<scheme>/<variable>/', methods=['GET'])
def showUserData(variable,scheme):
    if variableFound(scheme):
                print "redirecting"
                return redirect("/"+scheme.strip(), code=302)
    cssName = cssChecker(scheme)
    userCollection,trackCollection,_ = collectionNameGetter(scheme)
    print request.remote_addr
    print request.headers
    agent = request.headers.get('User-Agent')
    referer = request.headers.get('Referer')
    timestamp = int(datetime.datetime.now().strftime('%s'))	
    geoStats = requests.get("http://freegeoip.net/json/" + request.remote_addr.strip())
    geoJson = json.loads(geoStats.content)

    collection = db[userCollection]
    userInfo = collection.find({"id" : variable})
    if userInfo.count() == 0:
	image = logoImageGetter(scheme)
	return render_template('invalidId.html' , cssName=cssName, imageUrl = "/uploads/" + image)

    session['cardLogin'] = False
    session['cardID'] = None
    userInfo = userInfo[0]
    try:
	if userInfo["state"] == "inactive":
		return redirect("/" + scheme.strip() + "/" + variable.strip() + "/admin", code=302)	
    except:
	pass
	    
    if ('android') in agent.lower():
	openInAppLink = userInfo['androidLink']
	userType = "android"
    elif ('iphone') in agent.lower() or ('ipad') in agent.lower():   
	openInAppLink = userInfo['iPhoneLink']
	userType = "iPhone"
    else:
        openInAppLink = userInfo['browserLink']
 	userType = "computer"
    
    trackingData = {
                "userID" : variable,
		"referer" : referer,
		"timestamp" : timestamp,
		"geoStats" : geoJson,
		"remoteIp" : request.remote_addr.strip(),
		"userType" : userType,
		   }
    print trackingData
    print schemeUsageTypeGetter(scheme)
    if schemeUsageTypeGetter(scheme) == 0:
	print "SINGLE"
	utype = "single"
    else:
	print "DUAL"
	utype = "dual"
    buttonText = schemeUsageTextGetter(scheme,userInfo['browserLink'])
    trackingCollection = db[trackCollection]
    trackingCollection.insert(trackingData)
    return render_template('mainPage.html',name = userInfo['name'],imageUrl = userInfo['imageUrl'],appLink = openInAppLink , browserLink = userInfo['browserLink'], description = userInfo['shortDesc'], cssName=cssName, utype = utype, manage = True, manageLink = "/" + scheme.strip() + "/" + variable.strip() + "/admin",buttonText = buttonText )


