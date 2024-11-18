class container:
    def __init__(self, x, y, weight, name):
        self.x = x
        self.y = y
        self.weight = weight
        self.name = name

class BoardState:
    MAX_BAY_Y = 10
    SAIL_BAY_Y = 8
    MAX_BAY_X = 12
    BAX_BUFFER_Y = 4
    BAX_BUFFER_X = 24
    BAX_BUFFER_CONTAINERS = 96

    def __init__(self, needed_off, current_off, needed_on, current_on, bay, buffer, g, parent):
        self.needed_off = needed_off # array of container objects
        self.current_off = current_off
        self.needed_on = needed_on
        self.current_on = current_on
        self.bay = bay # 2D array of container objects
        self.buffer = buffer # 2D array of container objects
        self.moves = [] # list of (from, to) pairs
        self.g = g # cost to reach this current state
        self.h = self.heuristic() # estimated cost to the goal
        self.parent = parent 

        def heuristic(self):
            # placeholder for the heuristic alg/calc
            return 0

        def get_g(self):
            return self.g

        def get_h(self):
            return self.h
        
        def get_f(self):
            return self.g + self.h
        
        def get_board_state(self):
            # implement logic to return the current state as needed
            pass

class Tree:
    def __init__(self, root):
        self.root = root
    
    def compare_boards(node1, node2):
        # logic to compare the two board states
        pass
    
    def a_star(self):
        import heapq

        frontier = [] # priority queue for BoardState objects
        frontier_set = set() # set for quick membership checking
        visited_set = set() # set for visited BoardState objects

    heapq.heappush(frontier, (self.root.get_f(), self.root))

    frontier_set.add(self.root)

    while frontier:
        _, curr = heapq.heappop(frontier)
        frontier_set.remove(curr)

        if self.is_goal(curr):
            for move in curr.moves:
                print(f"{move[0]} to {move[1]}")
            return
            
            visited_set.add(curr)

            # expands the current state
            for expansion in self.expand(curr):
                if expansion not in visited_set and expansion not in frontier_set:
                    heapq.heappush(frontier, (expansion.get_f(), expansion))
                    frontier_set.add(expansion)
    
    def is_goal(self, state):
        # placeholder for goal check
        return False
    
    def expand(self, state):
        # placeholder for expanding a Boardstate
        return []