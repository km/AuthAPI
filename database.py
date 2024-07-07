import sqlite3
import bcrypt

#Reason every function has a different connection is because sqlite isn't thread safe and kept throwing exceptions, if I tried reusing the connection.

def createDatabase():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    #Only gets executed if the table hasn't been created
    cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT, email TEXT, currentToken TEXT)")
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
    connection.commit()
    connection.close()
    if(result != None):
        return True
    return False

#Uses bcrypt to encrypt the password
def encrypt(text):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(text.encode('utf-8'), salt)
    return hashed_password

#Checks the given credential, if they are valid returns true.
def checkCredentials(email, password):
    #Validate credentials
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    dbpassword = cursor.fetchone()
    connection.commit()
    connection.close()

    if dbpassword:
        if bcrypt.checkpw(password.encode('utf-8'), dbpassword[0]):
            #hashed password matches the given password
            return True
    
    return False

#Associates the specified token to the given email entry
def createSession(email, token):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET currentToken = ? WHERE email = ?", (token,email))
    connection.commit()
    connection.close()

#Deletes the specified token from the database, so it can't be used to access protected endpoints
def deleteToken(token):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET currentToken = ? WHERE currentToken = ?", ("",token))
    connection.commit()
    connection.close()

#Attempts to retrieve name from database, otherwise returns empty string
def retrieveName(token):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM users WHERE currentToken = ?", (token,))
    name = cursor.fetchone()
    connection.commit()
    connection.close()
    
    if(name != None):
        return name[0]
    else:
        return ''