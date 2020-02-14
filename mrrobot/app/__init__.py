from os.path import isfile
from time import perf_counter as counter
from multiprocessing import active_children, Lock, Pipe, Process

from app.arguments import parse as argparser

from units.esoteric.ook import Unit as Ook
from units.esoteric.brainfuck import Unit as Brainfuck


istimeout = lambda start,timeout: bool(not start or not timeout or counter() - start >= timeout)

def arguments() -> dict:
    configuration:dict = dict()
    arguments:object = argparser()
    
    if isfile(arguments.input):
        with open(arguments.input,"rb") as f: configuration['challenge'] = f.read()
    else: configuration['challenge'] = arguments.input

    return configuration

def execution(processes:list) -> None:
    for process in processes: process.start()

def processes(units:list) -> list:
    return [ Process(target=unit.run,name=f"{unit.ID[0]}::{unit.ID[1]}") for unit in units ]

def search(processes:list,pipe:Pipe,start:float=None,timeout:float=None) -> None:
    flag:bool   = False
    while not flag and len(active_children()) > 0 and not istimeout(start,timeout):
        if pipe.poll():
            flag = True
            ((category,name),result,additional_data) = pipe.recv()
            print(f"[+] Flag found!")
            print(f" | Flag:\t{result[0]}")
            print(f" | Category:\t{category}")
            print(f" | Unit:\t{name}")
            if additional_data:
                for key,data in additional_data: print(f" |-- {key}: {data}")
    if not flag: print("[-] Flag not found")

def terminate(processes:list) -> None:
    for process in processes: process.terminate()

def units(inpt:str,pipe:Pipe=None, lock:Lock=None) -> list:
    #units = [ Unit(pipe=pipe,lock=lock) for _ in range(1) ]
    units = list()
    units.append(Ook(pipe=pipe,lock=lock))
    units.append(Brainfuck(pipe=pipe,lock=lock))
    return [ unit.input(inpt).clean() for unit in units ]