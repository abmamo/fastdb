# fastdb ![test](https://github.com/abmamo/fastdb/workflows/test/badge.svg?branch=main)
set up & configure mock MySQL & Postgres databases using python + docker (requires docker)

## quickstarnt
install fastdb
```
  pip install 'fastdb @ https://github.com/abmamo/fastdb/archive/v0.0.1.tar.gz'
```
start mock databases in docker containers
```
  # mysql
  from fastdb import MockMySQL
  mock_mysql = MockMySQL()
  mock_mysql.start()
  # postgres
  from fastdb import MockPostgres
  mock_postgres = MockPostgres()
  mock_postgres.start()

```
to stop mock databases run
```
  # mysql
  mock_mysql.stop()
  # postgres
  mock_postgres.stop()
```
to set custom values for info such as db user, password etc you can use the config method
```
  # mysql
  from fastdb import MockMySQL
  mock_mysql = MockMySQL()
  mock_mysql.config(user="fastdb", password="fastdbpassword", port=5000)
  mock_mysql.start()
  
  # postgres
  from fastdb import MockPostgres
  mock_postgres = MockPostgres()
  mock_postgres.start()
  mock_postgres.config(user="fastdb", password="fastdbpassword", port=1000)
```
