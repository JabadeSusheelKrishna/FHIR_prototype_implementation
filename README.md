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

[insert Demo](https://youtu.be/iHn6OmCZwik)
[view Demo](https://youtu.be/Op5C65tiz1I)
[delete](https://youtu.be/o_m1TGXyoug)

# Running Program on Local Server
> Setup the server on your Local Host Using Docker. (Instructions are given above)
> Now Just Test the Server by clicking on Conformance button. You should be able to see 200/201 response code.
> Now to start working on the server, we first need to create an organisation
>   - Search `organisations` tab from side - bar
>   - Go to Crud operations
>   - Go to create and enter this 
> ```
> { "resourceType": "Organization" }
> ```
> json and click on create button.
>   - if you get 200/201 as response code, then Congradulations, You Setup your server.
>   - Now you can start sending data and receiving data from the server.
> Now Copy the Link eg : 
> ```
> localhost:8080/fhir
> ```
>  and paste it in `Line 7 : app.py`.