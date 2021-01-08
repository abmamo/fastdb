# fastdb
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
  mock_mysql.config(user="fs2db", password="fs2dbpassword")
  mock_mysql.start()
  # postgres
  from fastdb import MockPostgres
  mock_postgres = MockPostgres()
  mock_postgres.config(user="fs2db", password="fs2dbpassword")
  mock_postgres.start()

```
to stop mock databases run
```
  # mysql
  mock_mysql.stop()
  # postgres
  mock_postgres.stop()
```
