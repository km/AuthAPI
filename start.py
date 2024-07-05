from flask import Flask
from auth import auth

def createWebApp():
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.run()


createWebApp()

