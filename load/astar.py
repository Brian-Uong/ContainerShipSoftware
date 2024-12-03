import heapq
import manifest_read
from collections import Counter

MAX_BAY_Y = 10
SAIL_BAY_Y = 8
MAX_BAY_X = 12
MAX_BUFFER_Y = 4
MAX_BUFFER_X = 24
MAX_BUFFER_CONTAINERS = 96
testx = 5
testy = 4
testbayx = 7
textbayy = 2

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

    def PrintState(self):
        print("Current state of the bay:")
        name_width = 12
        weight_width = 5

        for row in range(testy - 1, -1, -1):
            for column in range(testx):
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
        filepath = 'C:\\Users\\matth\\OneDrive\\Desktop\\HW\\CS 179\\BEAM-Solutions-Project\\load\\test_manifest2.txt'
        cont1 = manifest_read.Container(3000, '6LBdogs500')
        cont2 = manifest_read.Container(634, 'Maersk')
        neededOff = [cont1, cont2]
        currentOff = []
        print("Tree initialized with root BoardState.")
        self.root = BoardState(manifest_read.parse(filepath), neededOff, currentOff, 0, None)
    
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
        for column in range(testx):
            if column in curr.bay and curr.bay[column]:
                top = curr.bay[column][-1]
                row = len(curr.bay[column])
                position = (column + 1, row + 1)
                print(f"Popped container '{top.name}' from position {position}")

                # for otherColumn in range(curr.testx):
                #     if otherColumn == column:
                #         continue

                #     newBay = {key: list(value) for key, value in curr.bay.item }

                #     for col in range(curr.testx):
                #         if col not in newBay:
                #             newBay[col] = []

                #     oldY = top.y
                #     oldX = top.x
                #     top.y = len(newBay[otherColumn]) + 1
                #     top.x = otherColumn + 1
                #     newBay[otherColumn].append(top)
                #     newCost = abs(oldX - top.x) + abs(oldY - top.y)

                #     child = BoardState(newBay, newCost, curr, curr.currentOff)

                #     if child not in visitedSet and child not in frontierSet:
                #         heapq.heappush(frontier, (child.f, child))
                #         frontierSet.add(child)

                newBay = {key: list(value) for key, value in curr.bay.items()}
                newCost = abs(position[0]) + abs(position[1] - (testy + 1)) + 4
                newCurrOff = curr.currentOff + [top]

                newBay[column].pop()

                child = BoardState(newBay, curr.neededOff, newCurrOff, curr.g + newCost, curr)
                print(f"Generated child state with f={child.f} (g={child.g}, h={child.h})")

                if child not in visitedSet and child not in frontierSet:
                    print("Adding child to frontier.")
                    heapq.heappush(frontier, (child.f, child))
                    frontierSet.add(child)

    def isGoal(self, curr):
        print("Checking goal state...")
        if Counter(curr.neededOff) == Counter(curr.currentOff):
            print("Goal state confirmed.")
            return True
        print("Not a goal state.")
        return False

def main():
    tree = Tree()
    tree.AStar()

if __name__ == "__main__":
    main()
