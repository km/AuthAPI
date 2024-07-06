from flask import Blueprint, request
from utilities import checkTokenValidity
import database

#Protected endpoints that require a valid token to access
protected = Blueprint('protected', __name__)


#Gets the name associated with the session token.
@protected.get('/getName')
def getToken():
    try:
    #throws exception if there is no authorization header
        tokenheader = request.headers.get('Authorization')
        #Authorization is by bearer token
        if 'Bearer ' in tokenheader:
          token = tokenheader.split()[1] 
          if checkTokenValidity(token):
               #Token is valid will then attempt to get the name
               try:
                name = database.retrieveName(token)
                if(name != ''):
                    return {"name": name}, 200
             
               except Exception as e:
                   print(e)
                   return {"error": "Server error, please try again later."}, 500
        else:
              #Invalid Token
              return {"error": "Check authorization headers"}, 401    
    except:
        return {"error": "Check authorization headers"}, 401


    return {"error": "Invalid token"}, 401
