'''
This code is able to add patient, search patient, delete patient
'''

import json
import pprint
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
from datetime import datetime

getMyEHR_url = "http://127.0.0.1:5000/"
hospital_base = "http://127.0.0.1:5052/"
patient_consent_server = "http://127.0.0.1:9000/"

app = Flask(__name__)
CORS(app, origins='http://127.0.0.1:5500')

@app.route('/')
def home():
    return "Welcome to the Hospital A server!"

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content response

@app.route('/patient_reg', methods=['POST'])
# def add_patient():
#     # Handle form data submission
#     data = request.get_json()
#     print('Received data:', data)
#     # Process the data and return a JSON response
#     # Example processing and response
#     if data:
#         # Perform patient registration logic here
#         return jsonify({'status': 'success', 'message': 'Patient registered successfully'}), 201
#     else:
#         return jsonify({'status': 'error', 'message': 'Failed to register patient'}), 400

def patient_reg():
    print("debug")
    data = request.get_json()  # Get JSON data from the request
    print(data)
    print("debug")
    # Retrieve data from the request
    hospital = data.get('hospital_name')
    f_name = data.get('first_name')
    l_name = data.get('last_name')
    dob = data.get('dob')
    height = int(data.get('height'))
    weight = int(data.get('weight'))
    mobile = data.get('mobile_number')
    option = data.get('share_medical_info')
    print(hospital)
    # Calculate age from dob
    try:
        birthdate = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        # age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid date of birth format'}), 400

    # Handle consent process
    name = f_name + ' ' + l_name
    # consent_url = f"{patient_consent_server}share-consent?name={name}&hospital={hospital}"
    # response = requests.get(consent_url)

    # if response.status_code != 200:
    #     return jsonify({'status': 'error', 'message': 'Consent server error'}), 500

    # if response.text != 'permission not given' and option == 'Yes':
    #     consent_id = response.text
    # else:
    #     consent_id = ''

    # Generate hash key and create a new patient
    age=19
    # consent_id=" "
    # hash_key = generate_hash_id(f_name, l_name, dob) + consent_id
    patient = Patient(name,age,height, weight, mobile, dob)
    patient_id = patient.store()

    # Store data in JSON
    # store_in_json(name, hash_key)

    # Return a JSON response
    if patient_id:
        return jsonify({'status': 'success', 'patient_id': patient_id}), 201
    else:
        return jsonify({'status': 'error', 'message': 'Failed to store patient'}), 500

def store_admission(patient_id, start_time, end_time, reason):
        # complete_url = Patient.url + "Patient?_format=json"
        complete_url = f"http://localhost:8000/fhir/Encounter"

        payload = {
        "resourceType": "Encounter",
        "id": "example",
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "period": {
            "start": start_time,
            "end": end_time
        },
        "reasonCode": [
            {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "123456",
                            "display": reason
                        }
                    ]
                }
            ]
        }

        headers = {'Content-Type': 'application/json'}

        try:
            # Post the Encounter data
            response = requests.post(complete_url, headers=headers, json=payload)
            print("Response status code:", response.status_code)
            if response.status_code == 201:
                response_json = response.json()
                
                print("Encounter ID:", response_json.get("id"))

                # encounter_id = response_json.get("id")
                # encounter_data_url = f"http://localhost:8000/fhir/Encounter/{encounter_id}?_format=json"
                # encounter_response = requests.get(encounter_data_url)

                # if encounter_response.status_code == 200:
                #     encounter_data = encounter_response.json()
                #     print("Encounter data:", encounter_data)
                return response_json.get("id")
            

            else:
                print("Error:", response.text)
                return "Error: " + response.text
        except Exception as e:
            print("Exception occurred while posting Encounter data:", e)
            return "Error: " + str(e)




@app.route('/add_admission', methods=['POST'])
def add_admission():
    # Parse JSON data from the request
    data = request.get_json()

    # Extract data from the JSON request
    reason = data.get('admissionReason')
    # start_time = data.get('startTime')
    # end_time = data.get('endTime')
    diet_preference = data.get('dietPreference')
    patient_id = data.get('patientID')
    start_time = "2024-04-23T10:00:00Z"
    end_time = "2024-04-23T15:00:00Z"
    # Perform necessary processing with the data
    # For demonstration purposes, we'll just print the data
    print(f"Reason: {reason}, Start Time: {start_time}, End Time: {end_time}, Diet Preference: {diet_preference}, Patient ID: {patient_id}")
    store_admission(patient_id, start_time, end_time,reason)
    # Placeholder for data processing logic
    # For example, you might store the data in a database here

    # Return a JSON response indicating success
    # Replace with actual processing and error handling as needed
    if reason and start_time and end_time and diet_preference and patient_id:
        return jsonify({'status': 'success', 'message': 'Admission added successfully'}), 201
    else:
        return jsonify({'status': 'error', 'message': 'Invalid data provided'}), 400

@app.route('/delete_patient/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    print("Hi")
    print(type(patient_id))
    # Perform necessary processing to delete the patient record based on the patient ID
    try:
        # Placeholder for deletion logic (e.g., deleting the patient record from a database)
        # Assume a function `Patient.delete(patient_id)` exists to delete the patient record
        result = Patient.delete(patient_id)
        
        if result:
            # Return a success response
            return jsonify({'status': 'success', 'message': 'Patient record deleted successfully'}), 200
        else:
            # Return an error response if the deletion failed
            return jsonify({'status': 'error', 'message': 'Failed to delete patient record'}), 500
    
    except Exception as e:
        # Return an error response if an exception occurred
        return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'}), 500

@app.route('/get_patient_details', methods=['POST'])
def get_patient_details():
    # Parse the incoming JSON data
    data = request.get_json()
    
    # Retrieve data from the request
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    hospital_id = data.get('hospital_id')
    hospital_username = data.get('hospital_username')
    login_token = data.get('login_token')
    
    # Placeholder for consent retrieval and data processing logic
    # Use the data provided to look up patient information
    
    # For demonstration, let's assume the request is successful
    # and return dummy patient information
    patient_info = {
        'name': f"{first_name} {last_name}",
        'dob': dob,
        'medical_history': 'No major illnesses',
        'medications': 'None'
    }
    
    # Return a JSON response with patient information
    return jsonify({'status': 'success', 'patient_info': patient_info}), 200
def get_patient_details():
    # Parse the incoming JSON data from the request
    data = request.get_json()
    
    # Retrieve data from the request
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    hospital_id = data.get('hospital_id')
    hospital_username = data.get('hospital_username')
    login_token = data.get('login_token')
    
    # Generate the patient's hash name using your custom function
    name = generate_hash_id(first_name, last_name, dob)
    
    # Create headers for the consent request
    headers = {
        'username': hospital_username,
        'password': 'Doraemon',  # Replace with secure password handling
        'Authorization': f'Bearer {login_token}'  # Replace with actual token handling
    }
    
    # Send a GET request to retrieve patient consent
    consent_url = f"{patient_consent_server}retrive-consent?name={first_name} {last_name}&hospital={hospital_username}"
    response = requests.get(consent_url, headers=headers)
    
    # Handle the response from the consent server
    if response.text != "permission not given":
        consent_id = response.text
        name += consent_id  # Concatenate the consent ID to the name
    else:
        return jsonify({'status': 'error', 'message': 'Patient consent not granted'}), 403

    # Define parameters to send in the GET request to fetch patient details
    params = {
        'patient': name,
        'id': hospital_id,
        'username': hospital_username,
        'access_token': login_token
    }
    
    # Send a GET request to fetch patient details from the server
    patient_details_url = f"{Patient.central_server}/get-details"
    response = requests.get(patient_details_url, params=params)
    
    # Handle the server response
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response from the server
        return jsonify({'status': 'success', 'patient_info': data})
    else:
        return jsonify({'status': 'error', 'message': f'Server responded with status code {response.status_code}'}), response.status_code

@app.route('/login', methods=['POST'])
def login():
    # Parse JSON data from the request
    data = request.get_json()
    
    # Retrieve username and password from the request data
    username = data.get('username')
    password = data.get('password')
    
    # Call send_login_request to send a POST request and receive a response
    response = send_login_request(username, password)
    
    # Handle the response
    if response.get('status') == 'success' or 1:
        # Login succeeded
        access_token = response.get('access_token')
        return jsonify({'status': 'success', 'access_token': access_token}), 200
    else:
        # Login failed
        error_message = response.get('message', 'Login failed')
        return jsonify({'status': 'error', 'message': error_message}), 401
    
# Define the route for registering the hospital
@app.route('/register', methods=['POST'])
def register():
    # Parse JSON data from the request body
    data = request.get_json()
    
    # Retrieve the data from the request
    username = data.get('username')
    password = data.get('password')
    ip_address = data.get('ip_address')  # Assuming this is the field for the IP address

    # Perform validation and registration logic here
    # For example, you could store the hospital data in a database

    # Example validation: Check if the required fields are present
    if not all([username, password, ip_address]):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    # Example registration logic: Store the data (you can replace this with your actual registration process)
    # Assuming you have a function `register_hospital(username, password, ip_address)` that handles registration
    success = register_hospital(username, password, ip_address)

    if success:
        # Registration successful
        return jsonify({'status': 'success', 'message': 'Hospital registered successfully'}), 201
    else:
        # Registration failed (e.g., due to a duplicate username or other issues)
        return jsonify({'status': 'error', 'message': 'Registration failed'}), 400

def register_hospital(username, password, ip_address):
    # This is a placeholder function. Implement your actual registration logic here.
    # For example, you might store the hospital data in a database and return True if successful.
    # Return False if the registration fails.
    print(f"Registering hospital: username={username}, password={password}, ip_address={ip_address}")
    # Placeholder: Assume the registration is successful
    return True

@app.route('/view_patient', methods=['GET'])
def search_patient():
    # Retrieve the patient's name from the query parameter
    patient_name = request.args.get('name')
    
    # Perform the search operation
    # Here, we are assuming that you have a function `search_patient_by_name(name)`
    # that takes a patient's name as input and returns a list of patients with matching names.
    print(patient_name)
    patient_demographics,patient_admission_details = search_patient_by_name(patient_name)
    print("going to print patient demographics")
    # print(patient_demographics)
    # Extract 'given', 'value', and 'birthDate' values
    print(patient_demographics)
    if patient_demographics !={}:
        given_name = patient_demographics['name'][0]['given'][0]
        phone_number = patient_demographics['telecom'][0]['value']
        birth_date = patient_demographics['birthDate']
        patient_id = int(patient_demographics['id'])
        print(patient_admission_details)
        print("Given Name:", given_name)
        print("Phone Number:", phone_number)
        print("Birth Date:", birth_date)
        print("going to print patient admissions details")
    # Extract 'start', 'end', and 'display' values
    if(patient_admission_details != {}):
        start_time = patient_admission_details['period']['start']
        end_time = patient_admission_details['period']['end']
        reason_display = patient_admission_details['reasonCode'][0]['coding'][0]['display']
        print("Start Time:", start_time)
        print("End Time:", end_time)
        print("Reason Display:", reason_display)
    # Check if any patients were found
    else:
        print("no admission")
    
    if patient_demographics != {}:
        print("hello patients")
        # Return a success response with the list of patients
        if patient_admission_details == {}:
            return jsonify({
                'patient_name':given_name,
                'phone_number':phone_number,
                'birth_date':birth_date,
                'status': 'success',
                'patient_id': patient_id
            }), 200
        else:
            print("not")
            return jsonify({
                    'patient_name':given_name,
                    'phone_number':phone_number,
                    'birth_date':birth_date,
                    'status': 'success',
                    'patient_id': patient_id,
                    'start_time':start_time,
                    'end_time':end_time,
                    'reason':reason_display

                }), 200
    else:
        # Return an error response if no patients were found
        return jsonify({
            'status': '',
            'message': 'No patients found with the given name'
        }), 404

# Implement your own function to search for patients by name
# This function should query your data source (e.g., a database) for patients with the given name
# def search_patient_by_name(name):
#     # This is a placeholder function. Implement your actual search logic here.
#     # For example, you might query a database and return a list of patients.
#     # Return a list of dictionaries representing patients.
#     example_patients = [
#         {'name': 'John Doe', 'age': 35, 'medical_history': 'Ass pain'},
#         {'name': 'Jane Smith', 'age': 28, 'medical_history': 'got kicked by a kid'},
#         {'name': 'Jane Smith', 'age': 29, 'medical_history': 'got kicked by a granny and a paleontologist'},
#     ]
#     # Filter the list of example patients based on the name (case-insensitive)
#     filtered_patients = [patient for patient in example_patients if name.lower() in patient['name'].lower()]
    
#     return filtered_patients
def search_patient_by_name(name):
    '''
        Implement this using APIs
        '''
    import requests
    complete_url = Patient.url + "Patient?given=" + name + "&_include=*&_count=5&_pretty=true"

    print("Searching Patient")
    payload = {}
    headers = {}
    patient_demographics={}
    patient_admission_details={}
    id=0
    response = requests.request("GET", complete_url, headers=headers, data=payload)
    if(response.json()["total"] > 0):
            print("total")
            list_of_patients = response.json()["entry"]
            for each_patient in list_of_patients :
                print("only one")
                pprint.pprint(each_patient["resource"])
                patient_demographics=each_patient["resource"]
                id = int(each_patient["resource"]["id"])
                print("only one only")
    else:
            print("----- No Patient Exists -----")
        
    encounter_id = id +1
    encounter_data_url = f"http://localhost:8000/fhir/Encounter/{encounter_id}?_format=json"
    encounter_response = requests.get(encounter_data_url)

    if encounter_response.status_code == 200:
            encounter_data = encounter_response.json()
            patient_admission_details=encounter_data
            print("Encounter data:", encounter_data) 
    else:
            print("Error")
   
    return patient_demographics,patient_admission_details
# @staticmethod
# def search(name):
#     """
#     Search for patients using an API request.

#     Args:
#         name (str): The given name of the patient to search for.

#     Returns:
#         list: A list of patients matching the given name, or None if an error occurs.
#     """
#     complete_url = f"{Patient.url}Patient?given={name}&_include=*&_count=5&_pretty=true"

#     try:
#         # Send API request
#         response = requests.get(complete_url)

#         # Check if the response is successful
#         if response.status_code == 200:
#             data = response.json()
#             # Check if patients are found
#             if data.get("total", 0) > 0:
#                 return data["entry"]
#             else:
#                 return []
#         else:
#             # Log the error
#             app.logger.error(f"Failed to fetch data. Status code: {response.status_code}")
#             return None
#     except requests.RequestException as e:
#         # Log the exception
#         app.logger.error(f"API request error: {e}")
#         return None

# @app.route('/search_patient', methods=['GET'])
# def search_patient():
#     # Get the 'name' query parameter
#     name = request.args.get('name')

#     # Perform the search
#     patients = search(name)

#     if patients is not None:
#         # Return a JSON response with the list of patients
#         return jsonify({
#             'status': 'success',
#             'total': len(patients),
#             'patients': patients
#         }), 200
#     else:
#         # Return an error response if the search failed
#         return jsonify({
#             'status': 'error',
#             'message': 'Failed to fetch patient data'
#         }), 500


def send_request(url, header):
    try:
        print("Sending this as header : ", header)
        response = requests.request("GET", url, headers=header)
        if response.status_code == 200:
            print("GET request successfully sent!")
            print("\nResponse:", response.text) # Here it recieves all the details
        else:
            print("Failed to send GET request. Status code:", response.status_code)
    except requests.RequestException as e:
        print("Error:", e)
        
def send_login_request(username, password):
    '''
    Sends the Username and password as POST request to the server
    '''
    url = getMyEHR_url + 'login'
    payload = {}
    headers = {
        'username': username,
        'password': password
        }

    response = requests.request("POST", url, headers=headers, data=payload)
    # Check response status
    if response.status_code == 200:
        return response.json()
    else:
        # If response status code is not 200, return error message
        return {
            'status': 'error',
            'message': f"Failed to login. Status code: {response.status_code}"
        }
        
def store_in_json(name, hash):
    with open("hashes.json", "r") as file:
        data = json.load(file)
    
    data[hash] = name
    print("SSSSSSSSSSSSSSSSS : ", data)
    
    with open("hashes.json", "w") as file:
        json.dump(data, file)
    
    print(" ------- Data Added ------ ")

import hashlib

def generate_hash_id(first_name, last_name, dob):
    """
    Generates a unique hash ID based on the provided first name, last name, and date of birth.
    
    Args:
        first_name (str): The person's first name.
        last_name (str): The person's last name.
        dob (str): The person's date of birth in the format "DD-MM-YYYY".
    
    Returns:
        str: The generated hash ID.
    """
    # Split the date of birth into its components
    year, month, day = dob.split("-")
    
    # Concatenate the components in the desired order
    input_string = f"{first_name.lower()}{last_name.lower()}{month}{year}"
    
    # Compute the SHA-256 hash and return the hexadecimal string
    hash_object = hashlib.sha256(input_string.encode())
    hash_id = hash_object.hexdigest()
    
    # Print the length of the hash ID
    print(f"The length of the hash ID is: {len(hash_id)}")
    
    return hash_id


class Patient:
    
    # url = "http://hapi.fhir.org/baseR4/"
    url = "http://localhost:8000/fhir/"
    central_server = "http://127.0.0.1:5000/"
    
    def __init__(self, name, age, height, weight, mobile, birthdate):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.mobile = mobile
        self.birthdate = birthdate

    def store(self):
        '''
        Implement this using API calls
        '''
        complete_url = Patient.url + "Patient?_format=json"
        payload = json.dumps({
          "resourceType": "Patient",
          "id": "example-patient",
          "name": [
            {
              "use": "official",
              "given": [
                self.name
            ]
            }
        ],
        "telecom": [
            {
            "system": "phone",
            "value": str(self.mobile),
            "use": "mobile"
            }
        ],
        "height": {
            "value": self.height,
            "unit": "cm",
            "system": "http://unitsofmeasure.org",
            "code": "cm"
        },
        "weight": {
            "value": self.weight,
            "unit": "kg",
            "system": "http://unitsofmeasure.org",
            "code": "kg"
        },
        "birthDate": "2005-10"
        })
        headers = {
          'Content-Type': 'application/json'
        }
        print("Complete URL check : ",complete_url)
        
        response = requests.request("POST", complete_url, headers=headers, data=payload)
        if(response.status_code == 201):
            print("hi")
            return response.json()["id"]
        else:
            return "Error There"

    @staticmethod
    def search(name):
        '''
        Implement this using APIs
        '''
        import requests
        complete_url = Patient.url + "Patient?given=" + name + "&_include=*&_count=5&_pretty=true"

        payload = {}
        headers = {}

        response = requests.request("GET", complete_url, headers=headers, data=payload)
        if(response.json()["total"] > 0):
            list_of_patients = response.json()["entry"]
            for each_patient in list_of_patients :
                pprint.pprint(each_patient["resource"])
        else:
            print("----- No Patient Exists -----")

    @staticmethod
    def delete(id2):
        '''
        Implement this using APIs
        '''
        p_id = id2
        complete_url = Patient.url + "Patient/" + str(p_id) +"?_pretty=true"
        payload = {}
        headers = {}
        print(complete_url)
        response = requests.request("DELETE", complete_url, headers=headers, data=payload)
        if(response.status_code == 200):
            print("------ COMPLETED DELETION --------")
            return 1
        else:
            print("----- ERROR : Please provide correct Fields ------")
            return 0

    @staticmethod
    def enter_new_patient():
        # Function to enter details of a new patient
        
        print("Entering details for a new patient...")
        hospital = input("Enter the Hospital Name : ")
        f_name = input("Enter the First Name of the Patient : ")
        l_name = input("Enter the second name of the Patient : ")
        # age = int(input("Enter the Age : "))
        height = int(input("Enter the Height : "))
        weight = int(input("Enter the Weight : "))
        mobile = int(input("Enter the Mobile Number : "))
        # birthdate = input("Enter Your Date of Birth in YYYY-MM : ")
        birthdate="2004-01-01"
        option = input("Do you want to share information in future (yes/no): ")
        name = f_name + l_name
        consent_url = patient_consent_server + "share-consent?name="+name+"&hospital="+hospital
        print(consent_url)
        payload = {}
        headers = {}
        response = requests.request("GET", consent_url, headers=headers, data=payload)
        print("response from patient : ", response.text)

        consent_id = ""
        if(response.text != "permission not given" and option == 'yes'):
            consent_id = response.text
        hash_key = generate_hash_id(f_name, l_name, birthdate) + consent_id
        patient = Patient(name, height, weight, mobile, birthdate)
        id2 = patient.store()
        print("---------------------------------------------")
        store_in_json(name, hash_key)
        if id2:
            print("----- Data Stored Successfully -----")
            print("Your ID : ", id2)
        
        # print(add_patient())

    @staticmethod
    def view_patient():
        # Function to view details of a specific patient
        print("Viewing details of a patient...")
        name_to_search = input("Please enter the Name that you want to search : ")
        Patient.search(name_to_search)
        print("------- SEARCH COMPLETED --------")

    @staticmethod
    def delete_patient_record():
        # Function to delete a patient's record
        print("Deleting a patient's record...")
        id2 = int(input("Enter the ID of the Patient : "))
        Patient.delete(id2)

    @staticmethod
    def get_patient_details():
        print("For Now, You can only access patients admission details")
        print("Please Enter the Patient Details to get his information")
        f_name = input("Enter First Name of the Patient : ")
        l_name = input("Enter the Last name of the Patient : ")
        dob = input("Enter the Data of birth YYYY-MM : ")
        name = generate_hash_id(f_name, l_name, dob)
        id_of_patient = input("Enter the Hospital ID (Port) : ")
        username = input("Enter Hospital Username : ")
        token = input("Enter the token generated after Login : ")
        print("----------- Waiting for Patient Consent -------------")
        consent_id = "" # Need to send request to the Patient Consent for retrieve
        consent_url = patient_consent_server + "retrive-consent?name="+f_name+l_name+"&hospital="+username
        payload = {}
        headers = {
          'username': 'susheelkrishna',
          'password': 'Doraemon',
          'Authorization': 'Bearer ddfdnjfhjfkd'
        }
        response = requests.request("GET", consent_url, headers=headers, data=payload)
        if(response.text != "permission not given"):
            consent_id = response.text

        name += consent_id
        params = {
        'patient': {name},
        'id': {id_of_patient},  # Assuming this is the hospital ID
        'username' : {username},
        'access_token' : {token}
        }
        response = requests.get(f"{Patient.central_server}/get-details", params=params)
        if response.status_code == 200:
            data = response.text
            print("Response from server:")
            print(data)
        else:
            print("Error:", response.status_code)
            
    @staticmethod
    def register_to_server():
        username = input("Enter the Username : ")
        password = input("Enter the password : ")
        port = input("Enter the IP address of hospital : ")
        
        url = "http://127.0.0.1:5000/register?username="+username+"&password="+password+"&port="+port
        print("Sending to URL : ", url)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        
    @staticmethod
    def Login_to_server():
        '''
        This Function sends post request to the getMyEHR server.
        Finally, it recieves the Message whether the Login is Succeeded
        '''
        print("-------- You are Now LOGGING IN -------")
        username = input("Enter the Username : ")
        password = input("Enter the Password : ")
        response = send_login_request(username, password)
        print("--------Response : Access_Token : {} --------", response)

    @staticmethod
    def add_admission():
        reason = input("Enter the reason : ")
        start_time = input("Enter the Start Time : ")
        end_time = input("Enter the End time : ")
        diet_preference = input("Enter the Diet preference : ")
        patient_id = input("Enter the Patient id : ")
        print("Will be implemented in future")

    @staticmethod
    def switch_case(option):
        # Switch case function to execute different actions based on user input
        switcher = {
            1: Patient.enter_new_patient,
            2: Patient.view_patient,
            3: Patient.delete_patient_record,
            4: Patient.get_patient_details,
            5: Patient.register_to_server,
            6: Patient.Login_to_server,
            7: Patient.add_admission
        }
        # Get the function corresponding to the user's input option
        selected_function = switcher.get(option, lambda: print("Invalid option"))
        # Execute the selected function
        selected_function()

# options = int(input("""
# Choose an Option from below :
# 1) Enter New Patient
# 2) View Patient in Local Server
# 3) Delete Patient Record
# 4) Get Details of the patient from other hospitals
# 5) Register my hospital to GetMyEHR
# 6) Login to getMyEHR
# 7) Add Admission Details

# """))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Patient.switch_case(options)

