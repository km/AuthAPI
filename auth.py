from flask import Blueprint, request
from utilities import checkData

auth = Blueprint('auth', __name__)


#Endpoint for registering, if it isn't a post request, flask automatically returns a 405.
#The JSON format is {"name": name, "email": email, "password": ""}
#Restrictions are for the email to not have been signed up before and be valid, and the length constraints in the config.json for name & password

@auth.post('/register')
def register():
    #Only accept json
    if(request.is_json):
        
        #Checks data according to constraints
        dataValidity = checkData(request.get_json())
        if(dataValidity != ""):
            return {"error": dataValidity}, 422
        else:
            #Register into database and return success
            return {"Success": "User succesfully registered"}, 201

    else:
        return {"error": "JSON accepted only"}, 415