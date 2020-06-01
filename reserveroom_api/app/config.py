db = {
    'user'     : 'root',
    'password' : 'dasomDASOM',
    'host'     : '15.164.93.91',
    'port'     : 3306,
    'database' : 'reserveroom'
}
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"