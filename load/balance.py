from astar import Container, BoardState
import numpy as np

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
    #also nneed to calculate cost in minutes

    #if only single container, done
    #if no containers, done
    count = np.count_nonzero(bay)
    if (count == 0):
        is_balanced = True
    elif (count == 1):
        is_balanced = True


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