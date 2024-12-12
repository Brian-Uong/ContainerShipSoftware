
from collections import Counter, defaultdict
import manifest_read
import heapq
import time
import copy

DEBUG = False

MAX_BAY_Y = 12
SAIL_BAY_Y = 8
MAX_BAY_X = 12
MAX_BUFFER_Y = 4
MAX_BUFFER_X = 24
MAX_BUFFER_CONTAINERS = 96
testx = 5
testy = 4
testBufferX = 2
testBufferY = 2

def SIFT(board):
    bay = board.bay
    sorted_containers = []
    #put all containers in buffer

    #logically, sort by weight
    for i in range(len(bay)):
        for j in range(board.MAX_BAY_X/2, board.MAX_BAY_X):
            sorted_container.append(bay[i][j])
    sorted_container.sort(key=lambda x: x.weight, reverse=True)
    print(sorted_container)
    #starting with the [01,06], put the heaviest container. The second heaviest goes in [01,07]
    #third heaviest in [01,05] etc. When first row is filled, go to second row and so on

def debugPrint(message):
    if DEBUG:
        print(message)


class BoardState:
    def __init__(self, bay, g, parent, moveDescription=None, movePositions=None):
        self.bay = bay
        #self.buffer = buffer
        self.g = g
        self.h = self.heuristic()
        self.parent = parent
        self.f = self.g + self.h
        self.depth = (parent.depth + 1) if parent else 0
        self.moveDescription = moveDescription
        self.movePositions = movePositions or []
        debugPrint(f"BoardState created: g={self.g}, h={self.h}, f={self.f}, depth={self.depth}, move: {self.moveDescription}")

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return (
            sorted(self.bay.items()) == sorted(other.bay.items())
        )
    
    def __hash__(self):
        bayHash = frozenset((k, tuple(v)) for k, v in sorted(self.bay.items()))
        #bufferHash = frozenset((k, tuple(v)) for k, v in sorted(self.buffer.items()))
        #change to balance value
        #currentOffHash = frozenset((container.name, container.weight) for container in self.currentOff)
        return hash((bayHash))

    def heuristic(self):
        return 0

    def printState(self):
        print("Current state of the bay and buffer:")
        nameWidth = 1
        weightWidth = 1

        print("Bay State:")
        for row in range(MAX_BAY_X - 1, -1, -1):
            for column in range(MAX_BAY_Y):
                if column in self.bay and row < len(self.bay[column]):
                    container = self.bay[column][row]
                    name = f"{container.name}".ljust(nameWidth)
                    weight = f"{container.weight}".ljust(weightWidth)
                    print(f"|{name} {weight}|", end='')
                else:
                    emptyName = "UNUSED".ljust(nameWidth)
                    emptyWeight = "0".ljust(weightWidth)
                    print(f"| {emptyName} {emptyWeight} |", end='')
            print()



class Tree:
    def __init__(self):

        filepath = 'C:\\Users\\emily\\Documents\\GitHub\\BEAM-Solutions-Project\\load\\ShipCase4.txt'
        debugPrint("Tree initialized with root BoardState.")
        grid, _ = manifest_read.parse(filepath)
        self.root = BoardState(grid, 0, None) 

        debugPrint("Tree initialized with root BoardState.")

    def AStar(self):
        debugPrint("Starting A* search...")
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontierSet = {self.root}
        visitedSet = set()

        while frontier:
            debugPrint(f"Frontier size: {len(frontier)}")
            
            _, curr = heapq.heappop(frontier)
            frontierSet.remove(curr)

            left = self.leftWeight(curr)
            right = self.rightWeight(curr)
            side = self.heavySide(left, right)

            debugPrint(f"Exploring state with f={curr.f} (g={curr.g}, h={curr.h})")
            curr.printState()

            if self.isGoal(left, right):
                print("Goal state reached!")
                curr.printState()
                return

            visitedSet.add(curr)
            print("Expanding current state...")
            self.Expand(curr, frontier, frontierSet, visitedSet, side)

            print(f"Left: {left}, right: {right}")

            print("Failed to find a solution: Frontier is empty.")

            
            #input("Press Enter to continue to the next step...")

    def Expand(self, curr, frontier, frontierSet, visitedSet, side):
        print("Expanding children...")

        if side == "left":
            for column in range(MAX_BAY_X // 2):
                if column in curr.bay and curr.bay[column]:
                    top = curr.bay[column][-1]
                    if top.name == "NAN" and top.weight == 0:
                        debugPrint(f"    Skipping container '{top.name}' with weight '{top.weight}' as it is not movable.")
                        continue

                    top = curr.bay[column].pop()
                    row = len(curr.bay[column])
                    position = (column + 1, row + 1)
                    print(f"Popped container '{top.name}' from position {position}")
                    appended = False

                    for otherColumn in range(MAX_BAY_X // 2, MAX_BAY_X):
                        if otherColumn == column:
                            continue

                        if not appended:
                            newBay = copy.deepcopy(curr.bay)
                            newRow = len(newBay[otherColumn]) + 1
                            newBay[otherColumn].append(top)
                            appended = True

                            newCost = abs(position[0] - (otherColumn + 1)) + abs(position[1] - newRow)

                            child = BoardState(newBay, curr.g + newCost, curr)
                            print(f"Generated child state with container moved to column {otherColumn + 1}, f={child.f} (g={child.g}, h={child.h})")

                            if child not in visitedSet and child not in frontierSet:
                                heapq.heappush(frontier, (child.f, child))
                                frontierSet.add(child)

                            appended = True
                            break

                    if appended:
                        break

        elif side == "right":
            for column in range(MAX_BAY_X // 2, MAX_BAY_X):
                if column in curr.bay and curr.bay[column]:
                    top = curr.bay[column][-1]
                    if top.name == "NAN" and top.weight == 0:
                        debugPrint(f"    Skipping container '{top.name}' with weight '{top.weight}' as it is not movable.")
                        continue

                    top = curr.bay[column].pop()
                    row = len(curr.bay[column])
                    position = (column + 1, row + 1)
                    print(f"Popped container '{top.name}' from position {position}")
                    appended = False

                    for otherColumn in reversed(range(MAX_BAY_X // 2)):
                        if otherColumn == column:
                            continue

                        if not appended:
                            newBay = copy.deepcopy(curr.bay)
                            newRow = len(newBay[otherColumn]) + 1
                            newBay[otherColumn].append(top)
                            appended = True

                            newCost = abs(position[0] - (otherColumn + 1)) + abs(position[1] - newRow)

                            child = BoardState(newBay, curr.g + newCost, curr)
                            print(f"Generated child state with container moved to column {otherColumn + 1}, f={child.f} (g={child.g}, h={child.h})")

                            if child not in visitedSet and child not in frontierSet:
                                heapq.heappush(frontier, (child.f, child))
                                frontierSet.add(child)

                            appended = True
                            break

                    if appended:
                        break



    def isGoal(self, left_weight, right_weight):
        total_weight = left_weight + right_weight
        print(f"Diff {abs(left_weight - right_weight)}")
        print(f"10% {0.1*total_weight}")
        print(f"Left {left_weight}, right {right_weight}")
        return abs(left_weight - right_weight) <= 0.1 * total_weight

    def leftWeight(self, curr):
        left_weight = 0
        for i in range(MAX_BAY_X // 2):
            for container in curr.bay[i]:
                debugPrint(f"left container weight: {container.weight}")
                left_weight += container.weight
        
        return left_weight

    def rightWeight(self, curr):
        right_weight = 0
        for i in range(MAX_BAY_X // 2, MAX_BAY_X):
            for container in curr.bay[i]:
                debugPrint(f"right container weight: {container.weight}")
                right_weight += container.weight

        return right_weight

    def heavySide(self, left, right):
        if left > right:
            return "left"
        elif right > left:
            return "right"

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