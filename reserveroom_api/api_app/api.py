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
from api_app.resources.auth import POSTSignin, POSTResetPW, POSTSignup
from api_app.resources.rooms import *
from api_app.resources.reservations import GETReservations

api = Api(app)

# Auth
api.add_resource(POSTSignin, '/auth/signin')
api.add_resource(POSTResetPW, '/auth/resetpw')
api.add_resource(POSTSignup, '/auth/signup')

# Rooms
api.add_resource(GETRooms, '/rooms')

# Reservations
api.add_resource(GETReservations, '/reservations')