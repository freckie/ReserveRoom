from flask_restful import Resource, reqparse, request
from flask import current_app as app

from api_app.models.response import error_response, ok_response
from api_app.utils import is_available

import datetime as dt
import itertools
# GET /rooms
class GETRooms(Resource):
    def get(self):
        # Parse body params
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('college_id', required=False, default=1, type=int)
            parser.add_argument('capacity', required=False, default=0, type=int)
            args = parser.parse_args()
        except:
            pass
        _college_id = args['college_id']
        _capacity = args['capacity']

        # Querying
        query = '''
            SELECT C.name, R.id, R.capacity
            FROM classrooms R, colleges C
            WHERE R.college_id=C.id
        '''
        all_rows = app.db_driver.execute_all(query) 

        query += 'AND R.college_id = ' + str(_college_id) + ' AND R.capacity >= ' + str(_capacity * 2)
        rows = app.db_driver.execute_all(query)


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
            print(row)
            result['rooms'].append({
                'college' : '전자정보대학',
                'classroom_id' : row,
                'capacity' : str(comb_dict[row] // 2)
            })
        return ok_response(result)

# GET /rooms/detail
class GETRoomsDetail(Resource):
    def get(self):
         # Parse body params
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('room_id', required=False, type=str)
            args = parser.parse_args()
        except:
            pass
        _room_id = args['room_id']
        # Querying
        query = '''
            SELECT subject, start_time, end_time
            FROM reservations
            WHERE classroom_id = %s
        '''
        
        rows = app.db_driver.execute_all(query,(_room_id))

         # Fetch
        result = {
            'times': []
        }
        for row in rows:
            result['times'].append({
                'subject': row['subject'],
                'start_time': row['start_time'].strftime('%Y-%m-%d %H:%M'),
                'end_time': row['end_time'].strftime('%Y-%m-%d %H:%M')
            })
        
        return ok_response(result)

# GET /rooms/available
class GETRoomsAvailable(Resource):
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
        query = '''
            SELECT start_time, end_time
            FROM reservations
            WHERE classroom_id = %s
        '''
        targetTuple = (_start_time,_end_time)
        timeList = []
        rows = app.db_driver.execute_all(query,(_room_id))
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