import heapq
import manifest_read
from collections import Counter
import copy
import time

DEBUG = True

MAX_BAY_Y = 10
SAIL_BAY_Y = 8
MAX_BAY_X = 12
MAX_BUFFER_Y = 4
MAX_BUFFER_X = 24
MAX_BUFFER_CONTAINERS = 96
testX = 5
testY = 4
testBuffer = 2

def debugPrint(message):
    if DEBUG:
        print(message)

class BoardState:
    def __init__(self, bay, neededOff, currentOff, g, parent, moveDescription=None, movePositions=None):
        self.neededOff = neededOff
        self.currentOff = currentOff
        self.bay = bay
        self.g = g
        self.h = self.heuristic()
        self.parent = parent
        self.f = self.g + self.h
        self.depth = (parent.depth + 1) if parent else 0
        self.moveDescription = moveDescription
        self.movePositions = movePositions or []
        debugPrint(f"BoardState created: g={self.g}, h={self.h}, f={self.f}, depth={self.depth}, move: {self.moveDescription}")

    def heuristic(self):
        totalCost = 0
        for needed in self.neededOff:
            found = False
            for column, stack in self.bay.items():
                for row, container in enumerate(stack):
                    if container == needed:
                        position = (column + 1, row + 1)
                        offloadCost = abs(position[0]) + abs(position[1] - (testY + 1)) + 4
                        totalCost += offloadCost
                        found = True
                        break
                if found:
                    break
        debugPrint(f"Heuristic calculated: {totalCost}")
        return totalCost

    def validateTotalContainers(self, initialCount):
        bayCount = sum(len(stack) for stack in self.bay.values())
        totalCount = bayCount + len(self.currentOff)
        if totalCount != initialCount:
            debugPrint("ERROR: Container count mismatch!")
            debugPrint(f"Expected: {initialCount}, Found: {totalCount}")
            debugPrint(f"Bay count: {bayCount}, Current Off count: {len(self.currentOff)}")
            self.printState()
            debugPrint("Full Bay State:")
            for col, stack in self.bay.items():
                debugPrint(f"  Column {col}: {[container.name for container in stack]}")
            debugPrint("Full Current Off State:")
            debugPrint([container.name for container in self.currentOff])
            raise ValueError("Container count mismatch")

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return (
            sorted(self.bay.items()) == sorted(other.bay.items()) and
            Counter(self.currentOff) == Counter(other.currentOff)
        )

    def __hash__(self):
        bayHash = frozenset((k, tuple(v)) for k, v in sorted(self.bay.items()))
        currentOffHash = frozenset((container.name, container.weight) for container in self.currentOff)
        return hash((bayHash, currentOffHash))

    def printState(self):
        print("Current state of the bay:")
        nameWidth = 14
        weightWidth = 5

        for row in range(testX - 1, -1, -1):
            for column in range(testY):
                if column in self.bay and row < len(self.bay[column]):
                    container = self.bay[column][row]
                    name = f"{container.name}".ljust(nameWidth)
                    weight = f"{container.weight}".ljust(weightWidth)
                    print(f"| {name} {weight} |", end='')
                else:
                    emptyName = "UNUSED".ljust(nameWidth)
                    emptyWeight = "0".ljust(weightWidth)
                    print(f"| {emptyName} {emptyWeight} |", end='')
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
        filePath = 'C:\\Users\\matth\\OneDrive\\Desktop\\HW\\CS 179\\BEAM-Solutions-Project\\load\\test_manifest.txt'
        cont1 = manifest_read.A_Container(3000, '6LBdogs500')
        cont2 = manifest_read.A_Container(634, 'Maersk')
        neededOff = [cont1, cont2]
        currentOff = []

        debugPrint("Tree initialized with root BoardState.")
        grid, _ = manifest_read.parse(filePath)
        self.root = BoardState(grid, neededOff, currentOff, 0, None)
        self.initialCount = sum(len(stack) for stack in self.root.bay.values()) + len(self.root.currentOff)

        self.statesExpanded = 0
        self.maxDepthReached = 0
        self.totalNodesGenerated = 0

    def traceSolution(self, goalState):
        moves = []
        current = goalState
        while current.parent:
            moves.append((current.moveDescription, current.movePositions))
            current = current.parent
        moves.reverse()
        print("\nSolution Moves:")
        for i, (desc, positions) in enumerate(moves, 1):
            print(f"{i}. {desc}")
            print(f"   Positions: Initial {positions[0]} -> Final {positions[1]}")
        return moves

    def aStar(self):
        debugPrint("Starting A* search...")
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontierSet = {self.root}
        visitedSet = set()

        while frontier:
            debugPrint(f"Frontier size: {len(frontier)}, Visited size: {len(visitedSet)}")
            _, curr = heapq.heappop(frontier)
            frontierSet.remove(curr)

            self.statesExpanded += 1
            self.maxDepthReached = max(self.maxDepthReached, curr.depth)

            debugPrint(f"Exploring state with f={curr.f} (g={curr.g}, h={curr.h})")
            curr.printState()

            if self.isGoal(curr):
                curr.printState()
                print("\nSearch Statistics:")
                print(f"  Total States Expanded: {self.statesExpanded}")
                print(f"  Maximum Depth Reached: {self.maxDepthReached}")
                print(f"  Total Nodes Generated: {self.totalNodesGenerated}")
                return self.traceSolution(curr)
            
            visitedSet.add(curr)
            debugPrint("Expanding current state...")
            self.expand(curr, frontier, frontierSet, visitedSet)

    def expand(self, curr, frontier, frontierSet, visitedSet):
        debugPrint(f"Expanding children of node at depth {curr.depth}...")

        for column in range(testX):
            if column in curr.bay and curr.bay[column]:
                debugPrint(f"  Exploring column {column} with {len(curr.bay[column])} containers...")

                top = curr.bay[column][-1]
                position = (column + 1, len(curr.bay[column]))
                debugPrint(f"    Accessed container '{top.name}' from position {position}")

                if top.name == "NAN" and top.weight == 00000:
                    debugPrint(f"    Skipping container '{top.name}' with weight '{top.weight}' as it is not movable.")
                    continue

                for otherColumn in range(testX):
                    if otherColumn == column:
                        continue

                    debugPrint(f"    Trying to move container to column {otherColumn}...")
                    newBay = copy.deepcopy(curr.bay)
                    newBay[column] = newBay[column][:-1]
                    newBay[otherColumn].append(top)

                    newCost = abs(position[0] - (otherColumn + 1)) + abs(position[1] - (len(newBay[otherColumn])))
                    moveDescription = f"Move '{top.name}' from column {column + 1} to column {otherColumn + 1}"
                    movePositions = [(column + 1, position[1]), (otherColumn + 1, len(newBay[otherColumn]))]
                    child = BoardState(newBay, curr.neededOff, copy.deepcopy(curr.currentOff), curr.g + newCost, curr, moveDescription, movePositions)
                    child.validateTotalContainers(self.initialCount)

                    debugPrint(f"      Generated child node at depth {child.depth}")
                    self.totalNodesGenerated += 1

                    if child not in visitedSet and child not in frontierSet:
                        debugPrint(f"      Adding child node at depth {child.depth} to frontier.")
                        heapq.heappush(frontier, (child.f, child))
                        frontierSet.add(child)

                newBay = copy.deepcopy(curr.bay)
                newBay[column] = newBay[column][:-1]
                newCurrOff = copy.deepcopy(curr.currentOff)
                newCurrOff.append(top)

                newCost = abs(position[0]) + abs(position[1] - (testY + 1)) + 4
                moveDescription = f"Move '{top.name}' from column {column + 1} to OFFLOAD"
                movePositions = [(column + 1, position[1]), "OFFLOAD"]
                child = BoardState(newBay, curr.neededOff, newCurrOff, curr.g + newCost, curr, moveDescription, movePositions)
                child.validateTotalContainers(self.initialCount)

                debugPrint(f"      Generated child node at depth {child.depth}")
                self.totalNodesGenerated += 1

                if child not in visitedSet and child not in frontierSet:
                    debugPrint(f"      Adding child node at depth {child.depth} to frontier.")
                    heapq.heappush(frontier, (child.f, child))
                    frontierSet.add(child)

    def isGoal(self, curr):
        debugPrint("Checking goal state...")
        if Counter(curr.neededOff) == Counter(curr.currentOff):
            debugPrint("Goal state confirmed.")
            return True
        debugPrint("Not a goal state.")
        return False


def main():
    startTime = time.time()

    tree = Tree()
    moves = tree.aStar()

    endTime = time.time()

    runtimeSeconds = endTime - startTime
    runtimeMinutes = runtimeSeconds / 60

    print(f"Runtime: {runtimeSeconds:.2f} seconds ({runtimeMinutes:.2f} minutes)")
    print("\nMoves as a list:")
    print(moves)

if __name__ == "__main__":
    main()
