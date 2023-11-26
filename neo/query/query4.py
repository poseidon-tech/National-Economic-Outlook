from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
from neo.query.all_queries import Crime_Unemployment_Query
import neo.query.utils as utils

bp = Blueprint('query4', __name__, url_prefix='/query4')

@bp.route('', methods=['GET'])
def fetch_unemployment_crime_relation():
    states = request.args.get('states')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')
    states_list = [state.strip() for state in states.split(',')] if states else []
    bind_states = ",".join(":" + str(i + 1) for i in range(len(states_list)))
    q = Crime_Unemployment_Query.format(bind_states=bind_states, start_year=start_year,
                                  end_year=end_year)
    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute(q, states_list)
    results = cursor.fetchall()
    cursor.close
    print(results)

    response_data = []
    for result in results:
        state_name = result[0]
        year = int(result[1])
        crime_rate_per_year = float(result[10])
        unemployment_rate_per_year = float(result[13])

        record = {
            "state_name": state_name,
            "crime_rate_per_year": crime_rate_per_year,
            "unemployment_rate_per_year": unemployment_rate_per_year,
            "year": year
        }

        response_data.append(record)

    final_output = sorted(response_data, key=lambda x: x['year'])
    return jsonify(final_output)