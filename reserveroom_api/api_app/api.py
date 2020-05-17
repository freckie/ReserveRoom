from flask import Flask
from flask_restful import Api

app = Flask(__name__)

from api_app.resources.auth import *
from api_app.resources.rooms import *
from api_app.resources.reservations import *

api = Api(app)

#api.add_resource(func, '/~')
