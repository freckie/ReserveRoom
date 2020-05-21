import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import app

# Flask JWT
from flask_jwt_extended import JWTManager

jwt_manager = JWTManager(app)

# API
from flask_restful import Api
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