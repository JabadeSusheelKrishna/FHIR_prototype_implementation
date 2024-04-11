# FHIR_prototype_implementation
We are creating two servers and establishing communication between them.
for server creattion we are using HAPI JAP server setup.
for setting up the server, follow the below instructions : 
> ### Server Setup
> - Clone the JAP repository
> ```
> git clone https://github.com/hapifhir/hapi-fhir-jpaserver-starter.git
> ```
> - Now Navigate to src
> ```
> cd hapi-fhir-jpaserver-starter/src 
> ```
> - Now run the following commands to start the server on your Local Host 8080 (This may take some time)
> ```
> docker pull hapiproject/hapi:latest ; docker run -p 8080:8080 hapiproject/hapi:latest
> ```
> - When you are able to see "0 deleted" then you can search `localhost:8080` on your web browser and start playing with it.

# Status Quo
presently this `app.py` code inserts, deletes, searches data in global fhir server. (Please donot insert any valuable information because it can be accessed by any one)
(https://youtu.be/iHn6OmCZwik)
![](view.mp4)
![](delete.mp4)
