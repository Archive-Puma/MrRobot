from app.utils import arguments
from app.utils import configuration
from app.unit.loader import load_units
from app.utils.configuration import DEFAULT_FILE, ALL_UNITS_DISABLED, UNITS_CATEGORIES

import re
import threading
from os import remove
from os.path import exists, isfile
from concurrent.futures import as_completed, ThreadPoolExecutor
from pebble import ProcessPool

# challenge = b"Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook. Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook. Ook! Ook. Ook! Ook? Ook! Ook! Ook? Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook."

def is_solved(flagformat,result):
    pattern = re.compile(flagformat)
    flag = pattern.match(result)
    return flag[0] if flag else None

def flow(units,config):
    # Init the needed variables
    method, flag = None, None
    with ProcessPool(max_workers=config["Threads"]) as pool:
        # Start all the threads
        threads = { pool.schedule(units[name].run, timeout=config["Timeout"]): units[name].id() for name in units }
        # Get the results
        for thread in threads:
            method = threads[thread]
            try:
                result = thread.result()
                if result:
                    flag = is_solved(config["Flag"],result)
                    if flag: break
            except:
                print(f"-- Timeout {method}")
    # Return the flag or the finished state 
    return (method,flag)

def get_configuration():
    # Get the arguments
    args = arguments.parse()
    # File or text (TODO, maybe magic numbers)
    if isfile(args.input):
        with open(args.input, "rb") as challenge:
            args.input = challenge.read()
    else: args.input = args.input.encode("utf-8") 
    # Removes the old configuration file
    if args.clean and exists(DEFAULT_FILE): remove(DEFAULT_FILE)
    # Create the configuration file if not specified
    if not args.config or not args.config is DEFAULT_FILE: args.config = configuration.default()
    # --- Parse and override the configuration values with the arguments
    config = configuration.parse(args.config)
    # Flag
    config["Flag"] = args.flag if args.flag else config["Flag"]
    # Timeout
    config["Timeout"] = args.timeout if args.timeout else float(config["Timeout"])
    # Threads
    config["Threads"] = args.threads and args.threads > 0 if args.threads else int(config["Threads"])
    # Units
    if args.esoteric: # or args.crypto or ...
        config["Units"] = ALL_UNITS_DISABLED
        if args.esoteric: config["Units"][UNITS_CATEGORIES.index("esoteric")] = True
    if args.all or not any(config["Units"]):
        config["Units"] = [ True for _ in units ]
    # Return the configuration
    return args.input, config


def entrypoint():
    # Get the configuration
    challenge, config = get_configuration()
    # Load all the units
    units = load_units()
    # Filter the enabled units
    enabled_units = dict()
    for idx, category in enumerate(UNITS_CATEGORIES):
        if config["Units"][idx]:
            for identifier in units[category]:
                enabled_units[identifier] = units[category][identifier].Unit(challenge)
    # Run the program
    (method, flag) = flow(enabled_units,config)
    if flag:    print(f"Flag\t{flag}\nMethod\t{method}")
    else:       print("Cannot find the flag :(")

if __name__ == '__main__':
    entrypoint()

