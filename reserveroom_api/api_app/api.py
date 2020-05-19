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
from api_app.resources.auth import POSTSignin, POSTResetPW, POSTSignup, POSTRefresh
from api_app.resources.rooms import *
from api_app.resources.reservations import GETReservations, POSTReservations, PUTReservations, DELETEReservations

api = Api(app)

# Auth
api.add_resource(POSTSignin, '/auth/signin')
api.add_resource(POSTResetPW, '/auth/resetpw')
api.add_resource(POSTSignup, '/auth/signup')
api.add_resource(POSTRefresh, '/auth/refresh')

# Rooms
api.add_resource(GETRooms, '/rooms')
api.add_resource(GETRoomsDetail, '/rooms/detail')
api.add_resource(GETRoomsAvailable, '/rooms/available')

# Reservations
api.add_resource(GETReservations, '/reservations')
api.add_resource(POSTReservations, '/reservations')
api.add_resource(PUTReservations, '/reservations/<reservation_id>')
api.add_resource(DELETEReservations, '/reservations/<reservation_id>')