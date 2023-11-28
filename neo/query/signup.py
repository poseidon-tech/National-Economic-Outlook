from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
from flask import redirect
import neo.query.utils as utils

bp = Blueprint('signup', __name__, url_prefix='/signup')

@bp.route('', methods=['GET'])
def fetch_signup():

    user_name = request.args.get('user_name')
    password = request.args.get('password') 
    user_type = request.args.get("user_type")

    credentials = "SELECT user_name from login_table where user_name IN '{user_name}'"

    query = credentials.format(user_name = user_name)

    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close
    
    if len(result) == 0:

        insert = "INSERT INTO login_table (user_name, password, user_type) VALUES ('{user_name}', '{password}', '{user_type}')"

        query = insert.format(user_name = user_name, password = password, user_type = user_type)

        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        
        cursor.close

        output = {"Success":1}

    else:

    

        output = {"Success":0}

        #return redirect("/login")   
    
    return jsonify(output)