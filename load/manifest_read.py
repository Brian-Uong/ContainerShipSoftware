from collections import defaultdict

class Container:
    def __init__(self, weight, name):
        self.weight = weight
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Container):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

def parse(file_path):
    grid = defaultdict(list)

    num_columns = 5
    for i in range(num_columns):
        grid[i] = []

    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(", ")
                    indices = parts[0].strip("[]").split(",")
                    x_index = int(indices[1]) - 1
                    weight = int(parts[1].strip("{}"))
                    name = parts[2]
                    
                    if name == "UNUSED" and weight == 0:
                        continue

                    container = Container(weight, name)
                    grid[x_index].append(container)
    except FileNotFoundError:
        print("Error: Manifest file not found.")
    except Exception as e:
        print(f"Error while parsing: {e}")
    return grid


