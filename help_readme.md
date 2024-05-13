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
> docker pull hapiproject/hapi:latest
> ```
> ```
> docker run -p 8080:8080 hapiproject/hapi:latest
> ```
> - When you are able to see "0 deleted" then you can search `localhost:8080` on your web browser and start playing with it.

# Status Quo
presently this `app.py` code inserts, deletes, searches data in global fhir server. (Please donot insert any valuable information because it can be accessed by any one)

[insert Demo](https://youtu.be/iHn6OmCZwik)
[view Demo](https://youtu.be/Op5C65tiz1I)
[delete](https://youtu.be/o_m1TGXyoug)

# Running Program on Local Server
> Setup the server on your Local Host Using Docker. (Instructions are given ![above](https://github.com/JabadeSusheelKrishna/FHIR_prototype_implementation?tab=readme-ov-file#server-setup))
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

# Setup Elasticsearch with Docker

## Prerequisites

1. Install [Docker](https://www.docker.com/get-started) for your environment.
2. If using Docker Desktop, allocate at least 4GB of memory. You can adjust memory usage in Docker Desktop by going to `Settings > Resources`.

## Create a Docker Network

1. Create a new Docker network:

    ```bash
    docker network create elastic
    ```

## Pull Elasticsearch Docker Image

1. Pull the Elasticsearch Docker image:

    ```bash
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.2
    ```

### Optional: Verify Elasticsearch Image Signature

1. Install Cosign for your environment.
2. Verify the Elasticsearch image's signature:

    ```bash
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/elasticsearch/elasticsearch:8.13.2
    ```

    The `cosign verify` command prints the check results and the signature payload in JSON format.

## Start an Elasticsearch Container

1. Start an Elasticsearch container:

    ```bash
    docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.13.2
    ```

    - Use the `-m` flag to set a memory limit for the container. This removes the need to manually set the JVM size.
    - The command prints the `elastic` user password and an enrollment token for Kibana.

2. Copy the generated `elastic` password and enrollment token. These credentials are only shown when you start Elasticsearch for the first time.

### Regenerate Credentials

1. To regenerate the `elastic` password, run:

    ```bash
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
    ```

2. To regenerate the enrollment token for Kibana, run:

    ```bash
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    ```

### Store `elastic` Password

1. Store the `elastic` password as an environment variable in your shell:

    ```bash
    export ELASTIC_PASSWORD="your_password"
    ```

## Copy SSL Certificate

1. Copy the `http_ca.crt` SSL certificate from the container to your local machine:

    ```bash
    docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
    ```

## Make a REST API Call

1. Make a REST API call to Elasticsearch to ensure the Elasticsearch container is running:

    ```bash
    curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
    ```


# Setup Elasticsearch and Kibana with Docker

## Prerequisites

1. Install [Docker](https://www.docker.com/get-started) for your environment.
2. If using Docker Desktop, allocate at least 4GB of memory. You can adjust memory usage in Docker Desktop by going to `Settings > Resources`.

## Create a Docker Network

1. Create a new Docker network for Elasticsearch and Kibana:

    ```bash
    docker network create elastic
    ```

## Pull Elasticsearch Docker Image

1. Pull the Elasticsearch Docker image:

    ```bash
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.2
    ```

### Optional: Verify Elasticsearch Image Signature

1. Install Cosign for your environment.
2. Verify the Elasticsearch image's signature:

    ```bash
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/elasticsearch/elasticsearch:8.13.2
    ```

    The `cosign verify` command prints the check results and the signature payload in JSON format.

## Start an Elasticsearch Container

1. Start an Elasticsearch container:

    ```bash
    docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.13.2
    ```

    - Use the `-m` flag to set a memory limit for the container. This removes the need to manually set the JVM size.
    - The command prints the `elastic` user password and an enrollment token for Kibana.

2. Copy the generated `elastic` password and enrollment token. These credentials are only shown when you start Elasticsearch for the first time.

### Regenerate Credentials

1. To regenerate the elastic password, run:

    ```bash
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
    ```

2. To regenerate the enrollment token for Kibana, run:

    ```bash
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    ```

## Pull Kibana Docker Image

1. Pull the Kibana Docker image:

    ```bash
    docker pull docker.elastic.co/kibana/kibana:8.13.2
    ```

### Optional: Verify Kibana Image Signature

1. Use Cosign to verify the Kibana image's signature:

    ```bash
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/kibana/kibana:8.13.2
    ```

## Start a Kibana Container

1. Start a Kibana container:

    ```bash
    docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.13.2
    ```

    - When Kibana starts, it outputs a unique generated link to the terminal. To access Kibana, open this link in a web browser.
    - In your browser, enter the enrollment token that was generated when you started Elasticsearch.

### Regenerate Token and Password

1. To regenerate the enrollment token, run:

    ```bash
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    ```

2. To regenerate the password, run:

    ```bash
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
    ```

Log in to Kibana as the `elastic` user with the password that was generated when you started Elasticsearch.


