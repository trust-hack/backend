import os, sys

from flask import Flask, request
from flask_json import FlaskJSON, json_response

from dotenv import load_dotenv
load_dotenv()

from internal.database import Database
from tools import content

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
DBNAME = os.getenv("DBNAME")

if CONNECTION_STRING == None or DBNAME == None:
    print(content.EnvVarsNotFound.format("CONNECTION_STRING or DBNAME"))
    sys.exit(1)


app = Flask(__name__) # Main APP
FlaskJSON(app) # For JSON response

db = Database(CONNECTION_STRING, DBNAME)

@app.route('/', methods=["GET"])
def root():
    """
    Check status server
    """
    return json_response(server="active", routes=['%s' % rule for rule in app.url_map.iter_rules()])

@app.route('/database/ping', methods=["GET"])
def check_status_database():
    """
    Check status database
    """
    return json_response(database=db.ping())

@app.route('/user/login/<login>', methods=["GET"])
def login(login):
    """
    Simple login without sha256
    """
    if login is None:
        return json_response(status_=403, error=content.ErrorBodyLoginIsEmpty)

    return json_response(user=db.login_check(login))

@app.route('/user/signup', methods=["POST"])
def signup():
    """
    Simple signup without sha256

    Required: JSON login, password
    """
    try:
        payload = request.get_json()
        fname = payload["fname"]
        lname = payload["lname"]
        login = payload["login"]
        password = payload["password"]
        role = payload["role"]
        data = payload["data"]
        # TODO FIELDS
    except Exception as E:
        return json_response(status_=403, error=content.ErrorBodyJSON)

   
    if db.login_check(login):
        return json_response(status_=403, error=content.ErrorIsExists.format(login))
    else:
        db.sign_up({
            "fname": fname,
            "lname": lname,
            "login": login,
            "password": password, # Generate and check SHA256 on FRONTEND
            "role": role,
            "data": data
        })
        return json_response(created="ok")
    

# @app.route('/database/<data>/put', methods=["POST"])
# def data_put():
#     """
#     Put clean data to Database
#     """
#     data = request.get_json()
#     if data is None:
#         return json_response(status_=403, error=content.ErrorData)
#     return json_response(request=db.data_put(data=data))

@app.route('/database/<data>/get', methods=["GET"])
def data_get(data):
    """
    Get data from Database
    """
    filt = request.args.get("filter")
    return json_response(payload=db.data_get(data=data, filt=filt))

