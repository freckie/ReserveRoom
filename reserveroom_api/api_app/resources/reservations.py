from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_claims

from api_app.api import app, jwt_manager
from api_app.models.response import error_response, ok_response

# GET /reservations
class GETReservations(Resource):

    @jwt_required
    def get(self):
        # Handle body parameters

        # Querying
        query = '''
            SELECT R.id, R.classroom_id, C.id, C.name, R.user_email, U.name, R.start_time, R.end_Time, R.subject
            FROM reservations R, users U, colleges C
            WHERE R.user_email=U.email
                AND R.classroom_id=C.id;
        '''
        rows = app.db_driver.execute_all(query)

        result = {
            'reservation_count': 0,
            'reservations': []
        }
        for row in rows:
            result['reservations'].append({
                'reservation_id': row['R.id'],
                'classroom_id': row['R.classroom_id'],
                'college_id': row['C.id'],
                'college_name': row['C.name'],
                'user_email': row['R.user_email'],
                'user_name': row['U.name'],
                'start_time': row['R.start_time'],
                'end_time': row['R.end_time'],
                'subject': row['R.subject']  
            })
        result['reservation_count'] = len(result['reservation'])

        return ok_response(result)