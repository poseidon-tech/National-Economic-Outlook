from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
from neo.query.all_queries import Homelessness_Mortgage_Query
from neo.query.national_queries import National_Homelessness_Mortgage_Query
import neo.query.utils as utils

bp = Blueprint('query3', __name__, url_prefix='/query3')
@bp.route('', methods=['GET'])
def fetch_homelessness_mortgage_relation():
    state = request.args.get('state')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    q = Homelessness_Mortgage_Query.format(state=state, start_year=start_year, end_year=end_year)
    if state == 'all':
        q = National_Homelessness_Mortgage_Query.format(start_year=start_year, end_year=end_year)

    print(q)
    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute(q)
    results = cursor.fetchall()
    cursor.close

    print(results)

    response_data = {}
    for result in results:
        year = result[0]
        thirty_year_frm = result[1]
        total_homelessness_rate = result[2]
        total_caucasian_homelessness_rate = result[3]
        total_african_american_homelessness_rate = result[4]
        total_american_indian_homelessness_rate = result[5]
        total_asian_american_homelessness_rate = result[6]
        total_hawaiian_homelessness_rate = result[7]
        total_hispanic_homelessness_rate = result[8]

        if year not in response_data:
            response_data[year] = {"year": year}

        response_data[year]["thirty_year_frm"] = thirty_year_frm
        response_data[year]["total_homelessness_rate"] = total_homelessness_rate
        response_data[year]["total_caucasian_homelessness_rate"] = total_caucasian_homelessness_rate
        response_data[year]["total_african_american_homelessness_rate"] = total_african_american_homelessness_rate
        response_data[year]["total_american_indian_homelessness_rate"] = total_american_indian_homelessness_rate
        response_data[year]["total_asian_american_homelessness_rate"] = total_asian_american_homelessness_rate
        response_data[year]["total_hawaiian_homelessness_rate"] = total_hawaiian_homelessness_rate
        response_data[year]["total_hispanic_homelessness_rate"] = total_hispanic_homelessness_rate

    final_output = sorted(list(response_data.values()), key=lambda x: x['year'])
    return jsonify(final_output)


# TODO: Make a common function that accepts table names and returns min, max of all tables
@bp.route('/year_range', methods=['GET'])
def get_query3_range():
    conn = app.config['DB_CONN']
    cursor = conn.cursor()
    cursor.execute("""
    SELECT MAX(min), MIN(max) 
    FROM
        (SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Homelessness
        UNION
        SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Demographic
        UNION
        SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Mortgage)
    """)
    results = cursor.fetchall()

    cursor.close()
    print(results)

    return utils.generate_response_for_year_range(results[0][0], results[0][1])