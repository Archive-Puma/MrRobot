from os.path import isfile
from time import perf_counter as counter
from multiprocessing import active_children, Lock, Pipe, Process

from mrrobot.app.units import UnitLoader
from mrrobot.app.exception import Elliot
from mrrobot.app.configuration import Configuration
from mrrobot.app.arguments import parse as argparser

istimeout = lambda start,timeout: bool(timeout > 0 and not start or not timeout or counter() - start >= timeout)

def arguments() -> tuple:
    contents = None
    arguments = argparser()
    if isfile(arguments.input):
        with open(arguments.input,"rb") as f: contents = f.read()
    return arguments,contents

def check_requirements() -> None:
    # argparse
    try:        import argparse; del argparse
    except      ImportError: raise Elliot("Module argparse is not installed")
    # PIL (Pillow)
    try:        import PIL; del PIL
    except      ImportError: raise Elliot("Module Pillow is not installed")

def configuration(args) -> Configuration:
    # Create the configurator
    configuration:Configuration = Configuration()
    # Create/Load the config file
    configuration.load(args.config,clean=args.clean)
    # Override configuration with arguments
    configuration.set_encoding(args.encoding)
    configuration.set_flag(args.flag)
    configuration.set_timeout(args.timeout)
    if args.inside:
        if args.unit: configuration.set_inside(args.inside)
        else: raise Elliot("--inside requieres --unit to be used")
    # Disable all if only one unit is enabled
    if args.unit:
        category,name = None,None
        try: category,name = args.unit.split(".")
        except ValueError: raise Elliot("Bad unit specification (Format: category.name)")
        configuration.set_all_categories(enabled=False)
        configuration.enable_category(category)
        configuration.enable_only(name)
    # Disable all if one category at least is enabled
    if args.crypto or args.esoteric or args.forensics:
        configuration.set_all_categories(enabled=False)
        if args.crypto: configuration.enable_category("crypto")
        if args.esoteric: configuration.enable_category("esoteric")
        if args.forensics: configuration.enable_category("forensics")
    # All enabled
    if args.all: configuration.set_all_categories(enabled=True)
    # Return the configuration
    return configuration

def execution(processes:list) -> None:
    for process in processes: process.start()

def processes(units:list) -> list:
    return [ Process(target=unit.run,name=f"{unit.ID[0]}::{unit.ID[1]}") for unit in units ]

def search(processes:list,pipe:Pipe,start:float=None,timeout:float=None) -> tuple:
    while len(active_children()) > 0 and not istimeout(start,timeout):
        if pipe.poll(): return pipe.recv()
    if pipe.poll(timeout=0.0001): return pipe.recv()
    if istimeout(start,timeout): raise Elliot("Timeout reached")

def terminate(processes:list) -> None:
    for process in processes: process.terminate()

def units(challenge,config:Configuration,pipe:Pipe=None, lock:Lock=None) -> list:
    unitloader = UnitLoader()
    available_units = unitloader.load(config)
    units = [ available_units[category][unitname].Unit(config=config,pipe=pipe,lock=lock) \
        for category in available_units for unitname in available_units[category] ]
    inpt,contents = challenge
    inpt = inpt if type(inpt) is bytes else bytes(inpt,encoding=config.ENCODING)
    return [ unit.input((inpt,contents)).clean() for unit in units ]