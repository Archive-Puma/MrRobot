from app.works.base     import Base
from app.core.exception import Elliot

import imp
from pathlib import Path
from pkgutil import iter_modules

class Workflow:
    def __init__(self,workflow):
        self.count = 0
        self.current = None
        self.variables = dict()
        self.workflow = workflow
        self.worksdir = {
            "user": Path.home() / ".mrrobot",
            "local": Path(__file__).parent.parent / "works"
        }
    
    def run(self):
        for data in self.workflow:
            # Update the actual work
            self.count += 1
            self.current = data
            # Get the workname
            run = self.get_attribute("run", required=True)
            if ">" in run:
                run, output = run.split(">",1)
            if not "/" in run:
                raise Elliot("Bad work name. Works are specified in the following format: category/work")
            category, name = run.split("/",1)
            # Import the work
            module = self.import_work(category,name)
            work = self.init_work(module,data,self.variables)
            # Run the work
            result = work.run()
            # Save the output
            if output:
                self.save_output(output,result)
                print(self.variables)
            # Print the result
            else:
                print(result)


    def get_attribute(self, name, required=False):
        if name in self.current:
            return self.current[name]
        elif required:
            raise Elliot(f"Attribute required in the work #{self.count}: {name}")
        else:
            return None

    def save_output(self,name,value):
        # Strip the right side
        name = name.rstrip()
        # Check if is a concatenation
        if name.startswith(">"):
            # Removes the concat symbol
            name = name[1:].lstrip()
            # Check if the variable is already set
            if not name in self.variables:
                raise Elliot(f"No variable called {name}")
            # Concat the value
            old_value = self.variables[name]
            try:
                self.variables[name] = self.variables[name] + value
            except TypeError:
                raise Elliot(f"Variable {name} cannot be concated with the new value")
        else:
            # Store the value
            self.variables[name.lstrip()] = value

    def import_work(self,category,name):
        # Strip the results
        name = name.strip()
        category = category.strip()
        # Get the path
        path = self.worksdir["local"] / category / name
        module = f"{str(path)}.py"
        # Try to import the module
        try:
            imported = imp.load_source(name, module)
        except PermissionError:
            raise Elliot(f"You have no permissions to read {module}")
        # Return the module
        return imported
    
    def init_work(self,module,data,variables):
        expected_base = Base
        expected_class = "Work"
        # Check the class
        if not hasattr(module,expected_class):
            raise Elliot(f"[DEV] Cannot run the work. Expected class: '{expected_class}'")
        workclass = getattr(module,expected_class)
        # Check the base
        if not Base in workclass.__bases__:
            raise Elliot(f"[DEV] Cannot run the work. Expected base: {expected_base}")
        return workclass(data,variables)