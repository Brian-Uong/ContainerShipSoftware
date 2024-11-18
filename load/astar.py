import heapq

class Container:
    def __init__(self, x, y, weight, name):
        self.x = x
        self.y = y
        self.weight = weight
        self.name = name

class BoardState:
    MAX_BAY_Y = 10
    SAIL_BAY_Y = 8
    MAX_BAY_X = 12
    MAX_BUFFER_Y = 4
    MAX_BUFFER_X = 24
    MAX_BUFFER_CONTAINERS = 96
    
    def __init__(self, neededOff, currentOff, neededOn, currentOn, bay, buffer, g, parent):
        self.neededOff = neededOff
        self.currentOff = currentOff
        self.neededOn = neededOn
        self.currentOn = currentOn
        self.bay = bay
        self.buffer = buffer
        self.g = g
        self.h = self.heuristic()
        self.parent = parent
        self.f = self.g + self.h

class Tree:
    def __init__(self, root):
        self.root = root
    
    def AStar(self):
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontierSet = {self.root}
        visitedSet = set()

        while frontier:
            _, curr = heapq.heappop(frontier)
            frontierSet.remove(curr)

            if self.isGoal(curr):
                print('GOAL')

                return
            
            visitedSet.add(curr)

            
