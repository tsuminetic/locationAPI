from app import app
from flask import jsonify
from werkzeug.exceptions import HTTPException
from marshmallow.exceptions import ValidationError
from apis.v1 import initialize_routes_v1
from apis.v2 import initialize_routes_v2
initialize_routes_v1(app)
initialize_routes_v2(app)

@app.errorhandler(Exception)
def handle_bad_request(e):
    http_status_code = 500
    if isinstance(e,(HTTPException,)):
        http_status_code=e.code
        response = {
            "message":e.description,
            "code":e.code
        }
    elif isinstance(e,(ValidationError,)):
        http_status_code=400
        response = {
            "messages":e.messages,
        }
    else:
        response = {
            "message":e.args[0],
        }
    return jsonify(response), http_status_code

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')