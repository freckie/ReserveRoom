import sys
import json

# config
def load_config(filename):
    config = {}
    with open(filename, 'r', encoding='utf8') as f:
        config = json.load(f)
    return config

config = load_config('./config.json')

# Initialize Flask app
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JWT_SECRET_KEY'] = 'reserveroom'
if not config['server']['debug']:
    app.config['SERVER_NAME'] = '{}:{}'.format(config['server']['server_name'], str(config['server']['port']))

# DB connection
from api_app.db import DB
app.db_driver = DB(config['db'])

# JWT Manager
from flask_jwt_extended import JWTManager
jwt_manager = JWTManager(app)
app.jwt_manager = jwt_manager

# API
from api_app.api import build_api
build_api(app)

if __name__ == "__main__":
    if config['server']['debug']:
        app.run(debug=True, host='0.0.0.0', port=config['server']['port'])
