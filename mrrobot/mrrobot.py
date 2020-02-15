import app
from app.exception import Elliot
from app.configuration import Configuration

from time import perf_counter
from multiprocessing import Pipe

def main() -> None:
    start_time:float = perf_counter()
    conn_parent,conn_unit = Pipe(duplex=False)
    args = app.arguments()
    config:Configuration = app.configuration(args)
    units:list = app.units(args.input,config=config,pipe=conn_unit)
    processes:list = app.processes(units)
    app.execution(processes)
    result:tuple = app.search(processes,pipe=conn_parent,start=start_time,timeout=config.TIMEOUT)
    app.terminate(processes)
    app.display.flag(result)
    app.display.performance(start_time)

def entrypoint() -> None:
    try:
        main()
    except Elliot as problem:
        print(f"[!] {problem}")
    except KeyboardInterrupt:
        print("[!] The world is a dangerous place, Elliot...")

if __name__ == "__main__":
    entrypoint()