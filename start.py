from flask import Flask
from auth import auth
from database import createDatabase
def createWebApp():
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.run()

#Database is only created if it doesn't exist already
createDatabase()
createWebApp()

