from astar import BoardState
from collections import Counter
import manifest_read
import numpy as np
import heapq
import time
import copy


MAX_BAY_Y = 10
SAIL_BAY_Y = 8
MAX_BAY_X = 12
MAX_BUFFER_Y = 4
MAX_BUFFER_X = 24
MAX_BUFFER_CONTAINERS = 96
testx = 5
testy = 4



def get_weight_left(board):
    left = 0
    bay = board.bay

    for i in range(len(bay)):
        #left side weight
        for j in range(MAX_BAY_X//2):
            left += bay[i][j].weight

    return left


def get_weight_right(board):
    right = 0
    bay = board.bay

    for i in range(len(bay)):
        for j in range(board.MAX_BAY_X/2, board.MAX_BAY_X):
            right += bay[i][j].weight

    return right



def balance(board):
    bay = board.bay
    is_balanced = False
    moves = 0
    #also need to calculate cost in minutes

    #if only single container, done
    #if no containers, done
    count = np.count_nonzero(bay)
    if (count == 0):
        is_balanced = True
    elif (count == 1):
        is_balanced = True

    frontier = []
    heapq.heappush(frontier, ())



    #loop should work? it might be stuck in an infinite loop in certain cases tho. ex: looping moving a single container back n forth like case 5
    #use SIFT?
    #use tree to keep track of states?
    while not is_balanced:
        moves+=1
        left = get_weight_left(board)
        right = get_weight_right(board)
        diff = abs(left - right)
        #if its balanced
        #aslso need to account if all containers on one side, leading to div by 0
        if (diff/min(left, right) * 100 <= 10): 
            is_balanced = True
        
        #if not balanced
        else:
            #determine which side is bigger
            #find the container to move (container with 0 < weight <= diff)
            if (left > right):
                container = find_closest_weight(bay[:, :board.MAX_BAY_X/2], diff)
            else:
                container = find_closest_weight(bay[:, board.MAX_BAY_X/2:], diff)

            #a star to find a path

        
        #if changes r ineffective, use SIFT instead

    


    print("This balance will require " + moves + " moves, taking " + " minutes. Done! Don't forget to  ")


def find_closest_weight(bay, diff):
    container = bay[0][0]
    min_diff = abs(diff - container.weight)

    for row in bay:
        for curr in row:
            curr_diff = abs(diff - curr_diff)

            if (curr_diff < min_diff):
                min_diff = curr_diff
                container = curr

    return container

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



class Tree:
    def __init__(self):

        filepath = 'C:\\Users\\emily\\Documents\\GitHub\\BEAM-Solutions-Project\\load\\test_manifest2.txt'
        cont1 = manifest_read.A_Container(300, '6LBdogs500')
        cont2 = manifest_read.A_Container(634, 'Maersk')
        neededOff = [cont1, cont2]
        currentOff = []
        print("Tree initialized with root BoardState.")
        grid, _ = manifest_read.parse(filepath)
        self.root = BoardState(grid, neededOff, currentOff, 0, None) 

        print("Tree initialized with root BoardState.")

    def AStar(self):

        print("Starting A* search...")
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontierSet = {self.root}
        visitedSet = set()
        left = self.leftWeight(self.root)
        right = self.rightWeight(self.root)
        is_balanced = self.isGoal(left, right)
        side = self.heavySide(left, right)
        

        while not is_balanced:
            print(f"Frontier size: {len(frontier)}")
            _, curr = heapq.heappop(frontier)
            frontierSet.remove(curr)

            print(f"Exploring state with f={curr.f} (g={curr.g}, h={curr.h})")
            curr.PrintState()

            left = self.leftWeight(self.root)
            right = self.rightWeight(self.root)

            if self.isGoal(left, right):
                print("Goal state reached!")
                curr.PrintState()
                return
            
            visitedSet.add(curr)
            print("Expanding current state...")
            self.Expand(curr, frontier, frontierSet, visitedSet, side)

            is_balanced = self.isGoal(left, right)
            
            input("Press Enter to continue to the next step...")

    def Expand(self, curr, frontier, frontierSet, visitedSet, side):
        print("Expanding children...")

        if side == "left":
            for column in range(testx // 2):
                if column in curr.bay and curr.bay[column]:
                    top = curr.bay[column].pop()
                    row = len(curr.bay[column])
                    position = (column + 1, row + 1)
                    print(f"Popped container '{top.name}' from position {position}")

                    for otherColumn in range(testx // 2):
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

        elif side == "right":
            for column in range(testx // 2, testx):
                if column in curr.bay and curr.bay[column]:
                    top = curr.bay[column].pop()
                    row = len(curr.bay[column])
                    position = (column + 1, row + 1)
                    print(f"Popped container '{top.name}' from position {position}")

                    for otherColumn in range(testx // 2, testx):
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

                """ newBay = copy.deepcopy(curr.bay)
                newCurrOff = curr.currentOff[:]
                newCurrOff.append(top)
                newCost = abs(position[0]) + abs(position[1] - (testy + 1)) + 4

                child = BoardState(newBay, curr.neededOff, newCurrOff, curr.g + newCost, curr)
                print(f"Generated child state with container removed, f={child.f} (g={child.g}, h={child.h})")

                if child not in visitedSet and child not in frontierSet:
                    print("Adding child to frontier.")
                    heapq.heappush(frontier, (child.f, child))
                    frontierSet.add(child) """

    def isGoal(self, left_weight, right_weight):
        total_weight = left_weight + right_weight
        return abs(left_weight - right_weight) <= 0.1 * total_weight

    def leftWeight(self, curr):
        left_weight = 0
        for i in range(testx // 2):
            for container in curr.bay[i]:
                left_weight += container.weight
        
        return left_weight

    def rightWeight(self, curr):
        right_weight = 0
        for i in range(testx // 2, testx):
            for container in curr.bay[i]:
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