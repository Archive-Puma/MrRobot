from app.core.exception import Elliot

class Base:
    def __init__(self, data, variables):
        self.data = data
        self.variables = variables
        self.name = "base" if not hasattr(self,"name") else self.name
        self.category = "_" if not hasattr(self,"category") else self.category
    
    def run(self):
        raise Elliot("[DEV] -- Unimplemented --")
    
    def get(self,name,required=False):
        if name in self.data:
            data = self.data[name]
            if self._is_variable(data):
                data = self._get_variable(data)
            return data
        elif required:
            raise Elliot(f"'{name}' should be specified for work {self.category}/{self.name}")
        else:
            return None
    
    def get_one(self,first,second):
        # Try to get both parameters
        frst = self.get(first)
        scnd = self.get(second)
        # Check if no one was specified
        if not frst and not scnd:
            raise Elliot(f"'{first}' or '{second}' should be specified for work {self.category}/{self.name}")
        # Check if both are specified
        elif frst and scnd:
            raise Elliot(f"'{first}' and '{second}' cannot be specified at the same time for work {self.category}/{self.name}")
        # Return the value
        return (first, frst) if frst else (second, scnd)
    
    def _is_variable(self,name):
        return name.startswith("${{") and name.endswith("}}")
    
    def _get_variable(self,name):
        variable = name[3:-2].strip()
        if not variable in self.variables:
            raise Elliot(f"Variable '{variable}' does not exist")
        return self.variables[variable]
