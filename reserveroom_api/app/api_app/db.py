import pymysql
from flask import g
from threading import Lock

class DB():
    def __init__(self, db_config):
        self.config = db_config
        self.lock = Lock()
        self.db = pymysql.connect(
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            passwd=self.config['passwd'],
            db=self.config['db'],
            charset='utf8'
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def reconnect(self):
        if not self.db.open:
            self.cursor.close()
            self.__init__(self.config)
    
    def execute(self, query, args=None):
        '''
        args: query params, must be tuple
        '''
        self.reconnect()
        with self.lock:
            if args is not None:
                result = self.cursor.execute(query, args)
            else:
                result = self.cursor.execute(query)
        return result

    def execute_one(self, query, args=None):
        '''
        args: query params, must be tuple
        '''
        self.reconnect()
        with self.lock:
            if args is not None:
                self.cursor.execute(query, args)
            else:
                self.cursor.execute(query)
            row = self.cursor.fetchone()
        return row

    def execute_all(self, query, args=None):
        '''
        args: query params, must be tuple
        '''
        self.reconnect()
        with self.lock:
            if args is not None:
                self.cursor.execute(query, args)
            else:
                self.cursor.execute(query)
            row = self.cursor.fetchall()
        return row

    def commit(self):
        with self.lock:
            self.db.commit()
