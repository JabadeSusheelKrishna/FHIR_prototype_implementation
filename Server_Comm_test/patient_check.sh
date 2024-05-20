name_of_patient=$1
curl --location "http://127.0.0.1:9005/check-request?name=$name_of_patient"