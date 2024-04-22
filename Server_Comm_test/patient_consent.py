'''
This code is to implement the central server
'''

from flask import Flask, jsonify, request
import time
import requests
import pprint
import json
import string
import random

file_name = 'patients.json'

waiting_time = 20

def get_data_from_json(hash_id, hospital):
    with open(file_name, "r") as file:
        data = json.load(file)
        pat_data = data["patients"]
        
    for each_patient in pat_data:
        print(".")
        if(each_patient["name"] == hash_id):
            each_patient["hospital"] = hospital
            print("Dataaaa : ", data)
            with open(file_name, "w") as file:
                json.dump(data, file)
    
    time.sleep(waiting_time)    # in this time patient has to give access
    
    with open(file_name, "r") as file:
        data = json.load(file)
        pat_data = data["patients"]
    
    msg = "error"
    for each_patient in pat_data:
        if(each_patient["name"] == hash_id and each_patient["hospital"] == hospital):
            each_patient["hospital"] = ""
            if(each_patient["permission"] == 0):
                msg = "permission not given"
                break
            else:
                msg = each_patient["consent_id"]
                each_patient["permission"] = 0
    
    with open(file_name, "w") as file:
        json.dump(data, file)
    return msg

def store_data_to_json(dictionary):
    with open(file_name, "r") as file:
        data = json.load(file)["patients"]
    
    print("-------- FILE Access Ok ----------")
    flag = 0
    for each_patient in data :
        if(dictionary["name"] == each_patient["name"]):
            flag = 1
    if(flag != 1):
        data.append(dictionary)
        
    new_data = {"patients" : data}
        
    print(new_data)
    with open(file_name, "w") as file:
        json.dump(new_data, file)

def generate_token():
    length = 5
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def update_permission(name, perm):
    
    return_val = "Error"
    with open(file_name, "r") as file:
        data = json.load(file)["patients"]
        
    for each_patient in data:
        if(each_patient["name"] == name):
            each_patient["permission"] = perm
            return_val = "permission_granted"
    new_data = {"patients" : data}
    with open(file_name, "w") as file:
        json.dump(new_data, file) 
    return return_val

app = Flask(__name__)

@app.route('/retrive-consent', methods=['GET'])
def retrive_consent():
    name = request.args.get('name')
    hospital = request.args.get('hospital')
    
    data = get_data_from_json(name, hospital)
    return data

@app.route('/share-consent', methods=['GET'])
def share_consent():
    name = request.args.get('name')
    hospital = request.args.get('hospital')
    permission = 0
    consent_id = generate_token()
    
    patient = {
        "name" : name,
        "hospital" : hospital,
        "permission" : permission,
        "consent_id" : consent_id
    }
    
    
    store_data_to_json(patient)
    print("------------OK-------------")
    data = get_data_from_json(name, hospital)
    return data
    
@app.route('/check-request', methods=['GET'])
def check_requests():
    name = request.args.get("name")
    with open(file_name, "r") as file:
        data = json.load(file)["patients"]
    
    for each_patient in data:
        if(each_patient["name"] == name):
            return each_patient["hospital"]
    
    return "No requests"

@app.route('/give-consent', methods=['GET'])
def give_consent():
    name = request.args.get("name")
    permission = request.args.get("permission")
    if(permission == "0"):
        permission = 0
    else:
        permission = 1
    
    return update_permission(name, permission)

if __name__ == '__main__':
    app.run(port=9000, debug=True)