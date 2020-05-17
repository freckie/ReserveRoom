import sys

from api_app.api import app, connect_db

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = 8080

    # connect_db({
    #     'host': '13.125.227.113',
    #     'port': 3306,
    #     'user': 'newuser',
    #     'db': 'reserveroom',
    #     'passwd': 'password'
    # })

    debug = True
    app.run(debug=debug, host='0.0.0.0', port=port)
