# MoInfo
Created by Alina Carrillo, Sydney Moeller, Lucas Navarro
## Description
MoInfo is a service that notify's users of new legislation and representative's voting records in the Missouri Congress. It does this using a program that takes information from Missouri's House and Senate via there individual API's. The bills are then be categorized with tf-idf and store the information on a SQL database. There is also be a program to send out notifications to users that sign up with their emails and topics of interest also stored on a SQL database. They are able to sign up through a website that also stores brief summaries of the bills and individual representatives voting histories. Finally, the website contains interactive features that allow the users to leave comments and interact with each other. 

## Setup
Requirements
    - Python
    - Kafka
To setup a MOinfo server first clone the repository using 
```bash 
    git clone https://github.com/Durza71/MOinfo```

Then navigate into the repository

```bash 
    cd MOinfo 
```

Install the dependencies. It is recommended to use a virtual environment like venv to ensure version control of all python modules.

```bash 
    pip3 install -r requirements.txt 
```

If you want to run a the backend server which contains the database

```bash 
cd kafka_server
python3 start_kafka.py
cd ..
python3 database/setup_database.py
python3 server/application.py 
```

The program will now start downloading bills filling the database and sending notifications.

If you want to start the web server

```bash
python3 server/app.py
```

This will start the webserver on localhost, making the website available for users to register, login, submit their preferences, and get information about bills. The website should only be run after the backend server has started and in a different process.


