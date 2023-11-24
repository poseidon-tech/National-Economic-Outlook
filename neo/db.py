import oracledb
import os


def initialize_db(app):
    username = 'HARSHITH.KUMAR'
    password = 'WLsLZEaAh0DDmrXNCiULlCGp'
    hostname = os.environ.get('DB_HOSTNAME')
    port = os.environ.get('DB_PORT')
    service_name = 'orcl'

    params = oracledb.ConnectParams(host=hostname, port=port, service_name=service_name)
    conn = oracledb.connect(user=username, password=password, params=params)

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM State""")
        results = cursor.fetchall()
        print(results)
        print("PRINTED ONCE")

    app.config['DB_CONN'] = conn
