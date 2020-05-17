from flask_restful import Resource, reqparse, request

from api_app.api import app
from api_app.models.response import error_response, ok_response

# GET /rooms
class GETRooms(Resource):
    def get(self):
        # Parse body params
        # try:
        #     parser = reqparse.RequestParser()
        #     parser.add_argument('', required=False, type='', help='')
        # except:
        #     pass

        # Querying
        query = '''
            SELECT C.name, R.id, R.capacity
            FROM classrooms R, colleges C
            WHERE R.college_id=C.id;
        '''
        rows = app.db_driver.execute_all(query)

        # Fetch
        rooms = []
        for row in rows:
            rooms.append({
                'college': row[0],
                'classroom_id': row[1],
                'capacity': row[2]
            })
        
        return ok_response(rooms)

# GET /rooms/<room_id>
class GETRoomsDetail(Resource):
    def get(self, room_id):
        pass
