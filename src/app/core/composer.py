from app.core.exception import Elliot
from app.core.workflow  import Workflow

import yaml

class Composer:
    def __init__(self):
        self.code = dict()
        self.supported_versions = [1]

    def load(self,filename):
        try:
            # Open the file in read mode
            with open(filename, "r") as composer:
                # Parse the Yaml
                self.code = yaml.load(composer, Loader=yaml.FullLoader)
            # Check the version
            self.check_version()
        # File not found
        except FileNotFoundError:
            raise Elliot("Composer not found.")
        # YAML error
        except yaml.scanner.ScannerError as err:
            position = str(err).split("\", ")[-1]
            raise Elliot(f"YAML syntax error in composer ({position})")

    def get(self, attr):
        # Check if an attribute exists
        if not attr in self.code:
            raise Elliot(f"No {attr} specified in the composer")
        return self.code[attr]
    
    def check_version(self):
        # Get the version
        version = self.get("version")
        # Check if the version is numeric
        if type(version) is not int:
            raise Elliot("Composer version should be a number")
        # Check the correct version
        if not version in self.supported_versions:
            raise Elliot(f"Unsupported composer version (lastest: {self.supported_versions[-1]})")

    def workflow(self):
        # Get the workflow
        workflow = self.get("workflow")
        # Check if the workflow is a list
        if type(workflow) is not list:
            raise Elliot("Workflow attribute should be a list")
        # Return the workflow
        return Workflow(workflow)