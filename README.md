# image-management-server
An image managment backend server that allows to perform (C)RUD operations on images stored in MongoDB

## Setup
1. install python (v3.9.13)
2. setup venv
   1. `python -m venv venv`
   2. `./venv/Scripts/activate`
   3. `pip install -r requirements.txt`

## Tests
1. run `pytest`

## Run
1. run `python ./src/image_management_server.py <mongo_connection_string> <database> <collection>

## improvements

# api server
- do error and exception handling
- find better way to encapsulate api server with database
# tests
- setup and teardown method for consistent database state
- use database mock for testing and dont rely on assumed database state
- find proper way to setup api server and db without hack
  
