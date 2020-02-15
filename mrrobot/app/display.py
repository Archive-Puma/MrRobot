from time import perf_counter

# --- Colorama sucks ---

def colored(color:str="reset") -> str:
    MODE = { "reset": "0", "error": "31", "good": "32", "warn": "33", "info": "34" }
    return f"\033[{MODE[color]}m"

# --- Debuggin/logging/verbosity levels ---

def good(msg:str,decorator:str='+',append:bool=False) -> None:      show(msg,"good",decorator,append)
def info(msg:str,decorator:str='?',append:bool=False) -> None:      show(msg,"info",decorator,append)
def normal(msg:str,decorator:str='|',append:bool=True) -> None:     show(msg,"reset",decorator,append)
def error(msg:str,decorator:str='!',append:bool=False) -> None:     show(msg,"error",decorator,append)

# --- Colored printed ---

def show(msg:str,mode:str,decorator:str,append:bool) -> None:
    style = f"{colored(mode)} {decorator} {colored()}" if append else f"[{colored(mode)}{decorator}{colored()}]"
    print(f"{style} {msg}")

# --- Performance (execution time) ---

def performance(start:float=0) -> None:
    info(f"Execution time: {round(perf_counter() - start, 2)} seconds")

# --- Execution result ---

def flag(result:tuple) -> None:
    if result:
        ((category,name),result,additional_data) = result
        good(f"Flag found!")
        normal(f"Category:\t{category}")
        normal(f"Unit:\t{name}")
        normal(f"Flag:\t{result[0]}")
        if additional_data:
            for key,data in additional_data: normal(f"-- {key}: {data}")
    else: error("Flag not found")