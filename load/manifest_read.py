from collections import defaultdict

class Container:
    def __init__(self, x, y, weight, name):
        self.x = x
        self.y = y
        self.weight = weight
        self.name = name

def parse():
    grid = defaultdict(list)

    try:
        with open('./manifest.txt', 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(", ")
                    yx = parts[0].strip("[]").split(",")
                    y = int(yx[0]) - 1
                    x = int(yx[1]) - 1
                    weight = int(parts[1].strip("{}"))
                    name = parts[2]
                    container = Container(x + 1, y + 1, weight, name)
                    
                    if name != "UNUSED" or weight != 0:
                        print(x + 1, y + 1, weight, name)
                        grid[x].append(container)
    except FileNotFoundError:
        print("Error: Manifest file not found.")
    except Exception as e:
        print(f"Error while parsing: {e}")
    return grid

