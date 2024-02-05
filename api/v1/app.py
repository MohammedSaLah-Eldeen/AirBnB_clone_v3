#!/usr/bin/python3
"""
RESTAPI APP.
"""
import os
from api.v1.views import app_views
from flask import Flask
from models import storage
from werkzeug.exceptions import HTTPException


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    closes storage.
    """
    storage.close()


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global Route to handle All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000) 
    app.run(
        host=host,
        port=port,
        threaded=True
    )
