import oyaml as yaml

class YAMLReader:
    """
        read .yml / .yaml files
    """
    def __init__(self, file_path):
        """
            init file reader

            params:
                - file_path: path to YAML file
        """
        self.file_path = file_path
    
    def to_dict(self):
        """
            return yaml file as dict
        """
        with open(self.file_path) as file:
            # FullLoader handles conversion
            file_dict = yaml.load(file, Loader=yaml.FullLoader)
        # return dict
        return file_dict