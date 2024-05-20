'''
This code is to implement the central server
'''

Hospital_port_number = 5052     # Provide Port where you want Hospital server to be run
FHIR_port_number = 8001         # Provide Port or url where Docker is running
fhir_url = "http://localhost:" + str(FHIR_port_number) + "/fhir/"

from flask import Flask, jsonify, request
import requests
import hashlib
from flask_cors import CORS

Hash_data = {}

app = Flask(__name__)
CORS(app)
url = fhir_url

def generate_hash_id(first_name, last_name, dob):
    '''
    geneates hash_id with first name, last name and Date of Birth
    '''
    date, year, month = dob.split("-")
    input_string = f"{first_name.lower()}{last_name.lower()}{date}{month}{year}"
    
    hash_object = hashlib.sha256(input_string.encode())     # generating Hash
    hash_id = hash_object.hexdigest()                       # Converting to 16
    
    return hash_id                                          # returning the Hash

@app.route('/give-me-hash', methods=['GET'])
def retrive_consent():
    '''
    Takes HTTP requests, Extracts the arguments and Generates the Hash.
    '''
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    dob = request.args.get('dob')
    
    data = generate_hash_id(first_name=fname, last_name=lname, dob=dob)
    return data

@app.route('/store-hash-in-json', methods=['POST'])
def store_in_dict():
    '''
    Stores the data in the Dictionary
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
    returns the data present in dictionary as a JSON. (Helpful while debugging)
    '''
    return jsonify(Hash_data)
    
def get_original_name(name):
    '''
    Searches the Hash with our Hash_Data Dictionary and Sends the Name of the Patient
    '''
    for each_hash in Hash_data:
        if(name == each_hash):
            return Hash_data[each_hash]
    return "Not Found"

@app.route('/patient-details', methods=['GET'])
def patient_details():
    '''
    Get Data request is received here. and Data is sent if it is present
    it searches the data in our dictionary. if present, then returns the
    name of the patient and we search the same name in FHIR server. and
    return the response to Central server again. ("_")
    '''
    hash_from_central_server = request.args.get('name')
    
    o_name = get_original_name(hash_from_central_server)    # Here we search the Hash and return the Name
    
    if(o_name == "Not Found"):
        return o_name       # Case where data doesn't exist in Hospital Server or Has no consent
    
    complete_url = url + "Patient?given=" + o_name + "&_include=*&_count=5&_pretty=true"

    payload = {}
    headers = {}
    
    list_of_patients = {}
    response = requests.request("GET", complete_url, headers=headers, data=payload) # Searching in FHIR
    if(response.json()["total"] > 0):
        list_of_patients = response.json()["entry"]
    else:
        print("----- No Patient Exists -----")
    return jsonify(list_of_patients)

if __name__ == '__main__':
    app.run(port=Hospital_port_number, host='0.0.0.0', debug=True)
