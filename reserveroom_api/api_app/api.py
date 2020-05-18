# Initialize Flask app
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'reserveroom'

# DB Connection
from api_app.db import DB

def connect_db(db_config):
    app.db_driver = DB(db_config)

# Flask JWT
from flask_jwt_extended import JWTManager

jwt_manager = JWTManager(app)

# API
from api_app.resources.auth import *
from api_app.resources.rooms import *
from api_app.resources.reservations import *

api = Api(app)

api.add_resource(GETRooms, '/rooms')
