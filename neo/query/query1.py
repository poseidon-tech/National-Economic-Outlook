from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
from neo.query.all_queries import Industry_Gdp_Query
import neo.query.utils as utils

bp = Blueprint('query1', __name__, url_prefix='/query1')


@bp.route('', methods=['GET'])
def fetch_industry_gdp_relation():
    state = request.args.get('state')
    industries = request.args.get('naics')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    industries_list = [industry.strip() for industry in industries.split(',')] if industries else []
    bind_industries = ",".join(":" + str(i + 1) for i in range(len(industries_list)))
    q = Industry_Gdp_Query.format(state=state, bind_industries=bind_industries, start_year=start_year,
                                  end_year=end_year)

    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute(q, industries_list)
    results = cursor.fetchall()
    cursor.close
    # print(q)
    print(results)

    response_data = {}
    for result in results:
        year = result[0]
        industry = result[1]
        gdp = result[2]
        growth = result[3]

        if year not in response_data:
            response_data[year] = {"year": year, "gdp": gdp}

        response_data[year][industry] = growth

    final_output = sorted(list(response_data.values()), key=lambda x: x['year'])
    return jsonify(final_output)


# Common route to get states for all queries. Move to a common blueprint if time permits
@bp.route('/get_all_states', methods=['GET'])
def get_all_states():
    conn = app.config['DB_CONN']
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name, code
    FROM "HARSHITH.KUMAR".State
    """)

    results = cursor.fetchall()
    cursor.close()
    response_json = {}
    for row in results:
        response_json[row[0]] = row[1]


    return jsonify(response_json)


# TODO: Make a common function that accepts table names and returns min, max of all tables
@bp.route('/year_range', methods=['GET'])
def get_query1_range():
    conn = app.config['DB_CONN']
    cursor = conn.cursor()
    cursor.execute("""
    SELECT MAX(min), MIN(max) 
    FROM
        (SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Gdp
        UNION
        SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Industry)
    """)
    results = cursor.fetchall()

    cursor.close()
    print(results)

    return utils.generate_response_for_year_range(results[0][0], results[0][1])



