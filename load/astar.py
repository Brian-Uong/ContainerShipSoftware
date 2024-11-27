import heapq
import manifest_read

MAX_BAY_Y = 10
SAIL_BAY_Y = 8
MAX_BAY_X = 12
MAX_BUFFER_Y = 4
MAX_BUFFER_X = 24
MAX_BUFFER_CONTAINERS = 96
testx = 5
testy = 4
testbayx = 7
textbayy = 2

class BoardState:
    def __init__(self, bay, g, parent, currentOff):
        # self.neededOff = neededOff
        self.currentOff = currentOff
        # self.neededOn = neededOn
        # self.currentOn = currentOn
        self.bay = bay
        # self.buffer = buffer
        self.g = g
        self.h = self.heuristic()
        self.parent = parent
        self.f = self.g + self.h

    def heuristic():
        return 0

    # def __init__(self, bay):
    #     self.bay = bay

    def PrintState(self):
        name_width = 14
        weight_width = 6
        position_width = 6

        for row in range(testy - 1, -1, -1):
            for column in range(testx):
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

            self.expand(curr, frontier, frontierSet, visitedSet)

    def Expand(self, curr, frontier, frontierSet, visitedSet):
        for column in range(curr.testx):
            if column in self.bay and self.bay[column]:
                top = self.bay[column][-1]

                for otherColumn in range(curr.testx):
                    if otherColumn == column:
                        continue

                    newBay = {key: list(value) for key, value in curr.bay.item }

                    for col in range(curr.testx):
                        if col not in newBay:
                            newBay[col] = []

                    oldY = top.y
                    oldX = top.x
                    top.y = len(newBay[otherColumn]) + 1
                    top.x = otherColumn + 1
                    newBay[otherColumn].append(top)
                    newCost = abs(oldX - top.x) + abs(oldY - top.y)

                    child = BoardState(newBay, newCost, curr, curr.currentOff)

                    if child not in visitedSet and child not in frontierSet:
                        heapq.heappush(frontier, (child.f, child))
                        frontierSet.add(child)

                newBay = {key: list(value) for key, value in curr.bay.item }
                oldY = top.y
                oldX = top.x
                top.y = 'off'
                top.x = 'off'
                newCost = abs(oldX) + abs(oldY - curr.testy + 1) + 4 + 2
                curr.currentOff.append(top)
                child = BoardState(newBay, newCost, curr, curr.currentOff)
                if child not in visitedSet and child not in frontierSet:
                        heapq.heappush(frontier, (child.f, child))
                        frontierSet.add(child)
                

    # def isGoal():
        



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
