from flask_restful import Resource, reqparse, request

from api_app.api import app
from api_app.models.response import error_response, ok_response

# GET /rooms
class GETRooms(Resource):
    def get(self):
        body = request.get_json()
        return ok_response(body)

# GET /rooms/<room_id>
class GETRoomsDetail(Resource):
    def get(self, room_id):
        pass
