def update_service_environment(compose_config, service_name, **kwargs):
    environment = compose_config["services"][service_name]["environment"].copy()
    for key, value in kwargs.items():
        environment[key] = value
    compose_config["services"][service_name]["environment"] = environment
    return compose_config

def update_service_ports(compose_config, service_name, new_port=None):
    #print(compose_config["services"][service_name])
    port_data = compose_config["services"][service_name]["ports"].copy()[0]
    # split by :
    split_port_data = port_data.split(":")
    # split port data is of the format
    # host:host_port:docker_port
    # replace host port 
    if new_port is not None:
        split_port_data[1] = str(new_port)
    # join to convert to docker compose format
    joined_port_data = ":".join(split_port_data)
    # update compose config dict
    compose_config["services"][service_name]["ports"] = [joined_port_data]
    # return updated config
    return compose_config


    
def port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0