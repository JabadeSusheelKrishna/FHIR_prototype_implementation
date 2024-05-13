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
from flask_cors import CORS

writer_url = "http://127.0.0.1:9069/json-write"

file_name = 'patients.json'

waiting_time = 30

Patients_Data = {"patients" : []}

def get_data_from_json(hash_id, hospital):
    
    print("00000------- PRESENT DATA ------000000")
    print(Patients_Data)
    print("--------------------------------------")
    
    for each_patient in Patients_Data["patients"]:
        if(each_patient["name"] == hash_id):
            each_patient["hospital"] = hospital
    
    time.sleep(waiting_time)    # in this time patient has to give access

    msg = "error"
    for each_patient in Patients_Data["patients"]:
        if(each_patient["name"] == hash_id and each_patient["hospital"] == hospital):
            each_patient["hospital"] = ""
            if(each_patient["permission"] == 0):
                msg = "permission not given"
                break
            else:
                msg = each_patient["consent_id"]
                each_patient["permission"] = 0
        elif(each_patient["name"] == hash_id):
            return "Hospital Name Not Getting Set"

    return msg

def store_data_to_json(dictionary):
    
    print("Patients Data  : ", Patients_Data)
    print("=================================")
    
    flag = 0
    for each_patient in Patients_Data["patients"] :
        if(dictionary["name"] == each_patient["name"]):
            flag = 1
    if(flag != 1):
        Patients_Data["patients"].append(dictionary)
    
    return True

def generate_token():
    length = 5
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def update_permission(name, perm):
    
    return_val = "Error"
        
    for each_patient in Patients_Data["patients"]:
        if(each_patient["name"] == name):
            each_patient["permission"] = perm
            return_val = "permission_granted"
        
    if(perm == 0):
        return_val = "Permission Not Granted"
    return return_val

app = Flask(__name__)
CORS(app)

@app.route('/retrive-consent', methods=['GET'])
def retrive_consent():
    name = request.args.get('name')
    hospital = request.args.get('hospital')
    print("----- RETRIVE CONSENT ------")
    print(name, hospital)
    
    data = get_data_from_json(name, hospital)
    return data

@app.route('/share-consent', methods=['GET'])
def share_consent():
    
    print("~~~~~~~~~~~~~~~~~~~BEFORE ASKING PERMISSION~~~~~~~~~~~~~~~~~~~~~")
    print(Patients_Data)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    # time.sleep(2)
    print("----------------------------------")
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
    data = get_data_from_json(name, hospital)
    
    print("~~~~~~~~~~~~~~~~~~~AFTER ASKING PERMISSION~~~~~~~~~~~~~~~~~~~~~")
    print(Patients_Data)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return data
    
@app.route('/check-request', methods=['GET'])
def check_requests():
    name = request.args.get("name")
    
    print("\n\n ======== CHECK REQUEST =======")
    print(Patients_Data)
    print("++++++++++ COMPLETED +++++++++++\n\n")
    
    for each_patient in Patients_Data["patients"]:
        if(each_patient["name"] == name):
            return each_patient["hospital"]
    
    return "No requests"

@app.route('/give-consent', methods=['GET'])
def give_consent():
    name = request.args.get("name")
    permission = request.args.get("permission")
    print("Permissions : ", permission)
    if(permission == "0"):
        permission = 0
    else:
        permission = 1
    
    return update_permission(name, permission)

if __name__ == '__main__':
    app.run(port=9005, host='0.0.0.0', debug=True)
