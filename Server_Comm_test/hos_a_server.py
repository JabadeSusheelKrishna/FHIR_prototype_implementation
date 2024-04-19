'''
This code is to implement the central server
'''

from flask import Flask, jsonify, request
import time
import requests
import pprint


app = Flask(__name__)
url = "http://localhost:8000/fhir/"


@app.route('/patient-details', methods=['GET'])
def patient_details():
    time.sleep(1)  # Simulating some processing time
    # print(f"Received request with name: {name}")
    # print("Starting time recieved : ", request.headers['start-time'])
    # print("Ending time recieved : ", request.headers['end-time'])
    name = request.args.get('name')
    print("hospital server")
    complete_url = url + "Patient?given=" + name + "&_include=*&_count=5&_pretty=true"

    payload = {}
    headers = {}

    response = requests.request("GET", complete_url, headers=headers, data=payload)
    if(response.json()["total"] > 0):
        list_of_patients = response.json()["entry"]
        # for each_patient in list_of_patients :
        #     pprint.pprint(each_patient["resource"])
    else:
        print("----- No Patient Exists -----")
    return jsonify(list_of_patients)
    # return ({"name": name})

# @app.route('/id=<string:id>', methods=['GET'])
# def hi(id):
#     print("hello kk", id)
#     return jsonify({"message": f"Hello, {id}!"})


if __name__ == '__main__':
    app.run(port=5051, debug=True)