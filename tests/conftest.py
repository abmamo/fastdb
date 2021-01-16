# testing
import pytest
# mock db
from fastdb import MockPostgres, MockMySQL
mock_mysql = MockMySQL()
mock_postgres = MockPostgres()
# start docker dbs
mock_mysql.start()
mock_postgres.start()


@pytest.fixture(scope="package", autouse=True)
def mock_psql_dsn():
    # yield store
    yield mock_postgres.info()
    # stop after tests finish (basically deleting docker containers)
    mock_postgres.stop()


@pytest.fixture(scope="package", autouse=True)
def mock_mysql_dsn():
    # yield store
    yield mock_mysql.info()
    # stop after tests finish (basically deleting docker containers)
    mock_mysql.stop()