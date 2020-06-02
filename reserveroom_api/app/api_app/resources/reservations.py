import datetime
from flask import current_app as app
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_cors import cross_origin

from api_app.utils import is_available
from api_app.models.response import error_response, ok_response
from sqlalchemy import text

# GET /reservations
class GETReservations(Resource):

    @jwt_required
    @cross_origin()
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

        # sql = '''
        #     SELECT R.id "id", R.classroom_id "classroom_id", CL.id "college_id", CL.name "college_name", 
        #         R.user_email "user_email", U.name "user_name", R.start_time "start_time", R.end_Time "end_time", R.subject "subject"
        #     FROM reservations R, users U, colleges CL, classrooms CR
        #     WHERE R.user_email=U.email
        #         AND R.classroom_id=CR.id
        #         AND CR.college_id=CL.id
        #         {}
        #         {}
        #     ORDER BY id DESC;
        # '''.format(_sql_email, _sql_query)
        # rows = app.db_driver.execute_all(sql)

        rows = app.database.execute(text('''
            SELECT R.id id, R.classroom_id classroom_id, CL.id college_id, CL.name college_name, 
                R.user_email user_email, U.name user_name, R.start_time start_time, R.end_Time end_time, R.subject subject
            FROM reservations R, users U, colleges CL, classrooms CR
            WHERE R.user_email=U.email
                AND R.classroom_id=CR.id
                AND CR.college_id=CL.id
                {}
                {}
            ORDER BY id DESC;
        '''.format(_sql_email,_sql_query)),{
        }).fetchall()

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

# GET /reservations/<reservation_id>
class GETReservationsDetail(Resource):

    @jwt_required
    @cross_origin()
    def get(self, reservation_id):
        # Querying
        # sql = '''
        #     SELECT R.id "reservation_id", R.classroom_id, U.email "user_email", U.name "user_name", R.start_time, R.end_time, R.subject
        #     FROM reservations R, users U
        #     WHERE R.user_email=U.email
        #         AND R.id=%s;
        # '''
        # row = app.db_driver.execute_one(sql, (reservation_id))
       
        row = app.database.execute(text('''
            SELECT R.id reservation_id, R.classroom_id, U.email user_email, U.name user_name, R.start_time, R.end_time, R.subject
            FROM reservations R, users U
            WHERE R.user_email=U.email
            AND R.id= :id;
        '''),{
            'id' : reservation_id
        }).fetchone()
        result = {
            'reservation': {}
        }
        result['reservation'] = {
            'reservation_id': row['reservation_id'],
            'classroom_id': row['classroom_id'],
            'user_name': row['user_name'],
            'user_email': row['user_email'],
            'start_time': row['start_time'].strftime('%Y-%m-%d %H:%M'),
            'end_time': row['end_time'].strftime('%Y-%m-%d %H:%M'),
            'subject': row['subject']  
        }

        return ok_response(result)

# POST /reservations
class POSTReservations(Resource):

    @jwt_required
    @cross_origin()
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
                is_user = True
            else:
                is_user = False
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
        if not is_user:
            emailList = []
            rows = app.database.execute(text('''
                SELECT *
                FROM users
            '''),{}).fetchall()
            for row in rows:
                emailList.append(row['email'])
            if user_email not in emailList:
                return error_response(400, '유효하지 않은 이메일입니다.')
            # is_available
        # sql = '''
        #     SELECT start_time, end_time
        #     FROM reservations
        #     WHERE classroom_id = %s
        # '''
        # rows = app.db_driver.execute_all(sql,(classroom_id))
        targetTuple = (start_time, end_time)
        timeList = []
        rows = app.database.execute(text('''
            SELECT start_time, end_time
            FROM reservations
            WHERE classroom_id = :classroom_id
        '''),{
            'classroom_id' : classroom_id
        }).fetchall()
        for row in rows:
            tmpList = []
            for value in row.values():
                tmpList.append(value)
            timeList.append(tmpList)
        available = is_available(timeList,targetTuple)
        if available == False:
            return error_response(400, '예약 불가능한 시간입니다.')
        # Insert Querying
        # sql = 'INSERT INTO reservations (classroom_id, user_email, start_time, end_time, subject) VALUES (%s, %s, %s, %s, %s);'
        # try:
        #     result = app.db_driver.execute(sql, (classroom_id, user_email, start_time, end_time, subject))
        #     app.db_driver.commit()
        
        try:
            app.database.execute(text('''
            INSERT INTO reservations (classroom_id, user_email, start_time, end_time, subject) VALUES ( :classroom_id, :user_email, :start_time, :end_time, :subject);
            '''),{
                'classroom_id' : classroom_id,
                'user_email' : user_email,
                'start_time' : start_time,
                'end_time' : end_time,
                'subject' : subject
            }).fetchall()
        except Exception as exc:
            return error_response(500, str(exc))

        return ok_response(None)

# PUT /reservations/<reservation_id>
class PUTReservations(Resource):

    @jwt_required
    @cross_origin()
    def put(self, reservation_id):
        claims = get_jwt_claims()

        # Get target reservation
        # sql = 'SELECT count(user_email) "count", user_email FROM reservations WHERE id=%s;'
        # try:
        #     result = app.db_driver.execute_one(sql, (reservation_id))
        try:
            result = app.database.execute(text('''
            SELECT count(user_email) count, user_email 
            FROM reservations WHERE id= :reservation_id
            '''),{
            'reservation_id' : reservation_id
            }).fetchone()
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
            origin_start_time = request.json.get('origin_start_time', None)
            origin_end_time = request.json.get('origin_end_time', None)
            if not start_time:
                return error_response(400, 'start_time을 전달해주세요.')
            else:
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            if not end_time:
                return error_response(400, 'end_time을 전달해주세요.')
            else:
                end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            if not origin_start_time:
                return error_response(400, 'origin_start_time을 전달해주세요.')
            else:
                origin_start_time = datetime.datetime.strptime(origin_start_time, '%Y-%m-%d %H:%M')
            if not origin_end_time:
                return error_response(400, 'origin_end_time 전달해주세요.')
            else:
                origin_end_time = datetime.datetime.strptime(origin_end_time, '%Y-%m-%d %H:%M')
            if not classroom_id:
                return error_response(400, 'classroom_id를 전달해주세요.')
            if not subject:
                return error_response(400, 'subject를 전달해주세요.')
        except Exception as exc:
            return error_response(400, 'JSON 파싱 에러가 발생했습니다 : ' + str(exc))
        # is_available
        # sql = '''
        #     SELECT start_time, end_time
        #     FROM reservations
        #     WHERE classroom_id = %s
        # '''
        # rows = app.db_driver.execute_all(sql,(classroom_id))
        targetTuple = (start_time, end_time)
        originTuple = [origin_start_time, origin_end_time]
        timeList = []
        rows = app.database.execute(text('''
            SELECT start_time, end_time
            FROM reservations
            WHERE classroom_id = :classroom_id
            '''),{
            'classroom_id' : classroom_id
            }).fetchall()
        for row in rows:
            tmpList = []
            for value in row.values():
                tmpList.append(value)
            timeList.append(tmpList)
        timeList.remove(originTuple)
        available = is_available(timeList,targetTuple)
        if available == False:
            return error_response(400, '예약 불가능한 시간입니다.')
 
        # Querying
        # sql = 'UPDATE reservations SET start_time=%s, end_time=%s, classroom_id=%s, subject=%s WHERE id=%s;'
        # try:
        #     app.db_driver.execute(sql, (start_time, end_time, classroom_id, subject, reservation_id))
        #     app.db_driver.commit()
        try:
            app.database.execute(text('''
            UPDATE reservations SET start_time= :start_time, end_time= :end_time, classroom_id= :classroom_id, subject= :subject WHERE id= :reservation_id;
            '''),{
            'start_time' : start_time,
            'end_time' : end_time,
            'classroom_id' : classroom_id,
            'subject' : subject,
            'reservation_id' : reservation_id
            })
        except Exception as exc:
            return error_response(500, str(exc))
        
        return ok_response(None)

# DELETE /reservations/<reservation_id>
class DELETEReservations(Resource):

    @jwt_required
    @cross_origin()
    def delete(self, reservation_id):
        claims = get_jwt_claims()

        # Get target reservation
        # sql = 'SELECT count(user_email) "count", user_email FROM reservations WHERE id=%s;'
        # try:
        #     result = app.db_driver.execute_one(sql, (reservation_id))
        try:
            result = app.database.execute(text('''
            SELECT count(user_email) count, user_email 
            FROM reservations 
            WHERE id= :reservation_id;
            '''),{
            'reservation_id' : reservation_id
            }).fetchone()
        except Exception as exc:
            return error_response(404, "해당 예약 건을 찾을 수 없습니다. " + str(exc))
        if result['count'] == 0:
            return error_response(404, "해당 예약 건을 찾을 수 없습니다.")

        # Check level
        if claims['level'] != 9:
            if claims['email'] != result['user_email']:
                return error_response(403, "관리자 혹은 예약 당사자만 취소가 가능합니다.")

        # Querying
        # sql = 'DELETE FROM reservations WHERE id=%s;'
        # try:
        #     result = app.db_driver.execute(sql, (reservation_id))
        #     app.db_driver.commit()
        try:
            result = app.database.execute(text('''
            DELETE FROM reservations 
            WHERE id= :reservation_id
            '''),{
            'reservation_id' : reservation_id
            })

        except Exception as exc:
            return error_response(500, str(exc))

        
        return ok_response(None)

# POST /reservations2
class POSTReservations2(Resource):

    @jwt_required
    @cross_origin()
    def post(self):
        if not request.is_json:
            return error_response(400, 'JSON 형식으로 전달해주세요.')
        claims = get_jwt_claims()
        reserveList = request.json.get('reservations',None)
        queryList = []

        # check each reservation
        for reserve in reserveList:
            tmpEmail = reserve['user_email']
            if not tmpEmail:
                tmpEmail = claims['email']
                is_user = True
            else:
                is_user = False
            start_time = datetime.datetime.strptime(reserve['start_time'], '%Y-%m-%d %H:%M')
            end_time = datetime.datetime.strptime(reserve['end_time'], '%Y-%m-%d %H:%M')
            tmpTarget = (start_time,end_time)
            tmpClassroom_id = reserve['classroom_id']
            tmpSubject = reserve['subject']
            tmpList = [tmpClassroom_id, tmpEmail, tmpTarget[0], tmpTarget[1], tmpSubject]
            queryList.append(tmpList)
            if not is_user:
                emailList = []
                rows = app.database.execute(text('''
                    SELECT *
                    FROM users
                    '''),{}).fetchall()
                for row in rows:
                    emailList.append(row['email'])
                if tmpEmail not in emailList:
                    return error_response(400, '유효하지 않은 이메일입니다.')
            # is_available
            # sql = '''
            #     SELECT start_time, end_time
            #     FROM reservations
            #     WHERE classroom_id = %s
            # '''
            # rows = app.db_driver.execute_all(sql,(tmpClassroom_id))
            rows = app.database.execute(text('''
            SELECT start_time, end_time
            FROM reservations
            WHERE classroom_id = :classroom_id
            '''),{
            'classroom_id' : tmpClassroom_id
            }).fetchall()
            timeList = []
            for row in rows:
                tmpList = []
                for value in row.values():
                    tmpList.append(value)
                timeList.append(tmpList)
            available = is_available(timeList,tmpTarget)
            if available == False:
                return error_response(400, '예약 불가능한 시간입니다.')
        # Insert Querying
        # sql = '''INSERT INTO reservations (classroom_id, user_email, start_time, end_time, subject) VALUES (%s,%s,%s,%s,%s),(%s,%s,%s,%s,%s);'''
        # try:
        #     result = app.db_driver.execute(sql, (queryList[0][0], queryList[0][1], queryList[0][2], queryList[0][3], queryList[0][4],
        #     queryList[1][0], queryList[1][1], queryList[1][2], queryList[1][3], queryList[1][4]))
        #     app.db_driver.commit()
        try:
            result = app.database.execute(text('''
            INSERT INTO reservations (classroom_id, user_email, start_time, end_time, subject) 
            VALUES ( :classroom_id1, :user_email1, :start_time1, :end_time1, :subject1),( :classroom_id2, :user_email2, :start_time2, :end_time2, :subject2)
            '''),{
            'classroom_id1' : queryList[0][0],
            'user_email1' : queryList[0][1],
            'start_time1' : queryList[0][2],
            'end_time1' : queryList[0][3],
            'subject1' : queryList[0][4],
            'classroom_id2' : queryList[1][0],
            'user_email2' : queryList[1][1],
            'start_time2' : queryList[1][2],
            'end_time2' : queryList[1][3],
            'subject2' : queryList[1][4]
            })
        except Exception as exc:
            return error_response(500, str(exc))

        return ok_response(None)
