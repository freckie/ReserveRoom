import pymysql
from flask import g

class DB():
    def __init__(self, db_config):
        self.db = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            passwd=db_config['passwd'],
            db=db_config['db'],
            charset='utf8'
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    def execute(self, query, args):
        '''
        args: query params, must be tuple
        '''
        self.cursor.execute(query, args)

    def execute_one(self, query, args):
        '''
        args: query params, must be tuple
        '''
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def execute_all(self, query, args):
        '''
        args: query params, must be tuple
        '''
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
