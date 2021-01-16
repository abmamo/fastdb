# DBAPI
import psycopg2
import pymysql

def test_mock_postgres(mock_psql_dsn):
    # connect using mock info
    conn = psycopg2.connect(**mock_psql_dsn)
    # assert db is connected
    assert not conn.closed

def test_mock_mysql(mock_mysql_dsn):
    # connect using mock info
    conn = pymysql.connect(**mock_mysql_dsn)
    # assert db is connected
    assert conn.cursor().connection