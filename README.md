# Complete Set up guide

### Cloning the Repository
> - First you need to clone the Repo by running the below command
> ```
> git clone https://github.com/JabadeSusheelKrishna/FHIR_prototype_implementation.git
> ```
> - If you are unable to clone the Above repository, You can Just download Zip File
> - Now, if you are able to see a folder named `FHIR_prototype_Implementation` then congrats. you are able to Download Our server in you Local Machine.

### Setting Up Servers
> - Now Lets first Setup the `Central Server and Patient Consent Server` by running below code.
> - if you are not in `FHIR_prototype_Implementation` directory, the go to that directory by :
> ```
> cd FHIR_prototype_Implementation
> ```
> - Now go to `Server_Comm_test` folder by running the following : 
> ```
> cd Server_Comm_test
> ```
> - Now try to run the `main_servers.sh` by following command : 
> ```
> ./main_servers.sh
> ```
> ### If you are unable to run above command, then try below
> 
> > - run the following command to start the central server : 
> > ```
> > python3 central_server.py
> > ```
> > - Now Lets Run the Patient Consent Server by running the following command :
> > ```
> > python3 patient_consent.py
> > ```
> - If you are able to see Server getting run on both codes, then you are successfully able to run Central Server
> - (Note : Central server doesn't gets executed because of some module error, please install them/ upgrade them)
> - Please donot reload any of the servers. Because data for now is stored in Volatile memory.

### Now lets setup the Hospital Servers
> - Run Hospital server by running the following commands. Also make sure that you are in `Server_Comm_test` directory
> ```
> python3 hos_a_server.py
> ```
> - if you are trying to test on the Single system, then for multiple hospitals test, please run the `hos_b_server.py`  and `hos_c_server.py`. because the IP address is same, so common port can create and issue.
> - in case of multiple systems, You can run `hos_a_server.py` in different systems. because the Ip address changes for each system. So common port is not an issue.
> - Now we also have to run the FHIR server to store patient data. for that run the below command : 
> ```
> ./fhir_server.sh <port_number>
> ```
> ### IF you are not able to run above command, then try running below commands
> >  - Come Out of the `Server_Comm_test` folder by running : 
> >  ```
> >  cd ..
> >  ```
> >  - Now go to `hapi-fhir-jpaserver-starter` folder by running the following command : 
> >  ```
> >  cd hapi-fhir-jpaserver-starter
> >  ```
> >  - run the Docker on 8000 port by running the following command : 
> >  ```
> >  sudo docker run -p 8000:8080 hapiproject/hapi:latest
> >  ```
> - Enter your system password if asked.
> - if you are able to see 0 deleted text getting repeated, then your FHIR implementation is working
> - if you want to run for multiple hospitals, change the port to 8001, 8002 ... respectively and remember that `hos_b_server.py` and `hos_c_server.py` are linked to it respectively.

### Registering Orgainzation
> - go to browser and search the following : 
> ```
> localhost:<port_of_fhir>
> ```
> - Now if you are able to see website, then your Docker server is running correctly.
> - Now in left menu, search for the Organization.
> - Go to `Crud` operations
> - Go to `search` text field.
> - Type the following in text field : 
> ```
> {"resourceType" : "Organization"}
> ```
> - click `Search`.
> - You should be able to see success message. <b>(200/201 response code)</b>

### Running the UI : 
> - Open VS code and Open `Server_Comm_test` folder in it.
> - Now go to `Webspace/Hos_1` folder and there you can see `home_portal.html` file.
> - Make sure you have live server extension.
> - Now right click the `home_portal.html` file. and `click open with liveserver`
> - You will now get redirected to the webpage.
> (Note : if you are getting any errors, please check `script.js` in Same directory. Make sure that all the links provided are correct)

### Few Important Points to Remember :
> - If you want to work in single system, them make use of Ports. (i.e make sure that servers are ran on different Ports).
>    - also make sure that in text field of ip address, you need to provide `http://127.0.0.1:<port>`
> - If you are working on different systems, then make sure that both systems are on network. then type `ifconfg` or `ip address` to get the ip address of that system.
>    - suppose the ip address of the system where hospital server - 1 is running is `10.20.30.40` then during registration, please enter `http://10.20.30.40:<port_where_server_is_running>`.
>    - If you want to have more hospitals, then just copy the hos_a_server.py and change the Port number and FHIR server port in code (you can find them in `Line 4 and 5`
>    - Similarly, for webiste, just change the `script.js` accordingly.

### Application Part : 
> - For application, clone the `swaroop_final` branch.
> - There you can find a folder named `patient_consent`. You can find react native app there.
> - Just cd to that directory and install packages and run the App.
> ```
> cd patient_consent
> npm install
> npm start
> ```
> - make sure that you update

### Test cases that we tried on this system.
> - (tested) One of the Hospital Has data and the other doesn't has the data
> - (tested) More than one Hospital has the data and has consent to share
> - (tested) All the hospitals have data of a patient and consent to share
> - (tested) Hospital asking data without consent
> - (tested) Hospitals having data but doesn't have share consent
> - (tested) User neglects the consent
> - (tested) Hospital with wrong access token (during get-data) or passowrd (during Login)
> - (tested) No hospital has data of the patient
> - (tested) reload of Central server without issues
> - (tested) Adding patient details into the FHIR server
> - (tested) Adding Patient hash id and name in Hospital Local Server
> - (not tested) Deleting the patient from FHIR server but not from Hospital local server
> - (not tested) Trying to send request to Hospital without front end, and without patient consent.
> - (not tested) Hospital servers accessing same FHIR server.
> - (not tested) Verifying Hospital credentials during the Patient consent.

# Thank you for providing the oppurtunity
