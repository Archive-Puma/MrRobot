#!/usr/bin/env python3

from mrrobot import app
from mrrobot.app import display
from mrrobot.app.exception import Elliot
from mrrobot.app.configuration import Configuration

from time import perf_counter
from multiprocessing import Pipe

def main(processes:list) -> None:
    # Check dependencies
    app.check_requirements()
    # Start the performance counter
    start_time:float = perf_counter()
    # Create the connection between processes
    conn_parent,conn_unit = Pipe(duplex=False)
    # Parse the arguments and configuration
    args,contents = app.arguments()
    config:Configuration = app.configuration(args)
    challenge:tuple = (args.input,contents) if contents else (args.input,args.input)
    if not args.no_banner: app.display.banner()
    units:list = app.units(challenge,config=config,pipe=conn_unit)
    processes = app.processes(units)
    app.execution(processes)
    continous:bool = True
    while continous:
        result:tuple = app.search(processes,pipe=conn_parent,start=start_time,timeout=config.TIMEOUT)
        if args.find_all and result: app.display.flag(result)
        else: continous = False
    if not args.find_all: app.display.flag(result)
    app.display.performance(start_time)

def entrypoint() -> None:
    processes:list = list()
    try:
        main(processes)
    except Elliot as problem:
        app.display.error(problem)
    except KeyboardInterrupt:
        app.display.error("The world is a dangerous place, Elliot...")
    finally:
        app.display.info("Cleanning processes...",decorator="*")
        app.terminate(processes)

if __name__ == "__main__":
    entrypoint()