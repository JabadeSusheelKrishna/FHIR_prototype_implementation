'''
This code is to implement the central server
'''

from flask import Flask, jsonify, request
import time
import requests
import pprint
import json


app = Flask(__name__)
url = "http://localhost:8080/fhir/"

Dictionary = {"hash" : "name"}

def get_original_name(name):
    with open("hashes.json", "r") as file:
        data = json.load(file)
    
    for each_hash in data:
        if(name == each_hash):
            return data[each_hash]
    return "Not Found"

@app.route('/patient-details', methods=['GET'])
def patient_details():
    time.sleep(1)  # Just For Making Delay ;)
    name = request.args.get('name')
    o_name = get_original_name(name)
    print("----------------------------------------------")
    
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
    app.run(port=5052, debug=True)