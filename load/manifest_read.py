from collections import defaultdict

class A_Container:
    def __init__(self, weight, name):
        self.weight = weight
        self.name = name

    def __eq__(self, other):
        if isinstance(other, A_Container):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

class Display_Container:
    def __init__(self, x, y, weight, name):
        self.weight = weight
        self.name = name
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash(self.name)

def parse(file_path):
    grid = defaultdict(list)
    display_Grid = defaultdict(list)

    num_columns = 12
    for i in range(num_columns):
        grid[i] = []

    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(", ")
                    indices = parts[0].strip("[]").split(",")
                    y_index = int(indices[0]) - 1
                    x_index = int(indices[1]) - 1
                    weight = int(parts[1].strip("{}"))
                    name = parts[2]
                    
                    display_Container = Display_Container(x_index, y_index, weight, name)
                    display_Grid[x_index].append(display_Container)

                    if name == "UNUSED" and weight == 0:
                        continue

                    container = A_Container(weight, name)
                    grid[x_index].append(container)

    except FileNotFoundError:
        print("Error: Manifest file not found.")
    except Exception as e:
        print(f"Error while parsing: {e}")
    return grid, display_Grid


