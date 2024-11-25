import heapq


class Container:
    def __init__(self, name, x, y, weight):
        self.name = name
        self.x = x
        self.y = y
        self.weight = weight


class BoardState:
    MAX_BAY_Y = 10  # maximum rows in the bay
    SAIL_BAY_Y = 8  # rows designated for sailing containers
    MAX_BAY_X = 12  # maximum columns in the bay
    MAX_BUFFER_Y = 4  # maximum rows in the buffer area
    MAX_BUFFER_X = 24  # maximum columns in the buffer area
    MAX_BUFFER_CONTAINERS = 96  # total buffer capacity
    testx = 5  # current bay column count
    testy = 4  # current bay row count

    def __init__(self, bay, g=0, parent=None):
        self.bay = bay  # a dictionary representing the container stacks in the bay
        self.g = g  # cost to reach this state
        self.h = self.heuristic()  # heuristic cost to goal
        self.parent = parent  # pointer to parent state
        self.f = self.g + self.h  # total cost (f = g + h)

    def heuristic(self):
        # a simple heuristic could be the number of containers still needed to be moved.
        return sum(len(stack) for stack in self.bay.values())

    def print_state(self):
        # prints the current state of the bay, displaying all containers in their positions.
        name_width = 14
        weight_width = 6
        position_width = 6

        for row in range(self.testy - 1, -1, -1):
            for column in range(self.testx):
                if column in self.bay and row < len(self.bay[column]):
                    container = self.bay[column][row]
                    name = f"{container.name}".ljust(name_width)
                    weight = f"{container.weight}".ljust(weight_width)
                    position = f"({container.x},{container.y})".ljust(position_width)
                    print(f"| {name} {weight} {position} |", end="")
                else:
                    empty_name = "unused".ljust(name_width)
                    empty_weight = "0".ljust(weight_width)
                    position = f"({column + 1},{row + 1})".ljust(position_width)
                    print(f"| {empty_name} {empty_weight} {position} |", end="")
            print()

    def offload(self, needed_off):
        # offload containers from the bay.
        # :param needed_off: list of container ids to be offloaded.
        moves = []  # track moves for debugging or simulation
        for container_id in needed_off:
            # find the container's position
            position = None
            for col, stack in self.bay.items():
                for row, container in enumerate(stack):
                    if container.name == container_id:
                        position = (col, row)
                        break
                if position:
                    break

            if not position:
                print(f"container {container_id} not found in the bay.")
                continue

            col, row = position

            # temporarily move blocking containers
            while len(self.bay[col]) > row + 1:
                blocking_container = self.bay[col].pop()
                buffer_pos = self.find_buffer_position()
                if buffer_pos:
                    buffer_col, buffer_row = buffer_pos
                    self.bay[buffer_col].append(blocking_container)
                    moves.append(f"moved {blocking_container.name} to buffer ({buffer_col}, {buffer_row}).")
                else:
                    print("no buffer space available!")
                    return moves  # stop offloading if buffer is full

            # remove the target container
            self.bay[col].pop()
            moves.append(f"offloaded container {container_id} from ({col}, {row}).")

        return moves

    def load(self, containers_to_load):
        # load new containers into the bay.
        # :param containers_to_load: list of container objects to load.
        moves = []  # track moves for debugging or simulation
        for container in containers_to_load:
            position = self.find_available_slot()

            if position:
                col, row = position
                container.x, container.y = col + 1, row + 1  # update container position
                self.bay[col].append(container)
                moves.append(f"loaded {container.name} at ({col}, {row}).")
            else:
                print("no available slot in the bay!")
                return moves  # stop loading if the bay is full

        return moves

    def find_buffer_position(self):
        # find an available position in the buffer space.
        for col in range(self.testx, self.testx + self.MAX_BUFFER_X):  # check buffer columns
            if col not in self.bay:
                self.bay[col] = []
            if len(self.bay[col]) < self.MAX_BUFFER_Y:
                return (col, len(self.bay[col]))
        return None  # no buffer space available

    def find_available_slot(self):
        # find an available position in the bay.
        for col in range(self.testx):  # check bay columns
            if col not in self.bay:
                self.bay[col] = []
            if len(self.bay[col]) < self.testy:
                return (col, len(self.bay[col]))
        return None  # no available slot

    def expand(self):
        # generate possible moves from the current state.
        new_states = []
        # example logic to offload a container
        for col in self.bay:
            if self.bay[col]:  # if there are containers in this column
                container = self.bay[col][-1]  # get the top container
                needed_off = [container.name]  # assume we want to offload this container
                new_bay = {k: v[:] for k, v in self.bay.items()}  # copy current bay state
                new_bay[col].pop()  # offload the container
                new_state = BoardState(new_bay, self.g + 1, self)  # create new state
                new_states.append(new_state)
        return new_states


class Tree:
    def __init__(self, root):
        self.root = root

    def a_star(self):
        # perform a* search to find the optimal sequence of moves.
        frontier = []
        heapq.heappush(frontier, (self.root.f, self.root))
        frontier_set = {self.root}
        visited_set = set()

        while frontier:
            _, curr = heapq.heappop(frontier)
            frontier_set.remove(curr)

            if self.is_goal(curr):
                print("goal state reached!")
                return curr

            visited_set.add(curr)
            for next_state in curr.expand():
                if next_state not in visited_set and next_state not in frontier_set:
                    heapq.heappush(frontier, (next_state.f, next_state))
                    frontier_set.add(next_state)

        print("no solution found!")
        return None

    def is_goal(self, state):
        # define the goal state. for this example, we can check if the bay is empty.
        return all(len(stack) == 0 for stack in state.bay.values())


def main():
    # example initialization of the bay
    bay = {
        0: [Container("C1", 1, 1, 5), Container("C2", 1, 2, 3)],
        1: [Container("C3", 2, 1, 7)],
        2: [],
        3: [],
        4: [],
    }

    # initialize BoardState and Tree
    root = BoardState(bay)
    tree = Tree(root)

    print("initial state:")
    root.print_state()

    # perform a* search
    result = tree.a_star()

    if result:
        print("final state:")
        result.print_state()


if __name__ == "__main__":
    main()