import oyaml as yaml
from pathlib import Path


class YAMLWriter:
    """
        convert python dict to .yaml/.yml
    """
    def __init__(self, d):
        """
            initilize writer

            params:
                - d: dictionary we want to convert
                     to YAML
        """
        self.d = d
    
    def to_yaml(self, file_name, dir_path=None):
        """
            convert python dictionary to YAML

            params:
                - file_name: name of YAML file
                - dir_path: directory to save the file in
        """
        # if dir path is not specified
        if dir_path is None:
            # use the current file's dir as the default
            dir_path = Path(__file__).parent.absolute()
        # create full file path from file name & dir path
        file_path = dir_path.joinpath(file_name)
        # open file using file path
        with open(file_path, 'w') as outfile:
            # write dict to yaml
            yaml.dump(self.d, outfile, default_flow_style=False)
