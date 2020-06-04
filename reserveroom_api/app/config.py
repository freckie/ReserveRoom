db = {
    'user'     : 'root',
    'password' : 'dasomDASOM',
    'host'     : '52.79.91.175',
    'port'     : 3306,
    'database' : 'reserveroom'
}
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"