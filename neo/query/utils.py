from flask import jsonify


def generate_response_for_year_range(min_year, max_year):
    response_data = {
        'min': min_year,
        'max': max_year
    }
    return jsonify(response_data)
