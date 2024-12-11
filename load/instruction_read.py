def iparse(filepath):
    load = []
    unload = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    if line.startswith("Action: Load, "):
                        name = line.split("Name: ")[1].split(",")[0]
                        load.apped(name)
                    if line.startswith("Action: Unload, "):
                        name = line.split("Name: ")[1].split(",")[0]
                        unload.append(name)
    except FileNotFoundError:
        print("Error: Manifest file not found.")
    except Exception as e:
        print(f"Error while parsing: {e}")
    return load, unload