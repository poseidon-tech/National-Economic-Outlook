from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
import neo.query.utils as utils

bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('', methods=['POST'])
def fetch_login():
    request_data = request.json

    username = request_data['username']
    password = request_data['password']
    
    login = """SELECT username from HARSHITH.KUMAR".Users where username IN '{username}' AND password IN 
    '{password}'"""

    query = login.format(username=username, password=password)

    conn = app.config['DB_CONN']
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close
    
    if len(result) == 0:
        output = {"Success": 0}
    else:
        output = {"Success": 1}

    return jsonify(output)