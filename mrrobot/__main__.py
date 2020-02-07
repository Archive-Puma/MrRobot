from app.utils import arguments
from app.utils import configuration
from app.utils.configuration import DEFAULT_THREADS
from app.unit.esoteric.ook import Unit as Ook
from app.unit.esoteric.brainfuck import Unit as Brainfuck


import re
import threading
from concurrent.futures import ThreadPoolExecutor

#challenge = b"++[---------->+<]>.-[-->+++<]>.-[->+++<]>-.--[--->+<]>-.-------------.+++++++++++++.+++++.[->+++++<]>-.>-[--->+<]>-.[----->+<]>++.>--[-->+++++<]>.[->+++++<]>-.>-[--->+<]>.++++++++++++++.++++++++.------------.++++++++++++++.--[--->+<]>.[->+++++<]>++.+++.[--->+<]>----.[-->+<]>-----.---.-[----->+<]>--.[--->+<]>+++."
challenge = b"""
Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook.

Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook. Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook. Ook! Ook. Ook! Ook? Ook! Ook! Ook? Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. 
"""


def is_solved(flagformat,result):
    pattern = re.compile(flagformat)
    flag = pattern.match(result)
    return flag[0] if flag else None

def flow(config):
    units   = list()
    threads = list()

    units.append(Brainfuck(challenge))
    units.append(Ook(challenge))

    with ThreadPoolExecutor(max_workers=config["Threads"]) as executor:
        threads = [ executor.submit(unit.run) for unit in units ]
        for thread in threads:
            result = thread.result()
            if result:
                flag = is_solved(config["Flag"], result)
                if flag: return flag
    return "-- Nothing --"

def entrypoint():
    # Get the arguments
    args = arguments.parse()
    # Create the configuration file if not specified
    if not args.file: args.file = configuration.default()
    # Parse and override the configuration values with the arguments
    config = configuration.parse(args.file)
    config["Threads"] = args.threads if args.threads else int(config["Threads"]) if config["Threads"] else DEFAULT_THREADS
    # Run the program
    print(flow(config))

if __name__ == '__main__':
    entrypoint()