import datetime
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_claims

from api_app.utils import is_available
from api_app.api import app, jwt_manager
from api_app.models.response import error_response, ok_response

# GET /reservations
class GETReservations(Resource):

    @jwt_required
    def get(self):
        # Handle query parameters
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
                'start_time': row['start_time'].strftime('%Y-%m-%d %H:%M'),
                'end_time': row['end_time'].strftime('%Y-%m-%d %H:%M'),
                'subject': row['subject']  
            })
        result['reservation_count'] = len(result['reservations'])

        return ok_response(result)

# POST /reservations
class POSTReservations(Resource):

    @jwt_required
    def post(self):
        if not request.is_json:
            return error_response(400, 'JSON 형식으로 전달해주세요.')
        
        claims = get_jwt_claims()

        # Handle body parameters
        try:
            user_email = request.json.get('user_email', None)
            start_time = request.json.get('start_time', None)
            end_time = request.json.get('end_time', None)
            classroom_id = request.json.get('classroom_id', None)
            subject = request.json.get('subject', None)
            if not user_email:
                user_email = claims['email']
            if not start_time:
                return error_response(400, 'start_time을 전달해주세요.')
            else:
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            if not end_time:
                return error_response(400, 'end_time을 전달해주세요.')
            else:
                end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            if not classroom_id:
                return error_response(400, 'classroom_id를 전달해주세요.')
            if not subject:
                return error_response(400, 'subject를 전달해주세요.')
        except Exception as exc:
            return error_response(400, 'JSON 파싱 에러가 발생했습니다 : ' + str(exc))

        # Querying
        sql = 'INSERT INTO reservations (classroom_id, user_email, start_time, end_time, subject) VALUES (%s, %s, %s, %s, %s);'
        try:
            result = app.db_driver.execute(sql, (classroom_id, user_email, start_time, end_time, subject))
            app.db_driver.commit()
        except Exception as exc:
            return error_response(500, str(exc))

        return ok_response({'affected_rows': result})

# PUT /reservations/<reservation_id>
class PUTReservations(Resource):

    @jwt_required
    def put(self, reservation_id):
        claims = get_jwt_claims()

        # Get target reservation
        sql = 'SELECT count(user_email) "count", user_email FROM reservations WHERE id=%s;'
        try:
            result = app.db_driver.execute_one(sql, (reservation_id))
        except Exception as exc:
            return error_response(404, "해당 예약 건을 찾을 수 없습니다. " + str(exc))
        if result['count'] == 0:
            return error_response(404, "해당 예약 건을 찾을 수 없습니다.")

        # Check level
        if claims['level'] != 9:
            if claims['email'] != result['user_email']:
                return error_response(403, "관리자 혹은 예약 당사자만 수정이 가능합니다.")

        # Handle body parameters
        if not request.is_json:
            return error_response(400, 'JSON 형식으로 전달해주세요.')

        try:
            start_time = request.json.get('start_time', None)
            end_time = request.json.get('end_time', None)
            classroom_id = request.json.get('classroom_id', None)
            subject = request.json.get('subject', None)
            if not start_time:
                return error_response(400, 'start_time을 전달해주세요.')
            else:
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            if not end_time:
                return error_response(400, 'end_time을 전달해주세요.')
            else:
                end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            if not classroom_id:
                return error_response(400, 'classroom_id를 전달해주세요.')
            if not subject:
                return error_response(400, 'subject를 전달해주세요.')
        except Exception as exc:
            return error_response(400, 'JSON 파싱 에러가 발생했습니다 : ' + str(exc))

        # Querying
        sql = 'UPDATE reservations SET start_time=%s, end_time=%s, classroom_id=%s, subject=%s WHERE id=%s;'
        try:
            app.db_driver.execute(sql, (start_time, end_time, classroom_id, subject, reservation_id))
            app.db_driver.commit()
        except Exception as exc:
            return error_response(500, str(exc))
        
        return ok_response(result)

# DELETE /reservations/<reservation_id>
class DELETEReservations(Resource):

    @jwt_required
    def delete(self, reservation_id):
        claims = get_jwt_claims()

        # Get target reservation
        sql = 'SELECT count(user_email) "count", user_email FROM reservations WHERE id=%s;'
        try:
            result = app.db_driver.execute_one(sql, (reservation_id))
        except Exception as exc:
            return error_response(404, "해당 예약 건을 찾을 수 없습니다. " + str(exc))
        if result['count'] == 0:
            return error_response(404, "해당 예약 건을 찾을 수 없습니다.")

        # Check level
        if claims['level'] != 9:
            if claims['email'] != result['user_email']:
                return error_response(403, "관리자 혹은 예약 당사자만 취소가 가능합니다.")

        # Querying
        sql = 'DELETE FROM reservations WHERE id=%s;'
        try:
            result = app.db_driver.execute(sql, (reservation_id))
            app.db_driver.commit()
        except Exception as exc:
            return error_response(500, str(exc))
        if result != 1:
            return error_response(500, "해당 요청 처리에 실패하였습니다.")
        
        return ok_response(None)