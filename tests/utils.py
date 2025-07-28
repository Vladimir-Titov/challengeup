import psycopg2


def check_pg_connect(url) -> bool:
    try:
        psycopg2.connect(url)
        return True
    except psycopg2.OperationalError:
        return False
