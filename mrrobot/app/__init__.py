from os.path import isfile
from time import perf_counter as counter
from multiprocessing import active_children, Lock, Pipe, Process

from app.units import UnitLoader
from app.configuration import Configuration
from app.arguments import parse as argparser

from units.esoteric.ook import Unit as Ook
from units.esoteric.brainfuck import Unit as Brainfuck

istimeout = lambda start,timeout: bool(timeout > 0 and not start or not timeout or counter() - start >= timeout)

def arguments():
    arguments = argparser()
    if isfile(arguments.input):
        with open(arguments.input,"rb") as f: arguments.input = f.read()
    return arguments

def configuration(arguments) -> Configuration:
    # Create the configurator
    configuration:Configuration = Configuration()
    # Create/Load the config file
    configuration.load(arguments.config,clean=arguments.clean)
    # Override configuration with arguments
    configuration.set_encoding(arguments.encoding)
    configuration.set_flag(arguments.flag)
    configuration.set_timeout(arguments.timeout)
    # Return the configuration
    return configuration

def execution(processes:list) -> None:
    for process in processes: process.start()

def processes(units:list) -> list:
    return [ Process(target=unit.run,name=f"{unit.ID[0]}::{unit.ID[1]}") for unit in units ]

def search(processes:list,pipe:Pipe,start:float=None,timeout:float=None) -> tuple:
    while len(active_children()) > 0 and not istimeout(start,timeout):
        if pipe.poll(): return pipe.recv()

def terminate(processes:list) -> None:
    for process in processes: process.terminate()

def units(inpt,config:Configuration,pipe:Pipe=None, lock:Lock=None) -> list:
    unitloader = UnitLoader()
    available_units = unitloader.load()
    units = [ available_units[category][unitname].Unit(config=config,pipe=pipe,lock=lock) \
        for category in available_units for unitname in available_units[category] ]
    inpt = inpt if type(inpt) is bytes else bytes(inpt,encoding=config.ENCODING)
    return [ unit.input(inpt).clean() for unit in units ]