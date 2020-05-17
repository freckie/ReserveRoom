import sys
from flask import Flask
from flask_restful import Resource, Api

# Initialize Flask instance
app = Flask(__name__)
api = Api(app)

# Routing

# Main
if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = 8080

    debug = True
    app.run(debug=debug, host='0.0.0.0', port=port)
