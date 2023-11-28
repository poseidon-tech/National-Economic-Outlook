from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
import neo.query.utils as utils

bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('', methods=['GET'])
def fetch_login():
    user_name = request.args.get('username')
    password = request.args.get('password') 

    print(user_name,password)
    
    login_credentials = "SELECT user_name from login_table where user_name IN '{user_name}' AND password IN '{password}'"

    query = login_credentials.format(user_name = user_name,password = password)

    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close
    
    if len(result) == 0:

        output = {"Success":0}

    else:

        output = {"Success":1}


    
    return jsonify(output)