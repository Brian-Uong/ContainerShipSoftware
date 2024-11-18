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
        for row in range(self.testx - 1, -1, -1):
            for column in range(self.testy):
                container = self.bay[row][column]
                if container:
                    print(f"| {container.name} {container.weight} ({container.x},{container.y}) |", end='')
                else:
                    print("| EMPTY |", end='')
            print('\n')



# class Tree:
#     def __init__(self, root):
#         self.root = root
    
#     def AStar(self):
#         frontier = []
#         heapq.heappush(frontier, (self.root.f, self.root))
#         frontierSet = {self.root}
#         visitedSet = set()

#         while frontier:
#             _, curr = heapq.heappop(frontier)
#             frontierSet.remove(curr)

#             if self.isGoal(curr):
#                 print('GOAL')

#                 return
            
#             visitedSet.add(curr)

def main():
    # bay = []

    # for i in range(5):
    #     row = []
    #     for j in range(4):
    #         container = manifest_read.Container(j + 1, i + 1, i * 5, 'bob')
    #         row.append(container)
    #     bay.append(row)

    test = BoardState(manifest_read.parse())

    test.PrintState()

if __name__ == "__main__":
    main()
