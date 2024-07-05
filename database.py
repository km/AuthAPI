import sqlite3
import bcrypt

#Reason every function has a different connection is because sqlite isn't thread safe and kept throwing exceptions, if I tried reusing the connection.

def createDatabase():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    #Only gets executed if the table hasn't been created
    cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT, email TEXT)")
    connection.commit()
    connection.close()

#Adds a new register to the database, it encrypts the password before hand.
def addUser(name, email, password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    hashedPassword = encrypt(password)
    cursor.execute("INSERT into users (name, email, password) VALUES (?,?,?)", (name,email,hashedPassword))
    connection.commit()
    connection.close()

#checks if the email already exists in the database
def checkMail(email):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    if(result != None):
        return True
    return False

#Uses bcrypt to encrypt the password
def encrypt(text):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(text.encode('utf-8'), salt)
    return hashed_password
