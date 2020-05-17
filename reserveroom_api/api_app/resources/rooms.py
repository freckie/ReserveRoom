from flask_restful import Resource, reqparse, request

from api_app.api import app
from api_app.models.response import error_response, ok_response

# GET /rooms
class GETRooms(Resource):
    def get(self):
        # Parse body params
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('college_id', required=False, type=int)
            parser.add_argument('capacity', required=False, type=int)
            args = parser.parse_args()
        except:
            pass
        _college_id = args['college_id']
        _capacity = args['capacity']
        print(_college_id)
        print(_capacity)
        # Querying
        query = '''
            SELECT C.name, R.id, R.capacity
            FROM classrooms R, colleges C
            WHERE R.college_id=C.id
        '''
        query += 'AND R.college_id = ' + str(_college_id) + ' AND R.capacity > ' + str(_capacity * 2)

        rows = app.db_driver.execute_all(query)

        # Fetch
        result = {
            'rooms': []
        }
        for row in rows:
            result['rooms'].append({
                'college': row['name'],
                'classroom_id': row['id'],
                'capacity': row['capacity']
            })
        
        return ok_response(result)

# GET /rooms/<room_id>
class GETRoomsDetail(Resource):
    def get(self, room_id):
        pass
