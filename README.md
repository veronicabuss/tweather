# tweather
Twitter Weather Project for CS6100 -  A Big Data Application to Explore How Twitter Users Talk About the Weather

### Install
------
To install the Front End:
(All commands assume you start in the root project directory)
Two separate terminals are required to run the front and back end services.

- Install npm (this will be different depending on your os)
- Install vue tools
    - `npm install -g @vue/cli @vue/cli-init`
- `cd frontend`
- `npm install`
To start the front end run:
- `cd frontend`
- `npm run dev`
OR
- ./startFront.sh

The webserver will be running at: http://localhost:8080/

Virtual Environment  (linux):
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- Now the backend service can be started
  - `./startBack.sh`
- When finished:
  - `deactivate`

Virtual Environment (Windows):
- `python3 -m venv venv`
- `cd venv/Scripts`
- `& .\activate`
- `pip install -r requirements.txt`
- Now the backend service can be started
  - `$env:FLASK_APP = "./backend/run.py"`
  - `flask run`
- When finished:
    - `deactivate`

To make sure the back end is running properly: http://localhost:5000/ should bring up a mostly blank page.
