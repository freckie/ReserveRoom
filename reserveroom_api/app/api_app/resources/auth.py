import bcrypt
from datetime import timedelta
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_claims,
    create_refresh_token, jwt_refresh_token_required
)
from flask_cors import cross_origin
from api_app.models.response import error_response, ok_response
from flask import current_app as app
from sqlalchemy import text
# POST /auth/signin
class POSTSignin(Resource):
    @cross_origin()
    def post(self):
        if not request.is_json:
            return error_response(400, 'JSON 형식으로 전달해주세요.')

        # Handle body parameters
        try:
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            if not email:
                return error_response(400, '이메일을 전달해주세요.')
            if not password:
                return error_response(400, '비밀번호를 전달해주세요.')
        except Exception as exc:
            return error_response(400, 'JSON 파싱 에러가 발생했습니다 : ' + str(exc))

        # Querying and check email & pw
        # query = '''SELECT count(email) AS counts, email, name, password, level 
        #         FROM users WHERE email=%s;'''
        # result = app.db_driver.execute_one(query, (email))
        result = app.database.execute(text('''
            SELECT count(email) AS counts, email, name, password, level 
            FROM users WHERE email= :email
        '''),{
            'email' : email
        }).fetchone()
        if int(result['counts']) == 0:
            return error_response(401, '이메일이 잘못되었습니다.')
        if result['level'] != 0: # Need to change pw (first login)
            try:
                if not bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
                    return error_response(401, '비밀번호가 잘못되었습니다.')
            except Exception as exc:
                return error_response(401, '비밀번호가 잘못되었습니다 : ' + str(exc))
        else:
            if password != '1111':
                return error_response(401, '비밀번호가 잘못되었습니다.')
        
        user_claims = {
            'email': result['email'],
            'name': result['name'],
            'level': int(result['level'])
        }
        access_token = create_access_token(
            identity=email,
            expires_delta=timedelta(minutes=20),
            user_claims=user_claims
        )
        refresh_token = create_refresh_token(
            identity=email,
            user_claims=user_claims
        )

        return ok_response({
            'access_token': access_token,
            'refresh_token': refresh_token
        })

# POST /auth/resetpw
class POSTResetPW(Resource):

    @jwt_required
    @cross_origin()
    def post(self):
        if not request.is_json:
            return error_response(400, 'JSON 형식으로 전달해주세요.')

        # Handle body parameters
        try:
            new_password = request.json.get('new_password', None)
            if not new_password:
                return error_response(400, '새 비밀번호를 전달해주세요.')
        except Exception as exc:
            return error_response(400, 'JSON 파싱 에러가 발생했습니다 : ' + str(exc))

        # Parse user claims
        claims = get_jwt_claims()

        # Encrypt new password
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        # Querying
        new_level = 0
        if claims['level'] == 0 or claims['level'] == 1:
            new_level = 1
        elif claims['level'] == 9:
            new_level = 9
        # query = 'UPDATE users SET password=%s, level=%s WHERE email=%s;'
        # try:
        #     app.db_driver.execute(query, (hashed, int(new_level), claims['email']))
        #     app.db_driver.commit()
        try:
            app.database.execute(text('''
            UPDATE users SET password= :password, level= :level WHERE email= :email
            FROM users WHERE email= :email
            '''),{
            'password' : hashed,
            'level' : new_level,
            'email' : claims['email']
            })
        except Exception as exc:
            return error_response(500, str(exc))

        return ok_response(None)

# POST /auth/signup
class POSTSignup(Resource):
    @cross_origin()
    def post(self):
        if not request.is_json:
            return error_response(400, 'JSON 형식으로 전달해주세요.')

        # Handle body parameters
        try:
            email = request.json.get('email', None)
            name = request.json.get('name', None)
            if not email:
                return error_response(400, '이메일을 전달해주세요.')
            if not name:
                return error_response(400, '이름을 전달해주세요.')
        except Exception as exc:
            return error_response(400, 'JSON 파싱 에러가 발생했습니다 : ' + str(exc))
        
        # Querying
        # query = 'INSERT INTO users (email, name) VALUES (%s, %s);'
        try:
            result = app.database.execute(text('''
                INSERT INTO users (email, name) 
                VALUES (:email, :name)
            '''),{
                'email' : email,
                'name' : name
            })
            # result = app.db_driver.execute_one(query, (email, name))
            # app.db_driver.commit()
        except Exception as exc:
            return error_response(500, str(exc))

        return ok_response(None)

# POST /auth/refresh
class POSTRefresh(Resource):

    @jwt_refresh_token_required
    @cross_origin()
    def post(self):
        rtoken = request.headers['Authorization'].split(' ')[1]

        user_claims = get_jwt_claims()
        access_token = create_access_token(
            identity=user_claims['email'],
            expires_delta=timedelta(minutes=20),
            user_claims=user_claims
        )
        refresh_token = rtoken

        return ok_response({
            'access_token': access_token,
            'refresh_token': refresh_token
        })