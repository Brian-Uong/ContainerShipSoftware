import heapq
import manifest_read
from collections import Counter
import copy
import time

MAX_BAY_Y = 10
SAIL_BAY_Y = 8
MAX_BAY_X = 12
MAX_BUFFER_Y = 4
MAX_BUFFER_X = 24
MAX_BUFFER_CONTAINERS = 96
testx = 5
testy = 4

class BoardState:
    def __init__(self, bay, neededOff, currentOff, g, parent):
        self.neededOff = neededOff
        self.currentOff = currentOff
        self.bay = bay
        self.g = g
        self.h = self.heuristic()
        self.parent = parent
        self.f = self.g + self.h
        print(f"BoardState created: g={self.g}, h={self.h}, f={self.f}")

    def heuristic(self):
        return 0

    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return (
            sorted(self.bay.items()) == sorted(other.bay.items()) and
            Counter(self.currentOff) == Counter(other.currentOff)
        )
    
    def __hash__(self):
        bay_hash = frozenset((i, tuple(row)) for i, row in enumerate(self.bay))
        currentOff_hash = frozenset((container.name, container.weight) for container in self.currentOff)
        return hash((bay_hash, currentOff_hash))

    def PrintState(self):
        print("Current state of the bay:")
        name_width = 14
        weight_width = 5

        for row in range(len(self.bay[0]) - 1, -1, -1):
            for column in range(len(self.bay)):
                if column in self.bay and row < len(self.bay[column]):
                    container = self.bay[column][row]
                    name = f"{container.name}".ljust(name_width)
                    weight = f"{container.weight}".ljust(weight_width)
                    print(f"| {name} {weight} |", end='')
                else:
                    empty_name = "UNUSED".ljust(name_width)
                    empty_weight = "0".ljust(weight_width)
                    print(f"| {empty_name} {empty_weight} |", end='')
            print()

        print("\nNeeded Off:")
        for container in self.neededOff:
            print(f"  - Name: {container.name}, Weight: {container.weight}")

        print("\nCurrent Off:")
        for container in self.currentOff:
            print(f"  - Name: {container.name}, Weight: {container.weight}")
        print()


class Tree:
    def __init__(self):
        filepath = 'C:\\Users\\uongb\\Documents\\School\\Senior\\Fall\\CS 179M\\test_manifest2.txt'
        cont1 = manifest_read.A_Container(3000, '6LBdogs500')
        cont2 = manifest_read.A_Container(634, 'Maersk')
        neededOff = [cont1, cont2]
        currentOff = []
        print("Tree initialized with root BoardState.")
        self.root = BoardState(manifest_read.parse(filepath), neededOff, currentOff, 0, None)

    def isGoal(self, curr):
        # Check for balance in the bay
        left_weight = sum(
            container.weight
            for column, stack in enumerate(curr.bay[: MAX_BAY_X // 2])
            for container in stack
        )
        right_weight = sum(
            container.weight
            for column, stack in enumerate(curr.bay[MAX_BAY_X // 2 :])
            for container in stack
        )
        total_weight = left_weight + right_weight
        balance_check = abs(left_weight - right_weight) <= 0.1 * total_weight

        # Check if the needed containers have been offloaded
        offload_check = Counter(curr.neededOff) == Counter(curr.currentOff)

        # Combine both checks
        print("Checking goal state...")
        if balance_check and offload_check:
            print("Goal state confirmed.")
            return True

        print("Not a goal state.")
        return False

    def AStar(self):
        print("Starting A* search...")
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontierSet = {self.root}
        visitedSet = set()

        while frontier:
            print(f"Frontier size: {len(frontier)}")
            _, curr = heapq.heappop(frontier)
            frontierSet.remove(curr)

            print(f"Exploring state with f={curr.f} (g={curr.g}, h={curr.h})")
            curr.PrintState()

            if self.isGoal(curr):
                print("Goal state reached!")
                curr.PrintState()
                return

            visitedSet.add(curr)
            print("Expanding current state...")
            self.Expand(curr, frontier, frontierSet, visitedSet)

    def Expand(self, curr, frontier, frontierSet, visitedSet):
        print("Expanding children...")
        for column in range(len(curr.bay)):
            if column in curr.bay and curr.bay[column]:
                top = curr.bay[column].pop()
                row = len(curr.bay[column]) + 1
                position = (column + 1, row)
                print(f"Popped container '{top.name}' from position {position}")

                for otherColumn in range(len(curr.bay)):
                    if otherColumn == column:
                        continue

                    newBay = copy.deepcopy(curr.bay)
                    newRow = len(newBay[otherColumn]) + 1
                    newBay[otherColumn].append(top)

                    newCost = abs(position[0] - (otherColumn + 1)) + abs(position[1] - newRow)

                    child = BoardState(newBay, curr.neededOff, curr.currentOff, curr.g + newCost, curr)
                    print(f"Generated child state with container moved to column {otherColumn + 1}, f={child.f} (g={child.g}, h={child.h})")

                    if child not in visitedSet and child not in frontierSet:
                        heapq.heappush(frontier, (child.f, child))
                        frontierSet.add(child)

                newBay = copy.deepcopy(curr.bay)
                newCurrOff = curr.currentOff[:]
                newCurrOff.append(top)
                newCost = abs(position[0]) + abs(position[1] - (len(curr.bay[0]) + 1)) + 4

                child = BoardState(newBay, curr.neededOff, newCurrOff, curr.g + newCost, curr)
                print(f"Generated child state with container removed, f={child.f} (g={child.g}, h={child.h})")

                if child not in visitedSet and child not in frontierSet:
                    print("Adding child to frontier.")
                    heapq.heappush(frontier, (child.f, child))
                    frontierSet.add(child)

def main():
    start_time = time.time()

    tree = Tree()
    tree.AStar()

    end_time = time.time()

    runtime_seconds = end_time - start_time
    runtime_minutes = runtime_seconds / 60

    print(f"Runtime: {runtime_seconds:.2f} seconds ({runtime_minutes:.2f} minutes)")

if __name__ == "__main__":
    main()