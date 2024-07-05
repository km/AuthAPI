import sqlite3
import b

connection = sqlite3.connect("users.db")
cursor = connection.cursor()

def createDatabase():
    #Only gets executed if the table hasn't been created
    cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT, email TEXT)")

#
def addUser(name, email, password):
    hashedPassword = encrypt(password)
    cursor.execute("INSERT into users (?,?,?)", (name,email,password))

