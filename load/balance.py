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
        for j in range(board.MAX_BAY_X/2):
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
        cont1 = manifest_read.A_Container(3000, '6LBdogs500')
        cont2 = manifest_read.A_Container(634, 'Maersk')
        neededOff = [cont1, cont2]
        currentOff = []
        print("Tree initialized with root BoardState.")
        self.root = BoardState(manifest_read.parse(filepath), neededOff, currentOff, 0, None)

        print("Tree initialized with root BoardState.")

    def AStar(self):

        print("Starting A* search...")
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontierSet = {self.root}
        visitedSet = set()

        while frontier:
            _, curr = heapq.heappop(frontier)
            frontierSet.remove(curr)

            if self.isGoal(curr):
                print("Goal state reached!")
                curr.PrintState()
                return curr

            visitedSet.add(curr)
            self.Expand(curr, frontier, frontierSet, visitedSet)

        # If balancing fails, perform SIFT operation
        print("Unable to balance the ship. Performing SIFT operation.")
        #SIFT WIP


    def Expand(self, curr, frontier, frontierSet, visitedSet):

        for column in range(self.ship.cols):
            if column in curr.bay and curr.bay[column]:
                top = curr.bay[column].pop()  # Remove the top container
                row = len(curr.bay[column]) + 1
                position = (column + 1, row)

                # Move the container to other columns
                for otherColumn in range(self.ship.cols):
                    if otherColumn == column:
                        continue

                    newBay = copy.deepcopy(curr.bay)
                    newRow = len(newBay[otherColumn]) + 1
                    newBay[otherColumn].append(top)

                    moveCost = abs(position[0] - (otherColumn + 1)) + abs(position[1] - newRow)
                    child = BoardState(newBay, curr.neededOff, curr.currentOff, curr.g + moveCost, curr)

                    if child not in visitedSet and child not in frontierSet:
                        heapq.heappush(frontier, (child.f, child))
                        frontierSet.add(child)

                # Move the container to the buffer
                newBay = copy.deepcopy(curr.bay)
                newCurrOff = curr.currentOff[:]
                newCurrOff.append(top)
                bufferCost = abs(position[0]) + abs(position[1] - (self.ship.rows + 1)) + 4

                child = BoardState(newBay, curr.neededOff, newCurrOff, curr.g + bufferCost, curr)

                if child not in visitedSet and child not in frontierSet:
                    heapq.heappush(frontier, (child.f, child))
                    frontierSet.add(child)

    def isGoal(self, curr):

        left_weight = sum(
            container.weight
            for column, stack in enumerate(curr.bay[: self.ship.cols // 2])
            for container in stack
        )
        right_weight = sum(
            container.weight
            for column, stack in enumerate(curr.bay[self.ship.cols // 2 :])
            for container in stack
        )
        total_weight = left_weight + right_weight
        return abs(left_weight - right_weight) <= 0.1 * total_weight



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