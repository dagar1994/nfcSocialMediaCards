import base64
import random,string
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify, send_from_directory
from pymongo import MongoClient
import pymongo
import json
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import re

encryption = "Dumisani Nthanda"

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
collection = db["currentCardSeries"]

scheme = "facebook"
iterations = 10

for index in range(0,iterations):
	currentSeriesData = collection.find({"type" : scheme})
	if currentSeriesData.count() != 0:
		currentSeries = currentSeriesData[0]["currentId"]
		print currentSeries
		key = re.split('(\d+)',currentSeries)[0]
		number = int(re.split('(\d+)',currentSeries)[1])
		newID = key + str(number + 1)
		print newID	
		userCollection,_,cardPassCollection = collectionNameGetter(scheme)
		collection1 = db[userCollection]
		idData = collection1.find({"id" : newID})
		if idData.count() == 0:
			randomPassword = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))
			print randomPassword
			cardPassword = encode(encryption,randomPassword)
			idEncoded = encode(encryption,newID)
			cardPassCollection = db[cardPassCollection]
			cardPassCollection.insert({"id" : idEncoded,"password" : cardPassword})
			cardPasswordHash = generate_password_hash(randomPassword)
			insertData = {
							"id" : newID,
							"name" : "",
							"imageUrl" : "",
							"shortDesc" : "",
							"iPhoneLink" : "",
							"androidLink" : "",
							"browserLink" : "",
							"state" : "inactive",
							"password" : cardPasswordHash


						     }
			collection1.insert(insertData)
			collection.update({"type" : scheme},{"$set" : {"currentId" : newID}})

