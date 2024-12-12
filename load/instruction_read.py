import sys, os
def iparse(filepath):
    load = []
    unload = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip():
                    if line.startswith("Action: Load, "):
                        name = line.split("Name: ")[1].split(",")[0]
                        load.append(name)
                    if line.startswith("Action: Unload, "):
                        name = line.split("Name: ")[1].split(",")[0]
                        unload.append(name)
    except FileNotFoundError:
        print("Error: Instrucions file not found.")
    except Exception as e:
        print(f"Error while parsing: {e}")
    return load, unload

def main():
    load, unload = iparse('C:\\Users\\edech\\Documents\\BEAM-Solutions-Project\\Website\\ManifestFolder\\' + sys.argv[1])
    print(load)
    print(unload)

if __name__ == "__main__":
    main()