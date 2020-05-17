from flask_restful import Resource, reqparse, request

from api_app.api import app

# GET /rooms
class GETRooms(Resource):
    def get(self):
        body = request.get_json()
        return body

# GET /rooms/<room_id>
class GETRoomsDetail(Resource):
    def get(self, room_id):
        pass
