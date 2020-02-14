import app
from app.configuration import Configuration

from multiprocessing import Pipe
from time import perf_counter as performance

def main() -> None:
    start_time: float = performance()
    conn_parent,conn_unit = Pipe(duplex=False)
    
    args:dict = app.arguments()
    config:Configuration = Configuration()
    configfile = args.config if "config" in args else None
    config.load(configfile)

    units:list = app.units(args['challenge'],pipe=conn_unit)
    processes:list = app.processes(units)
    app.execution(processes)
    app.search(processes,pipe=conn_parent,start=start_time,timeout=5)
    app.terminate(processes)

    print(f"[?] Execution time: {round(performance() - start_time, 2)} seconds")

def entrypoint() -> None:
    try:
        main()
    except KeyboardInterrupt:
        print("[!] The world is a dangerous place, Elliot...")

if __name__ == "__main__":
    entrypoint()