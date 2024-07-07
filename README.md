# AuthAPI

AuthAPI is a Python-based authentication API, built using flask, that provides user registration, login, and token-based authentication functionalities. The API uses a local sqlite database to store user info, and bcrypt to encrypt passswords.

## Table of Contents

- [Prerequisites](#Prerequisites)
- [Installation](#Installation)
- [Usage](#Usage)
- [API Endpoints](#Endpoints)


## Prerequisites
Ensure you have the following installed:

- Python 3.8+
- Flask
- Bcrypt
- PyJWT
- Requests

## Installation

1. Clone/download the respository
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Configure:
  Customize the API by changing ```config.json```

## Configuration
You can configure the API from config.json
- `minPasswordLength` is the minimum length of the password, default is 8.
- `maxPasswordLength` is the maximum length of the password, default is 128.
- `minNameLength` is the minimum length of the name, default is 2.
- `maxNameLength` is the maximum length of the name, default is 64.
- `sessionExpiryTime` is the time in seconds for which a token lasts, default is 300.
- `tokenSecret` is the secret key used to formulate the jwt tokens, the longer the more secure.
 


## Usage

To start the API, run:

```
python start.py
```
Which will run the API on a local server on `http://127.0.0.1:5000`

## Endpoints
### Register
 POST endpoint for registering an account  `/register`
 ##### Payload
 `{"email": email, "password": password, "name" : name} ` JSON
##### Response
If  request is successful:
```js
{"Success": "User succesfully registered"}
```
Response Code `201`

##### Python Example
```python
regjson = {"email": email, "name": name, "password": password}
regReq = requests.post(url='http://127.0.0.1:5000/register', json=regjson)
print("Response: ", regReq.text)

```



 ### Login
 POST endpoint for logging in  `/login`
 ##### Payload
 `{"email": email, "password": password} ` JSON
##### Response
If  request is successful:
```js
{"success": "User sucessfully logged in", "sessionToken": token, "sessionExpiry": expiry}
```
Response Code `200`
- **sessionToken** is the bearer token which will be used for protected endpoint calls
- **sessionExpiry** is Unix time in seconds, for which the token will expire.

##### Python Example
```python
logjson = {"email": email, "password": password}
logreq = requests.post(url='http://127.0.0.1:5000/login', json=regjson)
print("Response: ", logreq.text)

```


### Logout
 GET endpoint for logging out  `/logout`
 ##### Headers
 `Authorization: Bearer token` where token is the sessionToken, from logging in.
##### Response
If request is successful:
```js
{"Success": "Successfully logged out"}
```
Response Code `200`
- The token is thus invalidated, and cannot be used to access protected resources.

##### Python Example
```python
logreqjson = json.loads(logreq.text)
logoutreq = requests.get(url='http://127.0.0.1:5000/logout', headers = {"Authorization": "Bearer " + logreqjson["sessionToken"]})
print("Response: ", logoutreq.text)
```

### getName
 GET protected endpoint for getting the name of a valid token  `/getName`
 ##### Headers
 `Authorization: Bearer token` where token is the sessionToken, from logging in.
##### Response
If request is successful:
```js
{"name": name}
```
Response Code `200`
- If the token is not valid or expired the endpoint will return `401`.

##### Python Example
```python
logreqjson = json.loads(logreq.text)
nameReq = requests.get(url='http://127.0.0.1:5000/getName', headers = {"Authorization": "Bearer " + logreqjson["sessionToken"]})
print("Response: ", nameReq.text)
```


## Testing
In order to test the API, you can use a tool such as Postman, or you can use the included `test.py`, which will test all the endpoints. Simply run:
```
python test.py
```
Make sure that the local server is running, for the script to work.