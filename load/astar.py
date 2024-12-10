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
testx = 5
testy = 4

def debug_print(message):
    if DEBUG:
        print(message)

class BoardState:
    def __init__(self, bay, neededOff, currentOff, g, parent, move_description=None, move_positions=None):
        self.neededOff = neededOff
        self.currentOff = currentOff
        self.bay = bay
        self.g = g
        self.h = self.heuristic()
        self.parent = parent
        self.f = self.g + self.h
        self.move_description = move_description
        self.move_positions = move_positions or []
        debug_print(f"BoardState created: g={self.g}, h={self.h}, f={self.f}, move: {self.move_description}")

    def heuristic(self):
        totalCost = 0
        for needed in self.neededOff:
            found = False
            for column, stack in self.bay.items():
                for row, container in enumerate(stack):
                    if container == needed:
                        position = (column + 1, row + 1)
                        offloadCost = abs(position[0]) + abs(position[1] - (testy + 1)) + 4
                        totalCost += offloadCost
                        found = True
                        break
                if found:
                    break
        debug_print(f"Heuristic calculated: {totalCost}")
        return totalCost

    def validate_total_containers(self, initial_count):
        bay_count = sum(len(stack) for stack in self.bay.values())
        total_count = bay_count + len(self.currentOff)
        if total_count != initial_count:
            debug_print("ERROR: Container count mismatch!")
            debug_print(f"Expected: {initial_count}, Found: {total_count}")
            debug_print(f"Bay count: {bay_count}, Current Off count: {len(self.currentOff)}")
            self.PrintState()
            debug_print("Full Bay State:")
            for col, stack in self.bay.items():
                debug_print(f"  Column {col}: {[container.name for container in stack]}")
            debug_print("Full Current Off State:")
            debug_print([container.name for container in self.currentOff])
            raise ValueError("Container count mismatch")

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return (
            sorted(self.bay.items()) == sorted(other.bay.items()) and
            Counter(self.currentOff) == Counter(other.currentOff)
        )

    def __hash__(self):
        bay_hash = frozenset((k, tuple(v)) for k, v in sorted(self.bay.items()))
        currentOff_hash = frozenset((container.name, container.weight) for container in self.currentOff)
        return hash((bay_hash, currentOff_hash))

    def PrintState(self):
        print("Current state of the bay:")
        name_width = 14
        weight_width = 5

        for row in range(testx - 1, -1, -1):
            for column in range(testy):
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
        filepath = 'C:\\Users\\matth\\OneDrive\\Desktop\\HW\\CS 179\\BEAM-Solutions-Project\\load\\test_manifest.txt'
        cont1 = manifest_read.A_Container(3000, '6LBdogs500')
        cont2 = manifest_read.A_Container(634, 'Maersk')
        neededOff = [cont1, cont2]
        currentOff = []

        debug_print("Tree initialized with root BoardState.")
        grid, _ = manifest_read.parse(filepath)
        self.root = BoardState(grid, neededOff, currentOff, 0, None)
        self.initial_count = sum(len(stack) for stack in self.root.bay.values()) + len(self.root.currentOff)

    def trace_solution(self, goal_state):
        moves = []
        current = goal_state
        while current.parent:
            moves.append((current.move_description, current.move_positions))
            current = current.parent
        moves.reverse()
        print("\nSolution Moves:")
        for i, (desc, positions) in enumerate(moves, 1):
            print(f"{i}. {desc}")
            print(f"   Positions: Initial {positions[0]} -> Final {positions[1]}")
        return moves

    def AStar(self):
        debug_print("Starting A* search...")
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontierSet = {self.root}
        visitedSet = set()

        while frontier:
            debug_print(f"Frontier size: {len(frontier)}, Visited size: {len(visitedSet)}")
            _, curr = heapq.heappop(frontier)
            frontierSet.remove(curr)

            debug_print(f"Exploring state with f={curr.f} (g={curr.g}, h={curr.h})")
            curr.PrintState()

            if self.isGoal(curr):
                debug_print("Goal state reached!")
                curr.PrintState()
                return self.trace_solution(curr)
            
            visitedSet.add(curr)
            debug_print("Expanding current state...")
            self.Expand(curr, frontier, frontierSet, visitedSet)

    def Expand(self, curr, frontier, frontierSet, visitedSet):
        debug_print("Expanding children...")

        for column in range(testx):
            if column in curr.bay and curr.bay[column]:
                debug_print(f"  Exploring column {column} with {len(curr.bay[column])} containers...")
                
                top = curr.bay[column][-1]
                position = (column + 1, len(curr.bay[column]))
                debug_print(f"    Accessed container '{top.name}' from position {position}")

                for otherColumn in range(testx):
                    if otherColumn == column:
                        continue

                    debug_print(f"    Trying to move container to column {otherColumn}...")
                    newBay = copy.deepcopy(curr.bay)
                    newBay[column] = newBay[column][:-1]
                    newBay[otherColumn].append(top)

                    newCost = abs(position[0] - (otherColumn + 1)) + abs(position[1] - (len(newBay[otherColumn])))
                    move_description = f"Move '{top.name}' from column {column + 1} to column {otherColumn + 1}"
                    move_positions = [(column + 1, position[1]), (otherColumn + 1, len(newBay[otherColumn]))]
                    child = BoardState(newBay, curr.neededOff, copy.deepcopy(curr.currentOff), curr.g + newCost, curr, move_description, move_positions)
                    child.validate_total_containers(self.initial_count)

                    if child not in visitedSet and child not in frontierSet:
                        debug_print("      Adding child to frontier.")
                        heapq.heappush(frontier, (child.f, child))
                        frontierSet.add(child)

                newBay = copy.deepcopy(curr.bay)
                newBay[column] = newBay[column][:-1]
                newCurrOff = copy.deepcopy(curr.currentOff)
                newCurrOff.append(top)

                newCost = abs(position[0]) + abs(position[1] - (testy + 1)) + 4
                move_description = f"Move '{top.name}' from column {column + 1} to OFFLOAD"
                move_positions = [(column + 1, position[1]), "OFFLOAD"]
                child = BoardState(newBay, curr.neededOff, newCurrOff, curr.g + newCost, curr, move_description, move_positions)
                child.validate_total_containers(self.initial_count)

                if child not in visitedSet and child not in frontierSet:
                    debug_print("      Adding child to frontier.")
                    heapq.heappush(frontier, (child.f, child))
                    frontierSet.add(child)

    def isGoal(self, curr):
        debug_print("Checking goal state...")
        if Counter(curr.neededOff) == Counter(curr.currentOff):
            debug_print("Goal state confirmed.")
            return True
        debug_print("Not a goal state.")
        return False

def main():
    start_time = time.time()

    tree = Tree()
    moves = tree.AStar()

    end_time = time.time()

    runtime_seconds = end_time - start_time
    runtime_minutes = runtime_seconds / 60

    print(f"Runtime: {runtime_seconds:.2f} seconds ({runtime_minutes:.2f} minutes)")
    print("\nMoves as a list:")
    print(moves)

if __name__ == "__main__":
    main()
