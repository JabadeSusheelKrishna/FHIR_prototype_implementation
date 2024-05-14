
import time
from flask import Flask, jsonify, request
import requests
import json
import random
import string
from datetime import datetime
from flask_cors import CORS

central_server_port = 5050

app = Flask(__name__)
CORS(app)

hospitals = {}
with open("accounts.json", "r") as file:
    data_formed = json.load(file)["accounts"]
for each_entry in data_formed:
    hospitals[each_entry["username"]] = [each_entry["port"], each_entry["IP_Address"]]

def generate_token():
    length = 10
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_requests_to_other_ids(current_id, name):
    '''
    Sends the GET request to other servers
    '''     
    responses = {}
    count = 0
    print(hospitals)
    for id in hospitals:
        if str(hospitals[id][1]) != current_id:
            url = hospitals[id][1] + "/patient-details"
            print("Request sent to : ", url)
            try:
                response = requests.get(url, params={'name':{name}})
                responses[count] = response.json()
                count += 1
            except requests.exceptions.RequestException as e:
                responses[count] = str(e)
                count += 1
    return responses

@app.route('/get-details', methods=['GET'])
def handle_request():
    time.sleep(1)  # Simulating some processing time
    print(f"Received request with ID: {request.args.get('id')}")

    name = request.args.get('patient')
    hospital_id = request.args.get('id')    # IP_ADDRESS
    username = request.args.get('username')
    token = request.args.get('access_token')
    
    with open("accounts.json", "r") as file:
        data_f = json.load(file)["accounts"]
    
    permission_got = 0
    for each_entry in data_f : 
        if(username == each_entry["username"] and token == each_entry["token"]):
            permission_got = 1  # Verified Access Token
    if(permission_got):
        responses = send_requests_to_other_ids(hospital_id, name)
        return jsonify(responses)
    else:
        return "No Authorization. Please Login and Paste the correct token"

@app.route('/register', methods=['POST', 'GET'])
def registeration():
    username = request.args.get('username')
    password = request.args.get('password')
    port_number = request.args.get('port')
    ip_address = request.args.get('ip_address')
    
    user_credentials = {
        "username" : username, 
        "password" : password, 
        "port" : port_number, 
        "last_login" : "NONE", 
        "token" : "NONE",
        "IP_Address" : ip_address
        }

    # Reading data
    with open('accounts.json', 'r') as file:
        print("Hello")
        data = json.load(file)
        
    # Storing in Memory for faster access.
    hospitals[username] = [port_number, ip_address]     # Storing Port and IP Address
    
    if username in [user['username'] for user in data["accounts"]]:
        return "Data Already Exists, Please Proceed Loggin in"
    else:
        data["accounts"].append(user_credentials)
        with open('accounts.json', 'w') as file:
            json.dump(data, file)       # Storing Registration Data
    return "Successfully registered\n"

@app.route('/login', methods=['POST'])
def login():
    headers = request.headers
    username = headers.get('username')
    password = headers.get('password')
    
    with open('accounts.json', 'r') as file:
        data = json.load(file)
    
    for user in data["accounts"]:
        if(user["username"] == username):
            if(user["password"] == password):
                if(user["last_login"] == "NONE"):   # can add dynamic Tokens
                    user["last_login"] = datetime.now().strftime("%H:%M:%S")
                    user["token"] = generate_token()
                    with open('accounts.json', 'w') as file:
                        json.dump(data, file)
                return user["token"]
            else:
                return "-:[ERROR1]:- Incorrect Credentials!!! Please try again"
    return "-:[ERROR2]:- Account Not Found! Please register Again"

if __name__ == '__main__':
    app.run(port=central_server_port, host='0.0.0.0', debug=True)
