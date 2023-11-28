from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint

bp = Blueprint('signup', __name__, url_prefix='/signup')


@bp.route('', methods=['POST'])
def fetch_signup():
    request_data = request.json

    username = request_data['username']
    password = request_data['password']
    user_type = 'user'

    credentials = """SELECT username from "HARSHITH.KUMAR".Users where username IN '{username}'"""

    query = credentials.format(username=username)

    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close
    
    if len(result) == 0:
        insert = """INSERT INTO "HARSHITH.KUMAR".Users (username, password, user_type) VALUES 
        ('{username}', '{password}', '{user_type}')"""

        query = insert.format(username=username, password=password, user_type=user_type)

        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        
        cursor.close

        output = {"Success": 1}
    else:
        output = {"Success": 0}
    
    return jsonify(output)
