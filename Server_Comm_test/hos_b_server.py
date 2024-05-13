'''
This code implements the hospital server. PLease make sure the Necessary servers are running.
also have a Look at Line 19 and Line 104.
    > line 19 is the url where the FHIR local server of Hospital is ran
    > Line 104 is the port number where hospital server is gonna run
'''

from flask import Flask, jsonify, request
import time
import requests
import pprint
import hashlib
from flask_cors import CORS
import json
import time

Hash_data = {}

app = Flask(__name__)
CORS(app)
url = "http://localhost:8001/fhir/"

def generate_hash_id(first_name, last_name, dob):
    '''
    Generates a unique hash ID with first_name, last_name and Date of Birth
    '''
    date, year, month = dob.split("-")
    
    input_string = f"{first_name.lower()}{last_name.lower()}{date}{month}{year}"
    
    hash_object = hashlib.sha256(input_string.encode())
    hash_id = hash_object.hexdigest()
    
    return hash_id

@app.route('/give-me-hash', methods=['GET'])
def retrive_consent():
    '''
    gives you Hash ID when HTTP GET request is recieved to /give-me-hash
    '''
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    dob = request.args.get('dob')
    
    data = generate_hash_id(first_name=fname, last_name=lname, dob=dob)     # returns 16 charecter Hash ID
    print("Data : ", data)
    return data

@app.route('/store-hash', methods=['GET'])
def store_in_json():
    '''
    Stores the {hash : name} in the Hash_Data dictionary
    '''
    print("Got These for me : ")
    name = request.args.get('name')
    hash = request.args.get('hash')
    
    Hash_data[hash] = name              # { hash_id : name , hash_id , name }
    
    print("Added Data into Json too")
    return "Added"

@app.route('/store-hash-in-json', methods=['POST'])
def store_hasher():
    '''
    Not used for now
    '''
    if request.method == 'POST':
        data = request.get_json()
        print("Received hash:", data['hash'])
        print("Received fullname:", data['fullname'])
            
        Hash_data[data['hash']] = data['fullname']
        
        return "Hash stored successfully", 200
    else:
        return "Only POST requests are allowed", 405
    
@app.route('/print', methods=['GET'])
def print_Hash():
    '''
    Prints the data in Hash_data. ( Helpful if while debugging )
    '''
    return jsonify(Hash_data)
    
def get_original_name(name):
    '''
    retirves the Name of the patient when Hash ID is passed as input argument
    '''
    for each_hash in Hash_data:
        print(">>>> Hashes : ", each_hash)
        if(name == each_hash):
            return Hash_data[each_hash]     # returning the name
    return "Not Found"                      # if not present then return Not Found

@app.route('/patient-details', methods=['GET'])
def patient_details():
    name = request.args.get('name')
    print("--------- Request Came Successfully ----------")
    print(name)
    print("++++++++++++++++++++++++++++++++++++++++++++++")
    
    o_name = get_original_name(name)
    print("Patient Name : ", o_name)
    print("::::::::::::::::::::::::::::::::::::::::::::::")
    
    if(o_name == "Not Found"):
        return o_name
    
    print("hospital server")
    complete_url = url + "Patient?given=" + o_name + "&_include=*&_count=5&_pretty=true"

    payload = {}
    headers = {}
    
    response = requests.request("GET", complete_url, headers=headers, data=payload)
    if(response.json()["total"] > 0):
        list_of_patients = response.json()["entry"]         # Data present in FHIR
    else:
        print("----- No Patient Exists -----")
    return jsonify(list_of_patients)

if __name__ == '__main__':
    app.run(port=5052, host='0.0.0.0', debug=True)