import pandas
import time
import copy
import queue

# directions:
UP = 0
DOWN = 1

LEFT = 3
RIGHT = 4

UPRIGHT = 6
DOWNLEFT = 7

UPLEFT = 9
DOWNRIGHT = 10


DUMMY = -8

index = [0, 1, 3, 4, 6, 7, 9, 10]

directions = {0: (-1, 0), 1: (1, 0), 3: (0, -1), 4: (0, 1),
              6: (-1, 1), 7: (1, -1), 9: (-1, -1), 10: (1, 1)}

snapshotMap = set()

ROW = 0
COLUMN = 1


def cmp(a, b):
    a < b


class State:
    def __init__(self, _parent, _number, _direction, _height):
        self.parent = _parent
        self.number = _number
        self.direction = _direction
        self.children = []
        self.recentActions = set()
        self.height = _height
        self.inheritSnapshot()
        self.priority = _height + self.getLocalConflict()

    def __lt__(self, other):
        return self.priority < other.priority

    def inheritSnapshot(self):
        if(self.parent == None):
            return None
        self.snapshot = copy.deepcopy(self.parent.getSnapshot())
        move = directions[self.direction]
        self.snapshot[self.number -
                      1][ROW] = self.snapshot[self.number-1][ROW] + move[ROW]
        self.snapshot[self.number -
                      1][COLUMN] = self.snapshot[self.number-1][COLUMN] + move[COLUMN]

    def setSnapshot(self, snapshot):
        self.snapshot = snapshot

    def generateChildren(self, h):
        for n in range(1, 9):
            for d in index:

                if(self.number == n and ((n, d+1) in self.recentActions or (n, d-1) in self.recentActions)):
                    continue

                child = State(self, n, d, h)

                if(self.snapshot[n-1] == [1, 1]):
                    if(d != RIGHT and d != DOWN and d != DOWNRIGHT):
                        continue
                if(self.snapshot[n-1] == [1, 8]):
                    if(d != LEFT and d != DOWN and d != DOWNLEFT):
                        continue
                if(self.snapshot[n-1] == [8, 1]):
                    if(d != RIGHT and d != UP and d != UPRIGHT):
                        continue
                if(self.snapshot[n-1] == [8, 8]):
                    if(d != LEFT and d != UP and d != UPLEFT):
                        continue
                if(self.snapshot[n-1][ROW] == 1 and (d == UP or d == UPLEFT or d == UPRIGHT)):
                    continue
                if(self.snapshot[n-1][ROW] == 8 and (d == DOWN or d == DOWNRIGHT or d == DOWNLEFT)):
                    continue
                if(self.snapshot[n-1][COLUMN] == 1 and (d == LEFT or d == UPLEFT or d == DOWNLEFT)):
                    continue
                if(self.snapshot[n-1][COLUMN] == 8 and (d == RIGHT or d == UPRIGHT or d == DOWNRIGHT)):
                    continue

                if(listToTuple(child.getSnapshot()) in snapshotMap):
                    continue
                snapshotMap.add(listToTuple(child.getSnapshot()))

                child.recentActions = copy.deepcopy(self.recentActions)
                child.recentActions.add((n, d))
                self.children.append(child)

    def getLocalConflict(self):
        if(self.parent == None):
            return 0
        s = self.number-1
        num = 0
        for j in range(0, 8):
            if(s != j):
                if(self.snapshot[s][ROW] == self.snapshot[j][ROW]):
                    num += 1
                elif(self.snapshot[s][COLUMN] == self.snapshot[j][COLUMN]):
                    num += 1
                elif(abs(self.snapshot[s][COLUMN]-self.snapshot[j][COLUMN]) == abs(self.snapshot[s][ROW]-self.snapshot[j][ROW])):
                    num += 1
        return num

    def getChildren(self):
        return self.children

    def getSnapshot(self):
        return self.snapshot

    def hasConflict(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if(i != j and self.snapshot[i][ROW] == self.snapshot[j][ROW]):
                    return True
                elif(i != j and self.snapshot[i][COLUMN] == self.snapshot[j][COLUMN]):
                    return True
                elif(i != j and abs(self.snapshot[i][COLUMN]-self.snapshot[j][COLUMN]) == abs(self.snapshot[i][ROW]-self.snapshot[j][ROW])):
                    return True
        return False


class EightQueen:
    def __init__(self, firstSnapshot):
        self.start = State(None, 0, DUMMY, 0)
        self.start.setSnapshot(firstSnapshot)
        self.start.generateChildren(1)

    def aStar(self):
        if not self.start.hasConflict():
            return self.start

        expansion = queue.PriorityQueue()
        goals = queue.PriorityQueue()
        list(map(expansion.put, self.start.getChildren()))

        while not expansion.empty():
            node = expansion.get()

            if(node.hasConflict() == False):
                if(goals.empty()):
                    goals.put(node)
                else:
                    g = goals.get()
                    if(g.priority < node.priority):
                        return g
                    else:
                        goals.put(node)

            node.generateChildren(node.height+1)

            list(map(expansion.put, node.getChildren()))
        return None


def listToTuple(snapshot):
    listOfTuples = []
    for coo in snapshot:
        listOfTuples.append((coo[ROW], coo[COLUMN]))
    return tuple(listOfTuples)


snapshot = [[1, 2], [2, 4], [3, 6], [4, 7], [5, 3], [6, 2], [7, 7], [8, 4]]

print(snapshot)

board = EightQueen(snapshot)
try:
    print(board.aStar().getSnapshot())

except KeyboardInterrupt:
    print("interrupt! exiting...")

# f(n) = h(n) + g(n)
