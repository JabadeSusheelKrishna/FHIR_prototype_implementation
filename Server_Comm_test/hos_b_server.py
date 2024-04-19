'''
This code is to implement the central server
'''

from flask import Flask, jsonify, request
import time
import requests
import pprint


app = Flask(__name__)
url = "http://localhost:8080/fhir/"


@app.route('/patient-details', methods=['GET'])
def patient_details():
    time.sleep(1)  # Just For Making Delay ;)
    name = request.args.get('name')
    print("hospital server")
    complete_url = url + "Patient?given=" + name + "&_include=*&_count=5&_pretty=true"

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