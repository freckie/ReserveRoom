from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_claims

from api_app.api import app, jwt_manager
from api_app.models.response import error_response, ok_response

# GET /reservations
class GETReservations(Resource):

    @jwt_required
    def get(self):
        # Handle body parameters
        params = {
            'user_email': None,
            'query': None
        }
        if 'user_email' in request.args:
            params['user_email'] = request.args['user_email']
        if 'query' in request.args:
            params['query'] = request.args['query']

        # Querying
        _sql_email, _sql_query = '', ''
        if params['user_email'] is not None:
            _sql_email = ' AND R.user_email="{}" '.format(params['user_email'])
        
        if params['query'] is not None:
            _sql_query = ' AND (R.subject LIKE "%{}%" OR U.name LIKE "%{}%") '.format(params['query'], params['query'])

        sql = '''
            SELECT R.id "id", R.classroom_id "classroom_id", CL.id "college_id", CL.name "college_name", 
                R.user_email "user_email", U.name "user_name", R.start_time "start_time", R.end_Time "end_time", R.subject "subject"
            FROM reservations R, users U, colleges CL, classrooms CR
            WHERE R.user_email=U.email
                AND R.classroom_id=CR.id
                AND CR.college_id=CL.id
                {}
                {}
            ORDER BY id DESC;
        '''.format(_sql_email, _sql_query)
        rows = app.db_driver.execute_all(sql)

        result = {
            'reservation_count': 0,
            'reservations': []
        }
        for row in rows:
            result['reservations'].append({
                'reservation_id': row['id'],
                'classroom_id': row['classroom_id'],
                'college_id': row['college_id'],
                'college_name': row['college_name'],
                'user_email': row['user_email'],
                'user_name': row['user_name'],
                'start_time': row['start_time'],
                'end_time': row['end_time'],
                'subject': row['subject']  
            })
        result['reservation_count'] = len(result['reservations'])

        return ok_response(result)