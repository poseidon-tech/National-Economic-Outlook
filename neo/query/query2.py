from flask import current_app as app
from flask import jsonify, request
from flask import Blueprint
from neo.query.all_queries import Poverty_Demographics_Query
import neo.query.utils as utils

bp = Blueprint('query2', __name__, url_prefix='/query2')


@bp.route('', methods=['GET'])
def fetch_poverty_population_relation():

    state = request.args.get('state')
    
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    q = Poverty_Demographics_Query.format(state=state, start_year=start_year, end_year=end_year)

    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute(q)
    results = cursor.fetchall()
    cursor.close
    
    print(results)

    response_data = {}
    
    for result in results:
        year = result[0]
        total_african_american_population_percentage = result[4]
        total_american_indian_population_percentage = result[5]
        total_caucasian_population_percentage = result[6]
        total_asian_american_population_percentage = result[7]
        total_hawaiian_population_percentage = result[8]
        total_hispanic_population_percentage = result[9]

        total_poverty_percentage = result[12]
        total_poverty_under_18_percentage = result[14]
        total_poverty_over_18_percentage = result[16]

        if year not in response_data:
            response_data[year] = {"year": year,
                                   "total_african_american_population_percentage": total_african_american_population_percentage,
                                   "total_american_indian_population_percentage": total_american_indian_population_percentage,
                                   "total_asian_american_population_percentage": total_asian_american_population_percentage,
                                   "total_caucasian_population_percentage": total_caucasian_population_percentage,
                                   "total_hawaiian_population_percentage": total_hawaiian_population_percentage,
                                   "total_hispanic_population_percentage": total_hispanic_population_percentage,
                                   "total_poverty_percentage": total_poverty_percentage,
                                   "total_poverty_under_18_percentage": total_poverty_under_18_percentage,
                                   "total_poverty_over_18_percentage": total_poverty_over_18_percentage}

    final_output = sorted(list(response_data.values()), key=lambda x: x['year'])
    return jsonify(final_output)


@bp.route('/year_range', methods=['GET'])
def get_query2_range():
    conn = app.config['DB_CONN']
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT MAX(min), MIN(max) 
    FROM
        (SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Poverty
        UNION
        SELECT MAX(year) as max, MIN(year) as min
        FROM "HARSHITH.KUMAR".Demographic)
    """)

    results = cursor.fetchall()

    cursor.close()
    print(results)

    return utils.generate_response_for_year_range(results[0][0], results[0][1])











































