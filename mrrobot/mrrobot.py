from app.utils import arguments
from app.utils import configuration
from app.unit.loader import load_units
from app.utils.configuration import DEFAULT_FILE, ALL_UNITS_DISABLED, UNITS_CATEGORIES

import re
import threading
from os import remove
from os.path import exists, isfile
from concurrent.futures import as_completed, ThreadPoolExecutor, TimeoutError
from pebble import ProcessPool

# challenge = b"Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook. Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook. Ook! Ook. Ook! Ook? Ook! Ook! Ook? Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook."

def is_solved(flagformat,result):
    pattern = re.compile(flagformat)
    flag = pattern.match(result)
    return flag[0] if flag else None

def result2str(raw,coding):
    results = list()
    # Bytes to string
    if type(raw) is bytes:
        try: results.append(raw.decode(coding))
        except UnicodeDecodeError: pass
    # Recursive conversion to string
    elif type(raw) is list:
        for element in raw: results += result2str(element,coding)
    # Convert to string the rest of the types
    else: results.append(str(raw)) 
    # Return the results 
    return results

def flow(units,config):
    # Init the needed variables
    method, flag, current = None, None, 0
    with ProcessPool(max_workers=config["Threads"]) as pool:
        # Start all the threads
        threads = [ (pool.schedule(unit.run, timeout=config["Timeout"]), unit.id()) for (_,unit) in units ]
        # Get the results
        while not flag and current < len(threads):
            result = list()
            thread, method = threads[current]
            try:
                results = thread.result()
                results = result2str(results,config["Coding"])
                if len(results) > 0:
                    for result in results:
                        flag = is_solved(config["Flag"],result)
                        if flag: break
            except TimeoutError:
                print(f"-- Timeout {method}")
            current += 1
    # Return the flag or the finished state
    return (method,flag)

def get_configuration():
    inpt = None
    # Get the arguments
    args = arguments.parse()
    # File (TODO, maybe magic numbers)
    if isfile(args.input):
        with open(args.input, "rb") as challenge:
            inpt = challenge.read()
    # Removes the old configuration file
    if args.clean and exists(DEFAULT_FILE): remove(DEFAULT_FILE)
    # Create the configuration file if not specified
    if not args.config or not args.config is DEFAULT_FILE: args.config = configuration.default()
    # --- Parse and override the configuration values with the arguments
    config = configuration.parse(args.config)
    # Flag
    config["Flag"] = args.flag if args.flag else str(config["Flag"])
    # Timeout
    config["Timeout"] = args.timeout if args.timeout else float(config["Timeout"])
    # Threads
    config["Threads"] = args.threads and args.threads > 0 if args.threads else int(config["Threads"])
    # Coding
    config["Coding"] = args.coding.lower() if args.coding else str(config["Coding"]).lower()
    # Units
    if args.esoteric: # or args.crypto or ...
        config["Units"] = ALL_UNITS_DISABLED
        if args.esoteric: config["Units"][UNITS_CATEGORIES.index("esoteric")] = True
    if args.all or not any(config["Units"]):
        config["Units"] = [ True ] *  len(units)
    if not inpt: inpt = args.input.encode(config["Coding"]) 
    # Return the configuration
    return inpt, config


def entrypoint():
    # Get the configuration
    challenge, config = get_configuration()
    # Load all the units
    units = load_units()
    # Priotity units (0 - 100)
    priority_pool = [None] * 100
    # Iterate over all categories
    for idx, category in enumerate(UNITS_CATEGORIES):
        # Check if the unit is enabled
        if config["Units"][idx]:
            # Iterate over units
            for identifier in units[category]:
                # Get the unit and its priority
                unit = units[category][identifier].Unit(challenge)
                priority = unit.priority()
                # Init the priority
                if not priority_pool[priority]: priority_pool[priority] = list()
                # Append the unit
                priority_pool[priority].append((identifier, unit))
    # Join the priority pool to a list
    enabled_units = list()
    for priority in priority_pool:
        if priority: enabled_units += priority
    # Run the program
    (method, flag) = flow(enabled_units,config)
    # Print the result
    if flag:    print(f"Flag\t{flag}\nMethod\t{method}")
    else:       print("Cannot find the flag :(")

if __name__ == '__main__':
    entrypoint()

