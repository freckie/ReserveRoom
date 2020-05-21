import sys
import json

# Initialize Flask app
from flask import Flask

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'reserveroom'

from api_app.db import DB

def load_config(filename):
    config = {}
    with open(filename, 'r', encoding='utf8') as f:
        config = json.load(f)
    return config

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_filename = sys.argv[1]
    else:
        config_filename = './config.json'
        
    # config
    config = load_config(config_filename)

    # DB connection
    app.db_driver = DB(config['db'])

    debug = True
    app.run(debug=debug, host='0.0.0.0', port=config['server']['port'])