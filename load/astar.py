import heapq
import manifest_read

class BoardState:
    MAX_BAY_Y = 10
    SAIL_BAY_Y = 8
    MAX_BAY_X = 12
    MAX_BUFFER_Y = 4
    MAX_BUFFER_X = 24
    MAX_BUFFER_CONTAINERS = 96
    testx = 5
    testy = 4
    
    # def __init__(self, neededOff, currentOff, neededOn, currentOn, bay, buffer, g, parent):
    #     self.neededOff = neededOff
    #     self.currentOff = currentOff
    #     self.neededOn = neededOn
    #     self.currentOn = currentOn
    #     self.bay = bay
    #     self.buffer = buffer
    #     self.g = g
    #     self.h = self.heuristic()
    #     self.parent = parent
    #     self.f = self.g + self.h

    def __init__(self, bay):
        self.bay = bay

    def PrintState(self):
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
                    print(f"| {name} {weight} {position} |", end='')
                else:
                    empty_name = "UNUSED".ljust(name_width)
                    empty_weight = "0".ljust(weight_width)
                    position = f"({column + 1},{row + 1})".ljust(position_width)
                    print(f"| {empty_name} {empty_weight} {position} |", end='')
            print()



    # def Expand(self):
    #     for column in range(self.testx):
    #         if column in self.bay and self.bay[column]:
            


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

def main():
    # bay = []

    # for i in range(5):
    #     row = []
    #     for j in range(4):
    #         container = manifest_read.Container(j + 1, i + 1, i * 5, 'bob')
    #         row.append(container)
    #     bay.append(row)

    neededOff = []

    test = BoardState(manifest_read.parse())

    test.PrintState()

if __name__ == "__main__":
    main()
