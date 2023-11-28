from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
from neo.query.all_queries import Gini_Coefficient_Query
import neo.query.utils as utils

bp = Blueprint('query5', __name__, url_prefix='/query5')


@bp.route('', methods=['GET'])
def fetch_gini_coefficient():
    states = request.args.get('state')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    state_list = [state.strip() for state in states.split(',')] if states else []
    bind_states = ",".join(":" + str(i + 1) for i in range(len(state_list)))
    q = Gini_Coefficient_Query.format(bind_states=bind_states, start_year=start_year, end_year=end_year)

    print(q)
    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute(q, state_list)
    results = cursor.fetchall()
    cursor.close

    print(results)

    response_data = {}
    for result in results:
        year = result[1]
        state = result[0]
        gini_coeff = result[2]

        if year not in response_data:
            response_data[year] = {"year": year}

        response_data[year][state] = gini_coeff

    final_output = sorted(list(response_data.values()), key=lambda x: x['year'])
    return jsonify(final_output)


# TODO: Make a common function that accepts table names and returns min, max of all tables
@bp.route('/year_range', methods=['GET'])
def get_query5_range():
    conn = app.config['DB_CONN']
    cursor = conn.cursor()
    cursor.execute("""
    SELECT MAX(min), MIN(max) 
    FROM
        (SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".County
        UNION
        SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Demographic
        UNION
        SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Poverty)
    """)
    results = cursor.fetchall()

    cursor.close()
    print(results)

    return utils.generate_response_for_year_range(results[0][0], results[0][1])