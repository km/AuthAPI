from flask import Blueprint, request
from utilities import checkData, generateToken
import database
auth = Blueprint('auth', __name__)


#Endpoint for registering, if it isn't a post request, flask automatically returns a 405.
#The JSON format is {"name": name, "email": email, "password": ""}
#Restrictions are for the email to not have been signed up before and be valid, and the length constraints in the config.json for name & password
#Will throw an exception it fails to parse the given json.
@auth.post('/register')
def register():
    #Only accept json
    try:
        json = request.get_json()
        #Checks data according to constraints
        dataValidity = checkData(json)
        if(dataValidity != ""):
            return {"error": dataValidity}, 422
        else:
            #Register into database and return success
            try:
                database.addUser(json["name"], json["email"], json["password"])
                return {"Success": "User succesfully registered"}, 201
            except Exception as e:
                print(e)
                return {"Error": "Server error, please try again later"}, 500

    except:
        return {"Error": "JSON accepted only"}, 415


#Endpoint for logging in, requires email and password, will return a token if 
@auth.post('/login')
def login():
        #Only accept json
    try:
        json = request.get_json()
        try:
            #will throw exception if email or password arent in the json
            dataValidity = database.checkCredentials(json['email'], json['password'])
        except Exception as e:
            print(e)
            return {"error": "Missing fields"}, 422

        if(dataValidity):
            try:
                token, expiry = generateToken()
                database.createSession(json['email'], token, expiry)
                return {"success": "User sucessfully logged in", "sessionToken": token, "sessionExpiry": expiry}
            except:
                return {"error": "Server error, please try again later"}, 500

        else:
            #the password or email didnt match
            return {"error": "Invalid Credentials"}, 401

    except:
        return {"error": "JSON accepted only"}, 415
