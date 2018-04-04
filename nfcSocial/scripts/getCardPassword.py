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
import re,sys

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
	else:
		return 0,0,0


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

try:
	keyword = sys.argv[1]
except:
	print "Invalid Parameters"
	sys.exit()
_,_,cardCollection = collectionNameGetter(keyword)
if cardCollection == 0:
	print "Invalid scheme"
	sys.exit()
collection = db[cardCollection]
try:
	cardID = sys.argv[2]
except:
	print "Invalid Parameters"
	sys.exit()

encodedCardID = encode(encryption, cardID)
cardData = collection.find({"id" : encodedCardID})
if cardData.count() == 0:
	print "No such card"
else:
	cardData = cardData[0]
	encodedPass = cardData["password"]
	encodedPass = encodedPass.encode("utf-8")
	decodedPass = decode(encryption,encodedPass)
	print decodedPass




