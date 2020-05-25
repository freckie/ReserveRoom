# API
from flask_restful import Api
from api_app.resources.auth import POSTSignin, POSTResetPW, POSTSignup, POSTRefresh
from api_app.resources.rooms import *
from api_app.resources.reservations import GETReservations, GETReservationsDetail, POSTReservations, POSTReservations2, PUTReservations, DELETEReservations

def build_api(app):
    api = Api()

    # Auth
    api.add_resource(POSTSignin, '/api/auth/signin')
    api.add_resource(POSTResetPW, '/api/auth/resetpw')
    api.add_resource(POSTSignup, '/api/auth/signup')
    api.add_resource(POSTRefresh, '/api/auth/refresh')

    # Rooms
    api.add_resource(GETRooms, '/api/rooms')
    api.add_resource(GETRoomsDetail, '/api/rooms/detail')
    api.add_resource(GETRoomsAvailable, '/api/rooms/available')

    # Reservations
    api.add_resource(GETReservations, '/api/reservations')
    api.add_resource(GETReservations, '/api/reservations/<reservation_id>')
    api.add_resource(POSTReservations, '/api/reservations')
    api.add_resource(POSTReservations2, '/api/reservations2')
    api.add_resource(PUTReservations, '/api/reservations/<reservation_id>')
    api.add_resource(DELETEReservations, '/api/reservations/<reservation_id>')

    api.init_app(app)
    return api