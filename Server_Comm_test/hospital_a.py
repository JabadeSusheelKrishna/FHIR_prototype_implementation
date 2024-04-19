'''
This code is able to add patient, search patient, delete patient
'''

import json
import pprint
import requests
from flask import Flask
import time

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
    day, month, year = dob.split("-")
    
    # Concatenate the components in the desired order
    input_string = f"{first_name.lower()}{last_name.lower()}{day}{month}{year}"
    
    # Compute the SHA-256 hash and return the hexadecimal string
    hash_object = hashlib.sha256(input_string.encode())
    hash_id = hash_object.hexdigest()
    
    # Print the length of the hash ID
    print(f"The length of the hash ID is: {len(hash_id)}")
    
    return hash_id


class Patient:
    
    # url = "http://hapi.fhir.org/baseR4/"
    url = "http://localhost:8080/fhir/"
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

        response = requests.request("DELETE", complete_url, headers=headers, data=payload)
        if(response.status_code == 200):
            print("------ COMPLETED DELETION --------")
        else:
            print("----- ERROR : Please provide correct Fields ------")

    @staticmethod
    def enter_new_patient():
        # Function to enter details of a new patient
        print("Entering details for a new patient...")
        name = input("Enter the Name of the Patient : ")
        age = int(input("Enter the Age : "))
        height = int(input("Enter the Height : "))
        weight = int(input("Enter the Weight : "))
        mobile = int(input("Enter the Mobile Number : "))
        birthdate = input("Enter Your Date of Birth in YYYY-MM : ")
        
        patient = Patient(name, age, height, weight, mobile, birthdate)
        id2 = patient.store()
        if id2:
            print("----- Data Stored Successfully -----")
            print("Your ID : ", id2)

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
        name = input("Enter Name of the Patient : ")
        id_of_patient = input("Enter the Hospital ID (Port) : ")
        params = {
        'patient': {name},
        'id': {id_of_patient}  # Assuming this is the hospital ID
        }
        response = requests.get(f"{Patient.central_server}/get-details", params=params)
        if response.status_code == 200:
            data = response.json()
            print("Response from server:")
            print(data)
        else:
            print("Error:", response.status_code)
            
    @staticmethod
    def register_to_server():
        username = input("Enter the Username : ")
        password = input("Enter the password : ")
        port = 5051
        
        url = "http://127.0.0.1:5000/register?username=hospetal&password=Admin&port=5051"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response)

    @staticmethod
    def switch_case(option):
        # Switch case function to execute different actions based on user input
        switcher = {
            1: Patient.enter_new_patient,
            2: Patient.view_patient,
            3: Patient.delete_patient_record,
            4: Patient.get_patient_details,
            6: Patient.register_to_server
        }
        # Get the function corresponding to the user's input option
        selected_function = switcher.get(option, lambda: print("Invalid option"))
        # Execute the selected function
        selected_function()

# Main code
options = int(input("""
Choose an Option from below :
1) Enter New Patient
2) View Patient in Local Server
3) Delete Patient Record
4) Get Details of the patient from other hospitals
5) Get id of the patient from other hospitals
6) Register my hospital to GetMyEHR

"""))

Patient.switch_case(options)

