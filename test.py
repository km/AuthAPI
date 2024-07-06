import requests
import json
#Use this to test the api endpoints

email = input("Input email to register: ")
password = input("Input password to register: ")
name = input("Input name to register: ")

regjson = {"email": email, "name": name, "password": password}
print("Request data to be sent: ", regjson)

regReq = requests.post(url='http://127.0.0.1:5000/register', json=regjson)
print("Response: ", regReq.text)

print("Testing login...")
logjson = {"email": email, "password": password}

print("Request data to be sent: ", logjson)

logreq = requests.post(url='http://127.0.0.1:5000/login', json=regjson)
print("Response: ", logreq.text)

print("Testing logout...")
logreqjson = json.loads(logreq.text)
print("No data send aside from including the bearer token in the headers ", logreqjson["sessionToken"])

logoutreq = requests.get(url='http://127.0.0.1:5000/logout', headers = {"Authorization": "Bearer " + logreqjson["sessionToken"]})
print("Response: ", logoutreq.text)