from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
from neo.query.all_queries import Crime_Unemployment_Query
from neo.query.utils import generate_response_for_year_range

bp = Blueprint('query4', __name__, url_prefix='/query4')


@bp.route('', methods=['GET'])
def fetch_unemployment_crime_relation():
    state = request.args.get('state')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    q = Crime_Unemployment_Query.format(state=state, start_year=start_year, end_year=end_year)
    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute(q)
    results = cursor.fetchall()
    cursor.close
    print(results)

    response_data = []
    for result in results:
        state_name = result[0]
        year = int(result[1])
        murder_coefficient = float(result[2])
        robbery_coefficient = float(result[3])
        aggravated_assault_coefficient = float(result[4])
        burglary_coefficient = float(result[5])
        larceny_coefficient = float(result[6])
        motor_vehicle_theft_coefficient = float(result[7])
        arson_coefficient = float(result[8])

        record = {
            "state_name": state_name,
            "year": year,
            "murder_coefficient": murder_coefficient,
            "robbery_coefficient": robbery_coefficient,
            "aggravated_assault_coefficient": aggravated_assault_coefficient,
            "burglary_coefficient": burglary_coefficient,
            "larceny_coefficient": larceny_coefficient,
            "motor_vehicle_theft_coefficient": motor_vehicle_theft_coefficient,
            "arson_coefficient": arson_coefficient
        }

        response_data.append(record)

    final_output = sorted(response_data, key=lambda x: x['year'])
    return jsonify(final_output)


@bp.route('/year_range', methods=['GET'])
def get_query4_range():
    conn = app.config['DB_CONN']
    cursor = conn.cursor()
    cursor.execute("""
    SELECT MAX(min), MIN(max) 
    FROM
        (SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Crime
        UNION
        SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Demographic
        UNION
        SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Unemployment)
    """)
    results = cursor.fetchall()

    cursor.close()
    print(results)

    return generate_response_for_year_range(results[0][0], results[0][1])