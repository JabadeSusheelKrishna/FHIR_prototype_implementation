import requests
import json

class Patient:
    
    url = "	http://hapi.fhir.org/baseR4/"
    
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

        response = requests.request("POST", complete_url, headers=headers, data=payload)
        # print(type(response.status_code))
        if(response.status_code == 201):
            return 1

    @staticmethod
    def search(name):
        '''
        Implement this using APIs
        '''
        pass

    @staticmethod
    def search_all():
        '''
        Implement this using APIs
        '''
        pass

    @staticmethod
    def delete(id):
        '''
        Implement this using APIs
        '''
        pass

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
        if patient.store():
            print("----- Data Stored Successfully -----")

    @staticmethod
    def view_patient():
        # Function to view details of a specific patient
        print("Viewing details of a patient...")
        name_to_search = input("Please enter the Name that you want to search : ")
        Patient.search(name_to_search)

    @staticmethod
    def view_all_patients():
        # Function to view details of all patients
        print("Viewing details of all patients...")
        Patient.search_all()

    @staticmethod
    def delete_patient_record():
        # Function to delete a patient's record
        print("Deleting a patient's record...")
        id = int(input("Enter the ID of the Patient : "))
        Patient.delete(id)

    @staticmethod
    def switch_case(option):
        # Switch case function to execute different actions based on user input
        switcher = {
            1: Patient.enter_new_patient,
            2: Patient.view_patient,
            3: Patient.view_all_patients,
            4: Patient.delete_patient_record
        }
        # Get the function corresponding to the user's input option
        selected_function = switcher.get(option, lambda: print("Invalid option"))
        # Execute the selected function
        selected_function()

# Main code
options = int(input("""
Choose an Option from below :
1) Enter New Patient
2) View Patient
3) View all patients
4) Delete Patient Record
"""))

Patient.switch_case(options)
