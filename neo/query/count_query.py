from flask import current_app as app
from flask import jsonify
from flask import Blueprint

bp = Blueprint('count', __name__, url_prefix='/count')


@bp.route('', methods=['GET'])
def fetch_total_count():
    response = {}

    conn = app.config['DB_CONN']
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM "HARSHITH.KUMAR".State""")
    state_count = cursor.fetchone()[0]
    cursor.execute("""
        SELECT COUNT(*) FROM "HARSHITH.KUMAR".County""")
    county_count = cursor.fetchone()[0]
    cursor.execute("""
            SELECT COUNT(*) FROM "HARSHITH.KUMAR".County_Fips""")
    county_fips_count = cursor.fetchone()[0]
    cursor.execute("""
            SELECT COUNT(*) FROM "HARSHITH.KUMAR".Unemployment""")
    unemployment_count = cursor.fetchone()[0]
    cursor.execute("""
            SELECT COUNT(*) FROM "HARSHITH.KUMAR".Poverty""")
    poverty_count = cursor.fetchone()[0]
    cursor.execute("""
            SELECT COUNT(*) FROM "HARSHITH.KUMAR".Crime""")
    crime_count = cursor.fetchone()[0]
    cursor.execute("""
            SELECT COUNT(*) FROM "HARSHITH.KUMAR".Homelessness""")
    homelessness_count = cursor.fetchone()[0]
    cursor.execute("""
            SELECT COUNT(*) FROM "HARSHITH.KUMAR".Mortgage""")
    mortgage_count = cursor.fetchone()[0]
    cursor.execute("""
                SELECT COUNT(*) FROM "HARSHITH.KUMAR".Industry""")
    industry_count = cursor.fetchone()[0]
    cursor.execute("""
                SELECT COUNT(*) FROM "HARSHITH.KUMAR".Gdp""")
    gdp_count = cursor.fetchone()[0]
    cursor.execute("""
                    SELECT COUNT(*) FROM "HARSHITH.KUMAR".Industry_Category""")
    industry_category_count = cursor.fetchone()[0]
    cursor.execute("""
                        SELECT COUNT(*) FROM "HARSHITH.KUMAR".Demographic""")
    demographic_count = cursor.fetchone()[0]
    cursor.close()

    response['State'] = state_count
    response['County'] = county_count
    response['County_Fips'] = county_fips_count
    response['Unemployment'] = unemployment_count
    response['Poverty'] = poverty_count
    response['Crime'] = crime_count
    response['Homelessness'] = homelessness_count
    response['Mortgage'] = mortgage_count
    response['Industry'] = industry_count
    response['Gdp'] = gdp_count
    response['Industry_Category'] = industry_category_count
    response['Demographic'] = demographic_count
    response['Total'] = (state_count + county_count + county_fips_count + unemployment_count + poverty_count +
                         crime_count + homelessness_count + mortgage_count + industry_count + gdp_count +
                         industry_category_count + demographic_count)

    return jsonify(response)
