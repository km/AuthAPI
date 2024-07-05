import re
import json

with open("config.json", "r") as dir:
    config = json.load(dir)


def checkData(json):

    #check if email is valid using regex and not in database
    mailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(not re.fullmatch(mailRegex, json['email'])):
        return "Invalid Email"

    #check if mail in database

    #check password length
    if(len(json['password']) < config["minPasswordLength"]):
        return "Password too short, minimum " + config["maxPasswordLength"] +  " characters"
    if(len(json['password']) > config["maxPasswordLength"]):
        return "Password too long, maximum " + config["maxPasswordLength"] + " characters"


    #check name length
    if(len(json['name']) > config["maxNameLength"]):
        return "Name too long, keep under " + config["maxNameLength"] + " characters"
    if(len(json['name']) < config["minNameLength"]):
        return "Name too short, keep over " + config["minNameLength"] + " characters"
    

    #If it returns an empty string then the registeration data is valid.
    return ""
