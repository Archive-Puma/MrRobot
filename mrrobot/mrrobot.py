from time import perf_counter as performance

import app
from multiprocessing import Pipe

def main() -> None:
    start_time: float = performance()
    conn_parent,conn_unit = Pipe(duplex=False)
    
    configuration:dict = app.arguments()

    units:list = app.units(configuration['challenge'],pipe=conn_unit)
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