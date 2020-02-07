import pkgutil
from os import path
from pathlib import Path
from importlib import import_module

UNITS_CATEGORY_FOLDER = Path(__file__).parent

def __load_category(category):
    # Reset the units
    LOADED_UNITS = dict()
    # Get the units folder
    UNITS_FOLDER = path.join(UNITS_CATEGORY_FOLDER,category)
    # Find all the units
    for (_, name, _) in pkgutil.iter_modules([UNITS_FOLDER]):
        # Exclude base file
        if name != "base":
            # Import the module
            imported_unit = import_module(f"app.unit.{category}.{name}")
            # Check if it is a real unit
            if hasattr(imported_unit, "Unit"):
                # Add it to the loaded units
                LOADED_UNITS[name] = imported_unit
    # Return the units
    return LOADED_UNITS

def load_units():
    UNITS = dict()
    # Find all categories
    for (_, category, _) in pkgutil.iter_modules([UNITS_CATEGORY_FOLDER]):
        # Exclude loader and base files
        if category != "loader" and category != "base":
            # Load all the units in the category
            UNITS[category] = __load_category(category)
    # Return the units
    return UNITS


