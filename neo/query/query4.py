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
        murder_rate_per_year = float(result[2])
        rape_rate_per_year = float(result[3])
        robbery_rate_per_year = float(result[4])
        aggravated_assault_rate_per_year = float(result[5])
        burglary_rate_per_year = float(result[6])
        larceny_rate_per_year = float(result[7])
        motor_vechile_theft_rate_per_year = float(result[8])
        arson_rate_per_year = float(result[9])
        crime_rate_per_year = float(result[10])
        total_violent_crime_year = float(result[11])
        total_non_violent_crime_year = float(result[12])
        unemployment_rate_per_year = float(result[13])
        murder_rate_frm_2005_2019 = float(result[14])
        rape_rate_frm_2005_2019 = float(result[15])
        robbery_rate_frm_2005_2019 = float(result[16])
        aggravated_assault_rate_frm_2005_2019 = float(result[17])
        burglary_rate_frm_2005_2019 = float(result[18])
        larceny_rate_frm_2005_2019 = float(result[19])
        motor_vechile_theft_rate_frm_2005_2019 = float(result[20])
        arson_rate_frm_2005_2019 = float(result[21])
        crime_rate_frm_2005_2019 = float(result[22])
        unemployment_rate_frm_2005_2019 = float(result[23])


        record = {
            "state_name": state_name,
            "year": year,
            "murder_rate_per_year": murder_rate_per_year,
            "rape_rate_per_year": rape_rate_per_year,
            "robbery_rate_per_year": robbery_rate_per_year,
            "aggravated_assault_rate_per_year": aggravated_assault_rate_per_year,
            "burglary_rate_per_year": burglary_rate_per_year,
            "larceny_rate_per_year": larceny_rate_per_year,
            "motor_vechile_theft_rate_per_year": motor_vechile_theft_rate_per_year,
            "arson_rate_per_year": arson_rate_per_year,
            "crime_rate_per_year": crime_rate_per_year,
            "total_violent_crime_year": total_violent_crime_year,
            "total_non_violent_crime_year": total_non_violent_crime_year,
            "unemployment_rate_per_year": unemployment_rate_per_year,
            "murder_rate_frm_2005_2019": murder_rate_frm_2005_2019,
            "rape_rate_frm_2005_2019": rape_rate_frm_2005_2019,
            "robbery_rate_frm_2005_2019": robbery_rate_frm_2005_2019,
            "aggravated_assault_rate_frm_2005_2019": aggravated_assault_rate_frm_2005_2019,
            "burglary_rate_frm_2005_2019": burglary_rate_frm_2005_2019,
            "larceny_rate_frm_2005_2019": larceny_rate_frm_2005_2019,
            "motor_vechile_theft_rate_frm_2005_2019": motor_vechile_theft_rate_frm_2005_2019,
            "arson_rate_frm_2005_2019": arson_rate_frm_2005_2019,
            "crime_rate_frm_2005_2019": crime_rate_frm_2005_2019,
            "unemployment_rate_frm_2005_2019": unemployment_rate_frm_2005_2019
        }

        response_data.append(record)

    final_output = sorted(response_data, key=lambda x: x['year'])
    return jsonify(final_output)