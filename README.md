# tweather
Twitter Weather Project for CS6100 -  A Big Data Application to Explore How Twitter Users Talk About the Weather

### Install
------
1. Install npm (this will be different depending on your os)
2. Install vue tools
    - `npm install -g @vue/cli @vue/cli-init`
3. `cd frontend`
4. `npm install`

Virtual Environment:
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `deactivate`

Virtual Environment on Windows:
- `python3 -m venv venv`
- `cd venv/Scripts`
- `& .\activate`
- `pip install -r requirements.txt`
- `deactivate`

To run the back end:
`./startBack.sh`

Extra steps for windows:
$env:FLASK_APP = "./backend/run.py"
flash run

To run the front end (in a diff terminal from flask):
`cd frontend`
`npm run dev`
