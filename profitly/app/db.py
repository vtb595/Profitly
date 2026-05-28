import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="profitly",
        user="postgres",
        password="password"
    )
    return conn