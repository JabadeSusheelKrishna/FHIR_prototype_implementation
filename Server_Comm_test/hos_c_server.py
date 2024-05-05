'''
This code is to implement the central server
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
url = "http://localhost:8002/fhir/"

def generate_hash_id(first_name, last_name, dob):
    date, year, month = dob.split("-")
    
    input_string = f"{first_name.lower()}{last_name.lower()}{date}{month}{year}"
    
    hash_object = hashlib.sha256(input_string.encode())
    hash_id = hash_object.hexdigest()
    
    return hash_id

@app.route('/give-me-hash', methods=['GET'])
def retrive_consent():
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    dob = request.args.get('dob')
    
    data = generate_hash_id(first_name=fname, last_name=lname, dob=dob)
    print("Data : ", data)
    return data

@app.route('/store-hash', methods=['GET'])
def store_in_json():
    print("Got These for me : ")
    name = request.args.get('name')
    hash = request.args.get('hash')
    
    Hash_data[hash] = name
    
    print("Added Data into Json too")
    return "Added"

@app.route('/store-hash-in-json', methods=['POST'])
def store_hasher():
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
    return jsonify(Hash_data)
    
def get_original_name(name):
    for each_hash in Hash_data:
        print(">>>> Hashes : ", each_hash)
        if(name == each_hash):
            return Hash_data[each_hash]
    return "Not Found"

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
        list_of_patients = response.json()["entry"]
    else:
        print("----- No Patient Exists -----")
    return jsonify(list_of_patients)

if __name__ == '__main__':
    app.run(port=5051, debug=True)