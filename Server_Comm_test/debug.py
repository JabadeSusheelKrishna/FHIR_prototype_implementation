import requests

url = "http://127.0.0.1:5000/register"

payload = {}
headers = {
  'username': 'susheel',
  'password': 'susheel',
  'port': '123'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)