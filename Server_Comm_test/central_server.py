
import time
from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

# Sample list of IDs (you can replace this with your own list of IDs)
id_list = ['id1', 'id2', 'id3', 'id4', 'id5']

hospitals = {
    'id2': 5052
}

hospital_count = 2      # Stores no of hospitals registered

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
   
    print(name, hospital_id)
    
    # Send requests to all other IDs
    responses = send_requests_to_other_ids(hospital_id, name)
    return jsonify(responses)
    # return "Hello"

@app.route('/register', methods=['GET'])
def registeration():
    username = request.args.get('username')
    password = request.args.get('password')
    port_number = request.args.get('port')
    
    user_credentials = {"username" : username, "password" : password, "port" : port_number}
    
    with open('accounts.json', 'r') as file:
        data = json.load(file)
    
    hospitals[username] = port_number
    print("Hospitals Dictionary : ", hospitals)
    
    if username in [user['username'] for user in data["accounts"]]:
        print("Data Already Exists, Please Proceed Further")
    else:
        data["accounts"].append(user_credentials)
        print(data)
        with open('accounts.json', 'w') as file:
            json.dump(data, file)
    return "Successfully registered\n"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
