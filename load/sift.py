
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

def debugPrint(message):
    if DEBUG:
        print(message)


class BoardState:
    def __init__(self, bay, buffer, g, parent, moveDescription=None, movePositions=None):
        self.bay = bay
        self.buffer = buffer
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
            for column in range(testy):
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



class BalanceTree:
    def __init__(self, filepath):
        debugPrint("Tree initialized with root BoardState.")
        grid, _ = manifest_read.parse(filepath)
        buffer = defaultdict(list)
        for i in range(MAX_BUFFER_X):
            buffer[i] = []
        self.root = BoardState(grid, buffer, 0, None) 

        debugPrint("Tree initialized with root BoardState.")

    def AStar(self):
        debugPrint("Starting A* search...")
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontierSet = {self.root}
        visitedSet = set()

        siftgoal = self.siftGoal(self.root, self.root.buffer)
        print("Sift goal state")
        siftgoal.printState()
        sift = SiftTree(self.root.bay, siftgoal)
        sift.astar()

        #bayCount = sum(len(stack) for stack in self.root.values())
        #if bayCount == 0 or bayCount == 1:
            #print("This balance will require 0 moves, taking 0 minutes.")
            #return

        """ while frontier:
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

            print(f"Left: {left}, right: {right}") """



            #input("Press Enter to continue to the next step...")

        #call sift
        print("Unable to perform balancing, now attempting SIFT.")
        siftGoal = siftGoal(self.root, self.root.buffer)
        sift = SiftTree(self.root, siftGoal)
        sift.astar()

    def Expand(self, curr, frontier, frontierSet, visitedSet, side):
        print("Expanding children...")

        if side == "left":
            for column in range(testx // 2):
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

                    for otherColumn in range(testx // 2, testx):
                        if otherColumn == column:
                            continue

                        if not appended:
                            newBay = copy.deepcopy(curr.bay)
                            newRow = len(newBay[otherColumn]) + 1
                            newBay[otherColumn].append(top)
                            appended = True

                            newCost = abs(position[0] - (otherColumn + 1)) + abs(position[1] - newRow)

                            child = BoardState(newBay, self.root.buffer, curr.g + newCost, curr)
                            print(f"Generated child state with container moved to column {otherColumn + 1}, f={child.f} (g={child.g}, h={child.h})")

                            if child not in visitedSet and child not in frontierSet:
                                heapq.heappush(frontier, (child.f, child))
                                frontierSet.add(child)

                            appended = True
                            break

                    if appended:
                        break

        elif side == "right":
            for column in range(testx // 2, testx):
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

                    for otherColumn in reversed(range(testx // 2)):
                        if otherColumn == column:
                            continue

                        if not appended:
                            newBay = copy.deepcopy(curr.bay)
                            newRow = len(newBay[otherColumn]) + 1
                            newBay[otherColumn].append(top)
                            appended = True

                            newCost = abs(position[0] - (otherColumn + 1)) + abs(position[1] - newRow)

                            child = BoardState(newBay, self.root.buffer, curr.g + newCost, curr)
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
        debugPrint(f"Diff {abs(left_weight - right_weight)}")
        debugPrint(f"10% {0.1*total_weight}")
        debugPrint(f"Left {left_weight}, right {right_weight}")
        return abs(left_weight - right_weight) <= 0.1 * total_weight

    def leftWeight(self, curr):
        left_weight = 0
        for i in range(testx // 2):
            for container in curr.bay[i]:
                debugPrint(f"left container weight: {container.weight}")
                left_weight += container.weight
        
        return left_weight

    def rightWeight(self, curr):
        right_weight = 0
        for i in range(testx // 2, testx):
            for container in curr.bay[i]:
                debugPrint(f"right container weight: {container.weight}")
                right_weight += container.weight

        return right_weight

    def heavySide(self, left, right):
        if left > right:
            return "left"
        elif right > left:
            return "right"
        
    def siftGoal(self, board, buffer):
        sorted_containers = []

        for row in range(len(board.bay)):
            for container in board.bay[row]:
                if container.name != "NAN": 
                    sorted_containers.append(container)
        sorted_containers.sort(key=lambda x: x.weight, reverse=True)
        debugPrint(sorted_containers)

        newBay = defaultdict(list)
        for i in range(testx):
            newBay[i] = []
        for row in range(len(board.bay)):
            for container in board.bay[row]:
                if container.name == "NAN":
                    newBay[row].append(container)

        count = 0

        while sorted_containers:
            for col in range(testx):
                container = sorted_containers[0]

                if len(newBay[col]) > count:
                    continue
                
                newBay[col].append(container)
                sorted_containers = sorted_containers[1:]

            count += 1




        # for container in sorted_containers:
        #     placed = False
        #     count = 0
        #     for row in range(len(board.bay)):
        #         for col in range(len(newBay[row]), len(board.bay[row])):
        #             if col > count:
        #                 continue
        #             #need to wrap the columns somehow
        #             if col >= len(board.bay[row]):
        #                 col = 0
        #                 break
                    
        #             newBay[row].append(container)
        #             placed = True
        #             break

        #         count+=1
                
        #         if placed:
        #             break 

        sortedBay = BoardState(newBay, buffer, 0, None)
        return sortedBay
    

        
class SiftTree:
    def __init__(self, grid, goal_state):
        buffer = defaultdict(list)
        for i in range(testx):
            buffer[i] = []
        self.goal_state = goal_state
        self.root = BoardState(grid, buffer, 0, None)
        debugPrint("Tree initialized with root BoardState.")

    def astar(self):
        debugPrint("Starting A* search for SIFT...")
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontierSet = {self.root}
        visitedSet = set()

        while frontier:
            debugPrint(f"Frontier size: {len(frontier)}")
            _, curr = heapq.heappop(frontier)
            frontierSet.remove(curr)

            debugPrint(f"Exploring state with f={curr.f} (g={curr.g}, h={curr.h})")
            curr.printState()

            if self.isGoal(curr):
                print("Goal state reached!")
                curr.printState()
                return

            visitedSet.add(curr)
            print("Expanding current state...")
            self.Expand(curr, frontier, frontierSet, visitedSet)

            input("Press Enter to continue to the next step...")

        print("Failed to find a solution: Frontier is empty.")

    def isGoal(self, curr):
        return curr == self.goal_state

    def Expand(self, curr, frontier, frontierSet, visitedSet):
        for column in range(testx):
            if column in curr.bay and curr.bay[column]:
                top = curr.bay[column][-1]

                if top.name == "NAN" and top.weight == 0:
                    continue

                newBay = copy.deepcopy(curr.bay)
                top = newBay[column].pop()
                position = (column + 1, len(curr.bay[column]) + 1)

                for targetColumn in range(testx):
                    if targetColumn == column:
                        continue
                    if len(newBay[targetColumn]) < testy:
                        newBayCopy = copy.deepcopy(newBay)
                        newBayCopy[targetColumn].append(top)

                        newCost = abs(position[0] - (targetColumn + 1)) + len(newBayCopy[targetColumn])

                        child = BoardState(newBayCopy, curr.buffer, curr.g + newCost, curr)

                        if child not in visitedSet and child not in frontierSet:
                            heapq.heappush(frontier, (child.f, child))
                            frontierSet.add(child)

    def heuristic(self, curr):
        return 0



def main():
    start_time = time.time()
    filepath = 'C:\\Users\\emily\\Documents\\GitHub\\BEAM-Solutions-Project\\load\\test_manifest2.txt'
    tree = BalanceTree(filepath)
    tree.AStar()

    end_time = time.time()

    runtime_seconds = end_time - start_time
    runtime_minutes = runtime_seconds / 60

    print(f"Runtime: {runtime_seconds:.2f} seconds ({runtime_minutes:.2f} minutes)")

if __name__ == "__main__":
    main()