'''
This code is to implement the central server
'''

from flask import Flask, jsonify, request
import time
import string
import random
from flask_cors import CORS

waiting_time = 30               # Change Waiting Time Here
patient_consent_port = 9005     # you can change this accordingly

Patients_Data = {"patients" : []}

def get_data_from_dictionary(hash_id, hospital):
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

def store_data_in_dictionary(dictionary):
    """
    Adds Data to the Dictionary
    """
    flag = 0
    for each_patient in Patients_Data["patients"] :
        if(dictionary["name"] == each_patient["name"]):
            flag = 1
    if(flag != 1):
        Patients_Data["patients"].append(dictionary)
    return True

def generate_token():
    """Generates 5 digit random consent ID which is permanent

    Returns:
        5 digit Consent ID
    """
    length = 5
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def update_permission(name, perm):
    """Updates the Permission section in the Dictionary

    Args:
        name (string): name of the Patient
        perm (int): 0 or 1 denoting the permission

    Returns:
        String : Depicting the Success or Failure
    """
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
    """This Root is accessed when a Hospital needs Consent
    to get data from other Hospitals.

    Returns:
        string : Consent ID if Permission is Given.
    """
    name = request.args.get('name')
    hospital = request.args.get('hospital')
    
    data = get_data_from_dictionary(name, hospital)
    return data

@app.route('/share-consent', methods=['GET'])
def share_consent():
    """This Request is sent during the time of Patient Adding

    Returns:
        string : if permission is given, then consent id is sent.
                else "permission not given" is sent
    """
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

    store_data_in_dictionary(patient)                   # Stores the Data
    data = get_data_from_dictionary(name, hospital)     # Seeks permission here

    return data
    
@app.route('/check-request', methods=['GET'])
def check_requests():
    """Checks the Hopital requests to a particular patient

    Returns:
        string : Name of the Hospital requesting the consent
    """
    name = request.args.get("name")
    
    for each_patient in Patients_Data["patients"]:
        if(each_patient["name"] == name):
            return each_patient["hospital"]
    
    return "No requests"

@app.route('/give-consent', methods=['GET'])
def give_consent():
    """Changes permission field in Dictionary for a patient

    Returns:
        string : "permission granted" if permission = 1
        string : "permission not granted" if permission = 0
    """
    name = request.args.get("name")
    permission = request.args.get("permission")
    if(permission == "0"):
        permission = 0
    else:
        permission = 1
    
    return update_permission(name, permission)

if __name__ == '__main__':
    app.run(port=patient_consent_port, host='0.0.0.0', debug=True)
