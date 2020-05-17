import sys

from api_app.api import app

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = 8080

    debug = True
    app.run(debug=debug, host='0.0.0.0', port=port)
