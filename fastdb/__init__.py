# sys
import subprocess, sys, time
from pathlib import Path
# import I/O classes
from fastdb.reader import YAMLReader
from fastdb.writer import YAMLWriter
# import networking classes
from fastdb.utils import (
    update_service_environment,
    update_service_ports,
    port_in_use
)

class ShellExecutor:
    """
        class to execute shell commands
    """
    def exec(self, command):
        """
            method to execute shell commands

            params:
                - command: string shell command
        """
        # execute command 
        process = subprocess.Popen([command], 
                        stdout=subprocess.PIPE,
                        universal_newlines=True,
                        shell=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
            rc = process.poll()

class DockerExecutor:
    """
        class to execute docker related commands
    """
    def start(self, tail=False):
        if tail:
            command = "docker-compose -f %s up --build" % str(self.config_path)
        else:
            command = "docker-compose -f %s up -d --build" % str(self.config_path)
        # display connection info
        self.info()
        # execute start command
        self.exec(command)
        # sleep
        time.sleep(10)

    def stop(self, keep_volumes=False):
        if not keep_volumes:
            # delete networks, volumes etc in addition to containers
            command = "docker-compose -f %s down -v --remove-orphans" % str(self.config_path)
        else:
            # delete containers but keep networks, volumes etc
            command = "docker-compose -f %s down" % str(self.config_path)
        # execute stop command
        self.exec(command)

class MockPostgres(ShellExecutor, DockerExecutor):
    """
        python class to provide an interace to
        MySQL docker containers
    """
    def __init__(self, ui=True, config_path=None):
        # initialize shell executor
        ShellExecutor.__init__(self)
        # check if custom docker-compose config file path
        # has been specified
        if config_path is None:
            if ui:
                # use config with pgadmin
                self.config_path = Path(__file__).parent.absolute().joinpath("docker-compose.postgres.yaml")
            else:
                # use config without pgadmin
                self.config_path = Path(__file__).parent.absolute().joinpath("docker-compose.postgres.nopgadmin.yaml")
        else:
            # use user defined config
            self.config_path = config_path

    def config(
            self,
            user=None,
            password=None,
            database=None,
            port=5432,
            root_password=None
        ):
        """
            configure docker compose file for MySQL

            params:
                - user: database user
                - password: password for above database user
                - databse: name of default database for above user
                - port: port to run it on
                - root_password: passfor for root user
        """
        # get docker compose as dict
        compose_dict = YAMLReader(file_path=self.config_path).to_dict()
        # dict to store update data
        update_data = {}
        # if user specified
        if user is not None:
            # add to update data
            update_data["POSTGRES_USER"] = user
        # if password specified
        if password is not None:
            # add to update data
            update_data["POSTGRES_PASSWORD"] = password
        # if database name specified
        if database is not None:
            # add to update data
            update_data["POSTGRES_DB"] = database
        # if any update data found
        if update_data:
            # update dict with user specified data
            # otherwise use default values
            compose_dict = update_service_environment(compose_dict, "postgresdb", **update_data)
            # update dict with user specified port
            compose_dict = update_service_ports(compose_dict, "postgresdb", port)
        # if port specified use that otherwise generate unused new one
        # update default names to fastdb fastdbpass testdb
        # file name for update docker compose file
        file_name = "docker-compose.postgres.updated.yaml"
        # dir to store docker compose file in
        config_dir = Path(__file__).parent.absolute()
        # write to file
        yaml_writer = YAMLWriter(d=compose_dict).to_yaml(file_name=file_name, dir_path=config_dir)
        # get updated config file path
        updated_config_path = config_dir.joinpath(file_name)
        # update the current instances config path
        self.config_path = updated_config_path
        # display updated info
        self.info()

    def info(self):
        """
            get information about database from docker
            compose file
        """
        # get docker compose file as dict
        compose_dict = YAMLReader(file_path=self.config_path).to_dict()
        # get environment data from docker compose dict
        env_data = compose_dict["services"]["postgresdb"]["environment"]
        # get connection data from docker compose dict
        # this is of the form host:port:docker_port
        conn_data = compose_dict["services"]["postgresdb"]["ports"][0].split(":")
        # keys
        conn_keys = ['host', 'port', 'docker_port']
        # build conn info with names
        conn_info = {key: val for key, val in zip(conn_keys, conn_data)}
        # convert to DBAPI friendly dict format
        dsn = {
                "host": conn_info["host"],
                "port": int(conn_info["port"]),
                "user": env_data["POSTGRES_USER"],
                "password": env_data["POSTGRES_PASSWORD"],
                "database": env_data["POSTGRES_DB"]
        }
        # display connection info
        print(dsn)
        # return connection info as dict
        return dsn

class MockMySQL(ShellExecutor, DockerExecutor):
    """
        python class to provide an interace to
        MySQL docker containers
    """
    def __init__(self, ui=True, config_path=None):
        # initialize shell executor (just runs shell commands)
        ShellExecutor.__init__(self)
        # check if custom docker-compose config file path
        # has been specified
        if config_path is None:
            if ui:
                # use config with adminer
                self.config_path = Path(__file__).parent.absolute().joinpath("docker-compose.mysql.yaml")
            else:
                # use config without adminer
                self.config_path = Path(__file__).parent.absolute().joinpath("docker-compose.mysql.noadminer.yaml")
        else:
            # use user defined config
            self.config_path = config_path
    
    def config(
            self,
            user=None,
            password=None,
            database=None,
            port=33061,
            root_password=None
        ):
        """
            configure docker compose file for MySQL

            params:
                - user: database user
                - password: password for above database user
                - databse: name of default database for above user
                - port: port to run it on
                - root_password: passfor for root user
        """
        # get docker compose as dict
        compose_dict = YAMLReader(file_path=self.config_path).to_dict()
        # dict to store update data
        update_data = {}
        # if user specified
        if user is not None:
            # add to update data
            update_data["MYSQL_USER"] = user
        # if password specified
        if password is not None:
            # add to update data
            update_data["MYSQL_PASSWORD"] = password
        # if database name specified
        if database is not None:
            # add to update data
            update_data["MYSQL_DATABASE"] = database
        # if root password specified
        if root_password is not None:
            # add to update data
            update_data["MYSQL_ROOT_PASSWORD"] = root_password  
        # if any update data found
        if update_data:
            # update dict with user specified data
            # otherwise use default values
            compose_dict = update_service_environment(compose_dict, "mysqldb", **update_data)
            # update dict with user specified port
            compose_dict = update_service_ports(compose_dict, "mysqldb", port)
        # file name for update docker compose file
        file_name = "docker-compose.mysql.updated.yaml"
        # dir to store docker compose file in
        config_dir = Path(__file__).parent.absolute()
        # write to file
        yaml_writer = YAMLWriter(d=compose_dict).to_yaml(file_name=file_name, dir_path=config_dir)
        # get updated config file path
        updated_config_path = config_dir.joinpath(file_name)
        # update the current instances config path
        self.config_path = updated_config_path
        # display updated info
        self.info()

    def info(self):
        """
            get information about database from docker
            compose file
        """
        # get docker compose file as dict
        compose_dict = YAMLReader(file_path=self.config_path).to_dict()
        # get environment data from docker compose dict
        env_data = compose_dict["services"]["mysqldb"]["environment"]
        # get connection data from docker compose dict
        # this is of the form host:port:docker_port
        conn_data = compose_dict["services"]["mysqldb"]["ports"][0].split(":")
        # keys
        conn_keys = ['host', 'port', 'docker_port']
        # build conn info with names
        conn_info = {key:val for key, val in zip(conn_keys, conn_data)}
        # convert to DBAPI friendly dict format
        dsn = {
                "host": conn_info["host"],
                "port": int(conn_info["port"]),
                "user": env_data["MYSQL_USER"],
                "password": env_data["MYSQL_PASSWORD"],
                "database": env_data["MYSQL_DATABASE"]
        }
        # display connection info
        print(dsn)
        # return connection info as dict
        return dsn
