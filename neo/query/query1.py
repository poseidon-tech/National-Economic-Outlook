from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
import neo.query.utils as utils

bp = Blueprint('query1', __name__, url_prefix='/query1')


# Common route to get states for all queries. Move to a common blueprint if time permits
@bp.route('/get_all_states', methods=['GET'])
def get_all_states():
    conn = app.config['DB_CONN']
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name
    FROM "HARSHITH.KUMAR".State
    """)

    results = cursor.fetchall()
    cursor.close()
    for row in results:
        print(row)

    return jsonify({"list_of_states": results})


# TODO: Make a common function that accepts table names and returns min, max of all tables
@bp.route('/year_range', methods=['GET'])
def get_query1_range():
    conn = app.config['DB_CONN']
    cursor = conn.cursor()
    cursor.execute("""
    SELECT MAX(min), MIN(max) 
    FROM
        (SELECT MAX(year) as max, MIN(year) as min
        FROM Gdp
        UNION
        SELECT MAX(year) as max, MIN(year) as min
        FROM Industry)
    """)
    results = cursor.fetchall()

    cursor.close()
    print(results)

    return utils.generate_response_for_year_range(results[0][0], results[0][1])



