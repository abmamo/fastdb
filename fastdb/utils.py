# networking
import socket
# random
import random

def update_service_environment(compose_dict, service_name, **kwargs):
    """
        update docker compose file environment vals

        params:
            - compose_dict: docker compose yml file as python dict
            - service_name: docker compose service whose env vars are
                            being updated
    """
    # get environment from compose dict
    environment = compose_dict["services"][service_name]["environment"].copy()
    # for each user updates
    for key, value in kwargs.items():
        # update environment value
        environment[key] = value
    # update compose dict with new environment values
    compose_dict["services"][service_name]["environment"] = environment
    # return updated compose dict
    return compose_dict


def update_service_ports(compose_dict, service_name, new_port=None, host="localhost"):
    """
        update docker compose service connection mapping

        params:
            - compose_dict: docker compose yml file as python dict
            - service_name: docker compose service whose env vars are
                            being updated
    """
    # get conn data from docker compose file
    conn_data = compose_dict["services"][service_name]["ports"].copy()[0]
    # split by : (its of the format host:host_port:docker_port)
    conn_data_split = conn_data.split(":")
    # check port data passed
    if new_port is not None:
        # if port is in use
        if port_in_use(new_port):
            # generate new port
            new_port = generate_port(host=host)
    # if port data not passed
    else:
        # if default port is in use
        if port_in_use(conn_data_split[1]):
            # generate new port
            new_port = generate_port(host=host)
    # replace host port with new port
    conn_data_split[1] = str(new_port)
    # combine split conn data into docker compose format
    updated_conn_data = ":".join(conn_data_split)
    # update docker compose config with new conn data
    compose_dict["services"][service_name]["ports"] = [updated_conn_data]
    # return updated config
    return compose_dict


def port_in_use(port, host="localhost"):
    """
        check if port is in use

        params:
            - port: port number
    """
    # if port is a string
    if isinstance(port, str):
        # convert to int
        port = int(port)
    # open connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # return connection status
        return s.connect_ex((host, port)) == 0


def generate_port(host="localhost"):
    """
        return unused port on host machine

        params:
            - host: host to generate port for
    """
    # scan for port until found
    while True:
        # generate random number
        random_port = random.randint(1024, 65535)
        # check if it is not in use
        if not port_in_use(port=random_port, host=host):
            # return port
            return random_port