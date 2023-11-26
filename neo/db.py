import oracledb
import os


def initialize_db(app):
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    hostname = os.environ.get('DB_HOSTNAME')
    port = os.environ.get('DB_PORT')
    service_name = 'orcl'

    params = oracledb.ConnectParams(host=hostname, port=port, service_name=service_name)
    conn = oracledb.connect(user=username, password=password, params=params)

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT name FROM "HARSHITH.KUMAR".State
            FETCH FIRST 1 ROWS ONLY""")
        results = cursor.fetchall()
        print(results)

    app.config['DB_CONN'] = conn
