'''
This code is able to add patient, search patient, delete patient
'''

import json
import pprint
import requests

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
    
class Patient:
    
    # url = "http://hapi.fhir.org/baseR4/"
    url = "http://localhost:8002/fhir/"
    central_server = "http://127.0.0.1:5000/"
    
    def __init__(self, name, age, height, weight, mobile):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.mobile = mobile

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
        }
        })
        headers = {
          'Content-Type': 'application/json'
        }
        print("qwertyuiop",complete_url)

        response = requests.request("POST", complete_url, headers=headers, data=payload)
        # print(type(response.status_code))
        if(response.status_code == 201):
            return response.json()["id"]

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
        
        patient = Patient(name, age, height, weight, mobile)
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
        # start_time = input("Enter the Start time : ")
        # end_time = input("Enter the End time : ")
        id = input("Enter the Patient ID: ")

        send_url = Patient.central_server + str(name)
        params = {
        'patient': {name},
        'id': {id}  # Assuming this is the hospital ID
        }
        response = requests.get(f"{Patient.central_server}/get-details", params=params)
        # send_headers = {"start-time": start_time, "end-time": end_time}
        # send_request(send_url, send_headers)
        if response.status_code == 200:
            data = response.json()
            print("Response from server:")
            print(data)
        else:
            print("Error:", response.status_code)

    @staticmethod
    def switch_case(option):
        # Switch case function to execute different actions based on user input
        switcher = {
            1: Patient.enter_new_patient,
            2: Patient.view_patient,
            3: Patient.delete_patient_record,
            4: Patient.get_patient_details
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

"""))

Patient.switch_case(options)

