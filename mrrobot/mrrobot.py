import app
from app import display
from app.exception import Elliot
from app.configuration import Configuration

from multiprocessing import Pipe
from time import perf_counter as performance

def main() -> None:
    start_time: float = performance()
    conn_parent,conn_unit = Pipe(duplex=False)
    args = app.arguments()
    config:Configuration = app.configuration(args)
    units:list = app.units(args.input,config=config,pipe=conn_unit)
    processes:list = app.processes(units)
    app.execution(processes)
    result:tuple = app.search(processes,pipe=conn_parent,start=start_time,timeout=config.TIMEOUT)
    app.terminate(processes)
    display.flag(result)

    print(f"[?] Execution time: {round(performance() - start_time, 2)} seconds")

def entrypoint() -> None:
    try:
        main()
    except Elliot as problem:
        print(f"[!] {problem}")
    except KeyboardInterrupt:
        print("[!] The world is a dangerous place, Elliot...")

if __name__ == "__main__":
    entrypoint()