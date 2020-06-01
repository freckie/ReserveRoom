from flask_restful import Resource, reqparse, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_cors import cross_origin

from api_app.models.response import error_response, ok_response
from api_app.utils import is_available

import datetime as dt
import itertools
from sqlalchemy import text
# GET /rooms
class GETRooms(Resource):

    @jwt_required
    @cross_origin()
    def get(self):
        # Parse body params

        parser = reqparse.RequestParser()
        parser.add_argument('college_id', required=False, default=1, type=int)
        parser.add_argument('capacity', required=False, default=0, type=int)
        args = parser.parse_args()

        _college_id = args['college_id']
        _capacity = args['capacity']

        # Querying
        query = '''
            SELECT C.name, R.id, R.capacity
            FROM classrooms R, colleges C
            WHERE R.college_id=C.id
        '''
        # all_rows = app.db_driver.execute_all(query) 
        all_rows = app.database.execute(text('''
            SELECT C.name, R.id, R.capacity
            FROM classrooms R, colleges C
            WHERE R.college_id=C.id
            '''),{
            }).fetchall()
        query += 'AND R.college_id = ' + str(_college_id) + ' AND R.capacity >= ' + str(_capacity * 2)
        # rows = app.db_driver.execute_all(query)
        rows = app.database.execute(text(query),{
        }).fetchall()

        class_dict = {}
        name_list = []
        #호수별 인원수 저장
        for row in all_rows:
            if row['id'] not in class_dict:
                class_dict[row['id']] = row['capacity']
            name_list.append(row['id'])
        #조합 구하기
        class_combinations = itertools.combinations(name_list,2)
        #조합별 인원수 계산 저장
        comb_dict = {}
        for combination in class_combinations:
            comb_name = combination[0]+' '+combination[1]
            if comb_name not in comb_dict:
                tmp = int(class_dict[combination[0]]) + int(class_dict[combination[1]])
                if tmp >= _capacity * 2:
                    comb_dict[comb_name] = tmp
        

        # Fetch
        result = {
            'rooms': []
        }
        for row in rows:
            result['rooms'].append({
                'college': row['name'],
                'classroom_id': row['id'],
                'capacity': str(int(row['capacity'])//2)
            })
        for row in comb_dict:
            result['rooms'].append({
                'college' : '전자정보대학',
                'classroom_id' : row,
                'capacity' : str(comb_dict[row] // 2)
            })
        return ok_response(result)

# GET /rooms/detail
class GETRoomsDetail(Resource):

    @jwt_required
    @cross_origin()
    def get(self):
         # Parse body params
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('room_id', required=False, type=str)
            args = parser.parse_args()
        except:
            pass
        _room_id = args['room_id']
        roomList = list(_room_id.split())
        # 1 room
        if len(roomList) == 1:
            # query = '''
            #     SELECT start_time, end_time
            #     FROM reservations
            #     WHERE classroom_id = %s
            #     ORDER BY start_time
            # ''' 
            # rows = app.db_driver.execute_all(query,(_room_id))  
            rows = app.database.execute(text('''
                SELECT start_time, end_time
                FROM reservations
                WHERE classroom_id = :classroom_id
                ORDER BY start_time
            '''),{
            'classroom_id' : _room_id
            }).fetchall() 
        # 2 rooms
        elif len(roomList) == 2:
            # query = '''
            #     SELECT DISTINCT start_time, end_time
            #     FROM reservations
            #     WHERE classroom_id in (%s, %s)
            #     ORDER BY start_time
            # '''
            # rows = app.db_driver.execute_all(query,(roomList[0],roomList[1]))
            rows = app.database.execute(text('''
                SELECT DISTINCT start_time, end_time
                FROM reservations
                WHERE classroom_id in (:room1, :room2)
                ORDER BY start_time
            '''),{
            'room1' : roomList[0],
            'room2' : roomList[1]
            }).fetchall() 

         # Fetch
        result = {
            'times': []
        }
        for row in rows:
            result['times'].append({
                'start_time': row['start_time'].strftime('%Y-%m-%d %H:%M'),
                'end_time': row['end_time'].strftime('%Y-%m-%d %H:%M')
            })
        
        return ok_response(result)

# GET /rooms/available
class GETRoomsAvailable(Resource):

    @jwt_required
    @cross_origin()
    def get(self):
         # Parse body params
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('room_id', required=False, type=str)
            parser.add_argument('start_time',required=True, type=str)
            parser.add_argument('end_time',required=True, type=str)
            args = parser.parse_args()
        except:
            pass
        _room_id = args['room_id']
        _start_time = dt.datetime.strptime(args['start_time'],'%Y-%m-%d %H:%M')
        _end_time = dt.datetime.strptime(args['end_time'],'%Y-%m-%d %H:%M')

        # Querying
        # query = '''
        #     SELECT start_time, end_time
        #     FROM reservations
        #     WHERE classroom_id = %s
        # '''
        # rows = app.db_driver.execute_all(query,(_room_id))
        targetTuple = (_start_time,_end_time)
        timeList = []
        rows = app.database.execute(text('''
            SELECT start_time, end_time
            FROM reservations
            WHERE classroom_id = :classroom_id
        '''),{
                'classroom_id' : _room_id
            }).fetchall() 
        for row in rows:
            tmpList = []
            for value in row.values():
                tmpList.append(value)
            timeList.append(tmpList)
        available = is_available(timeList,targetTuple)
                
         # Fetch
        result = {
            'available': []
        }
        result['available'] = available
        
        return ok_response(result)