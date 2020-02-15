
def flag(result:tuple) -> None:
    if result:
        ((category,name),result,additional_data) = result
        print(f"[+] Flag found!")
        print(f" | Flag:\t{result[0]}")
        print(f" | Category:\t{category}")
        print(f" | Unit:\t{name}")
        if additional_data:
            for key,data in additional_data: print(f" |-- {key}: {data}")
    else: print("[-] Flag not found")