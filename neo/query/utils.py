from flask import jsonify


def generate_response_for_year_range(min_year, max_year):
    response_data = {
        'min': min_year,
        'max': max_year
    }
    return jsonify(response_data)


def normalize_gdp(gdp):
    scales = ['', 'Million', 'Billion', 'Trillion']
    scale_index = 0

    while gdp >= 1000:
        gdp /= 1000
        scale_index += 1

    return round(gdp, 2), scales[scale_index]