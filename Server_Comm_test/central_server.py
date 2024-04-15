'''
This code is to implement the central server
'''

from flask import Flask, jsonify, request
import time

app = Flask(__name__)

@app.route('/<string:name>', methods=['GET'])
def hello(name):
    time.sleep(1)  # Simulating some processing time
    print(f"Received request with name: {name}")
    print("Starting time recieved : ", request.headers['start-time'])
    print("Ending time recieved : ", request.headers['end-time'])
    return jsonify({"message": f"Hello, {name}!"})

if __name__ == '__main__':
    app.run(debug=True)
