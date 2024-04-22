# Code to create a Encounter

patient_id = 44676119
start_time = "2024-04-23T10:00:00Z"
end_time = "2024-04-23T15:00:00Z"
reason = "Headache due to IHS"

import requests
import json

url = "http://hapi.fhir.org/baseR4/Encounter?_format=json&_pretty=true"

payload = json.dumps({
  "resourceType": "Encounter",
  "id": "example",
  "subject": {
    "reference": "Patient/" + str(patient_id)
  },
  "period": {
    "start": start_time,
    "end": end_time
  },
  "reasonCode": [
    {
      "coding": [
        {
          "system": "SNOMED-CT",
          "code": "123456",
          "display": reason
        }
      ]
    }
  ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
