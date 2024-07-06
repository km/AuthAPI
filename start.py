from flask import Flask
from auth import auth
from protected import protected
from database import createDatabase
def createWebApp():
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.register_blueprint(protected)
    app.run()

#Database is only created if it doesn't exist already
createDatabase()
createWebApp()

