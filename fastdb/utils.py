def update_service_environment(compose_config, service_name, **kwargs):
    environment = compose_config["services"][service_name]["environment"].copy()
    for key, value in kwargs.items():
        environment[key] = value
        #print("{0} = {1}".format(key, value))
    compose_config["services"][service_name]["environment"] = environment
    return compose_config

def update_service_ports(compose_config, service_name, host, port):
    #ports = compose_config["services"][service_name]["ports"]
    pass

def port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0