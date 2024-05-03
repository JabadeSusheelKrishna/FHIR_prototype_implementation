
import time
from flask import Flask, jsonify, request
import requests
import json
import random
import string
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample list of IDs (you can replace this with your own list of IDs)
id_list = ['id1', 'id2', 'id3', 'id4', 'id5']

hospitals = {}
with open("accounts.json", "r") as file:
    data_formed = json.load(file)["accounts"]
for each_entry in data_formed:
    hospitals[each_entry["username"]] = each_entry["port"]

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
    for id in hospitals:
        # print(type(current_id))
        if str(hospitals[id]) != current_id:
            # This is where we need to send request to respective server according to ID

            url = f"http://127.0.0.1:{hospitals[id]}/patient-details"
            print("Request sent to : ", url)
            try:
                response = requests.get(url, params={'name':{name}})
                responses[count] = response.json()
                count += 1
            except requests.exceptions.RequestException as e:
                responses[count] = str(e)
                count += 1
    # print(responses[0])
    return responses

@app.route('/get-details', methods=['GET'])
def handle_request():
    time.sleep(1)  # Simulating some processing time
    print(f"Received request with ID: {request.args.get('id')}")

    name = request.args.get('patient')
    hospital_id = request.args.get('id')
    username = request.args.get('username')
    token = request.args.get('access_token')
   
    print(name, hospital_id)
    
    with open("accounts.json", "r") as file:
        data_f = json.load(file)["accounts"]
        
    print("----able to access file----")
     
    permission_got = 0   
    for each_entry in data_f : 
        print("Actual : ",each_entry["username"], each_entry["token"])
        print("given in : ", username, token)
        if(username == each_entry["username"] and token == each_entry["token"]):
            permission_got = 1
    # Send requests to all other IDs
    if(permission_got):
        print("Sending the Response :::::::: ")
        responses = send_requests_to_other_ids(hospital_id, name)
        return jsonify(responses)
    else:
        return "No Authorization. Please Login and Paste the correct token"
    # return "Hello"

@app.route('/register', methods=['POST'])
def registeration():
    print("hello world")
    headers = request.json
    username = headers.get('username')
    password = headers.get('password')
    port_number = headers.get('port')
    user_credentials = {
        "username" : username, 
        "password" : password, 
        "port" : port_number, 
        "last_login" : "NONE", 
        "token" : "NONE"
        }

    # Reading data
    with open('accounts.json', 'r') as file:
        print("Hello")
        data = json.load(file)
    # Storing in Memory for faster access.
    hospitals[username] = port_number
    print("Hospitals Dictionary : ", hospitals)

    if username in [user['username'] for user in data["accounts"]]:
        return "Data Already Exists, Please Proceed Loggin in"
    else:
        data["accounts"].append(user_credentials)
        print(data)
        with open('accounts.json', 'w') as file:
            json.dump(data, file)
    return "Successfully registered\n"

@app.route('/login', methods=['POST'])
def login():
    headers = request.json
    print("Headers : ",headers)
    username = headers.get('username')
    password = headers.get('password')
    
    # # Reading data
    with open('accounts.json', 'r') as file:
        data = json.load(file)
    
    for user in data["accounts"]:
        if(user["username"] == username):
            if(user["password"] == password):
                if(user["last_login"] == "NONE"):
                    user["last_login"] = datetime.now().strftime("%H:%M:%S")
                    user["token"] = generate_token()
                    with open('accounts.json', 'w') as file:
                        json.dump(data, file)
                print(user["token"])
                return {"aa":user["token"]}
            else:
                return "-:[ERROR1]:- Incorrect Credentials!!! Please try again"
    return "-:[ERROR2]:- Account Not Found! Please register Again"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
