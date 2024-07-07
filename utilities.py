import re
import json
from database import checkMail
import time
import jwt

#Load configuration
with open("config.json", "r") as dir:
    config = json.load(dir)


def checkData(json):
    #check if email is valid using regex and not in database
    try:
        mailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if(not re.fullmatch(mailRegex, json['email'])):
            return "Invalid Email"
        #check if mail in database
        if(checkMail(json['email'])):
            return "Email Already Registered"

        #check password length
        if(len(json['password']) < config["minPasswordLength"]):
            return "Password too short, minimum " + str(config["minPasswordLength"]) +  " characters"
        if(len(json['password']) > config["maxPasswordLength"]):
            return "Password too long, maximum " + str(config["maxPasswordLength"]) + " characters"

        #check name length
        if(len(json['name']) > config["maxNameLength"]):
            return "Name too long, keep under " + str(config["maxNameLength"]) + " characters"
        if(len(json['name']) < config["minNameLength"]):
            return "Name too short, keep over " + str(config["minNameLength"]) + " characters"
    except Exception as e:
     
        return "Missing fields"

    #If it returns an empty string then the registeration data is valid.
    return ""

#generates a random jwt token, and returns the current time + the expiry time from config
def generateToken():
    expiry = int(time.time() + config["sessionExpiryTime"])
    data = {"exp": expiry}
    #generates a jwt token with default HS256 encryption
    token = jwt.encode(data, config["tokenSecret"])
    return token, expiry

#Checks if token is valid and not expired
def checkTokenValidity(token):
    #Will throw exception if the token is expired or invalid
    try:
        decoded = jwt.decode(token, config["tokenSecret"], algorithms=["HS256"])
        return True
    except Exception as e:
        print(e)
        return False
    
