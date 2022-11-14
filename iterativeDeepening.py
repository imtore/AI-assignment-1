import pandas
import copy


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


class State:
    def __init__(self, _parent, _number, _direction):
        self.parent = _parent
        self.number = _number
        self.direction = _direction
        self.children = []
        self.recentActions = set()

    def inheritSnapshot(self):
        self.snapshot = copy.deepcopy(self.parent.getSnapshot())
        move = directions[self.direction]
        self.snapshot[self.number -
                      1][ROW] = self.snapshot[self.number-1][ROW] + move[ROW]
        self.snapshot[self.number -
                      1][COLUMN] = self.snapshot[self.number-1][COLUMN] + move[COLUMN]

    def setSnapshot(self, snapshot):
        self.snapshot = snapshot

    # def updateActions(self):
    #     self.recentActions = self.parent.recentActions
    #     self.recentActions.

    def generateChildren(self):
        x = 0
        # print(self.recentActions)
        for n in range(1, 9):
            # print("n: ", n)
            for d in index:
                # print("d: ", d)
                if(self.number == n and ((n, d+1) in self.recentActions or (n, d-1) in self.recentActions)):
                    continue

                child = State(self, n, d)

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

                child.inheritSnapshot()
                # set recent action function must be added
                if(listToTuple(child.getSnapshot()) in snapshotMap):
                    continue
                snapshotMap.add(listToTuple(child.getSnapshot()))
                child.recentActions = copy.deepcopy(self.recentActions)
                child.recentActions.add((n, d))
                self.children.append(child)
                x += 1

            # print()
        return x

    def getChildren(self):  # ok
        return self.children

    def getSnapshot(self):  # ok
        return self.snapshot

    def hasConflict(self):  # ok
        for i in range(0, 8):
            for j in range(0, 8):
                if(i != j and self.snapshot[i][ROW] == self.snapshot[j][ROW]):
                    return True
                elif(i != j and self.snapshot[i][COLUMN] == self.snapshot[j][COLUMN]):
                    return True
                elif(i != j and abs(self.snapshot[i][COLUMN]-self.snapshot[j][COLUMN]) == abs(self.snapshot[i][ROW]-self.snapshot[j][ROW])):
                    return True
        return False

    def removeChildrenAndActions(self):
        self.children = []
        self.recentActions = set()


class EightQueen:
    def __init__(self, firstSnapshot):
        self.start = State(DUMMY, 0, DUMMY)
        self.start.setSnapshot(firstSnapshot)

    def searchToDepth(self, startState, depth):
        if(depth == 0):
            if(startState.hasConflict()):
                return False, startState
            else:
                return True, startState

        if(startState.getChildren() == []):
            startState.generateChildren()

        expansion = startState.getChildren()
        for child in expansion:
            found, state = self.searchToDepth(child, depth-1)
            if(found):
                return found, state

        return False, startState

    def iterativeDeepening(self, depth):
        if not self.start.hasConflict():
            return self.start

        for i in range(depth):
            found, state = self.searchToDepth(self.start, i)
            if(found):
                return state


def listToTuple(snapshot):
    listOfTuples = []
    for coo in snapshot:
        listOfTuples.append((coo[ROW], coo[COLUMN]))
    return tuple(listOfTuples)


snapshot = [[1, 2],
            [2, 4],
            [3, 6],
            [4, 8],
            [4, 4],
            [6, 2],
            [7, 5],
            [8, 5]]

board = EightQueen(snapshot)
try:
    print(board.iterativeDeepening(6))
except KeyboardInterrupt:
    print("j")
    # print(board.getn())
