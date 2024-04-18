# '''
# This code is to implement the central server
# '''

# from flask import Flask, jsonify, request
# import time

# app = Flask(__name__)

# @app.route('/name=<string:name>', methods=['GET'])
# def hello(name):
#     time.sleep(1)  # Simulating some processing time
#     print(f"Received request with name: {name}")
#     print("Starting time recieved : ", request.headers['start-time'])
#     print("Ending time recieved : ", request.headers['end-time'])
#     return jsonify({"message": f"Hello, {name}!"})

# @app.route('/id=<string:id>', methods=['GET'])
# def hi(id):
#     print("hello kk", id)
#     return jsonify({"message": f"Hello, {id}!"})


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify, request
import time
import requests

app = Flask(__name__)

# Sample list of IDs (you can replace this with your own list of IDs)
# id_list = ['id1', 'id2', 'id3', 'id4', 'id5']

hospitals = {
    'id1': 5051,
    'id2': 5052,
    'id3': 5053,
}

def send_requests_to_other_ids(current_id, name):
    responses = {}
    count = 0
    for id in hospitals:
        print(id)
        if id != current_id:
            print("hi")
            url = f"http://127.0.0.1:{hospitals[id]}/patient-details"
            try:
                response = requests.get(url, params={'name':{name}})
                responses[count] = response.json()
                count += 1
            except requests.exceptions.RequestException as e:
                responses[count] = str(e)
                count += 1
    # print(responses[0])
    return responses

@app.route('/get-details', methods=['GET'])
def handle_request():
    time.sleep(1)  # Simulating some processing time
    print(f"Received request with ID: {request.args.get('id')}")

    name = request.args.get('patient')
    hospital_id = request.args.get('id')
   
    print(name, hospital_id)
    
    # Send requests to all other IDs
    responses = send_requests_to_other_ids(hospital_id, name)
    return jsonify(responses)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
