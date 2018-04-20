from itertools import product as cartesianProduct

import numpy as np
from colorama import Fore
from colorama import Style

UNCLAIMED = 0
LEARNER = 1
OPPONENT = 2
HEIGHT = 8
WIDTH = 10
DEPTH = 3

class Board(object):

    @staticmethod
    def otherPlayer(player):
        return LEARNER if player == OPPONENT else OPPONENT

    @staticmethod
    def _tileTemplate(x, y):
        return "(%d, %d)" % (x, y)


    def __init__(self, height=HEIGHT, width=WIDTH):

        self.height = height
        self.width = width
        self.available = [x for x in range(80)]
        self.grid = np.ndarray((height, width, DEPTH))
        self.neighbors = {}
        self._init_grids_()
        self._init_neighbors_()

    def _init_grids_(self):

        # UNCLAIMED LAYER, 1 if unclaimed, 0 otherwise
        self.grid[:, :, UNCLAIMED] = np.ones((self.height, self.width))

        # LEARNER, OPPONENT LAYERS, -1 if tile is unowned, otherwise value of tile
        self.grid[:, :, LEARNER] = -np.ones((self.height, self.width))
        self.grid[:, :, OPPONENT] = -np.ones((self.height, self.width))

    def _init_neighbors_(self):

        for move in self.available:
            x = move // self.width
            y = move % self.width
            self._setupNeighbors(x, y)

    # bcable
    def _setupNeighbors(self, row, col):

        neighbors = []
        # if these are valid rows or columns
        nextCol = (col + 1) < self.width
        prevCol = (col - 1) >= 0
        nextRow = (row + 1) < self.height
        prevRow = (row - 1) >= 0

        if prevRow:
            neighbors.append((row - 1, col))

        if nextRow:
            neighbors.append((row + 1, col))

        if prevCol:
            neighbors.append((row, col - 1))

        if nextCol:
            neighbors.append((row, col + 1))

        if row % 2 == 1:
            if nextCol:
                if prevRow:
                    neighbors.append((row - 1, col + 1))
                if nextRow:
                    neighbors.append((row + 1, col + 1))
        else:
            if prevCol:
                if prevRow:
                    neighbors.append((row - 1, col - 1))
                if nextRow:
                    neighbors.append((row + 1, col - 1))

        self.neighbors.update({Board._tileTemplate(row, col): neighbors})

    def owner(self, x, y):

        if self.grid[x, y, UNCLAIMED] == 1:
            return UNCLAIMED
        elif self.grid[x, y, OPPONENT] > 0:
            return OPPONENT
        else:
            return LEARNER

    def getFreeMoves(self):
        return self.available

    def isAvailable(self, x, y):
        return (x * self.width + y) in self.available

    def move(self, player, move, value):

        row = move // self.width
        col = move % self.width

        if not self.isAvailable(row, col):
            return False
        else:
            self.available.remove(move)
            self.grid[row, col, UNCLAIMED] = -1
            self.grid[row, col, player.ID] = value
            self.captureNeighbors(player, row, col, value)
            return True

    # bcable
    def captureNeighbors(self, player, row, col, value):

        tileID = self._tileTemplate(row, col)
        # numCaptured = 0
        otherPlayer = player.opponent

        for x, y in self.neighbors[tileID]:

            if not self.isAvailable(x, y):

                if self.owner(x, y) == otherPlayer:

                    otherVal = self.grid[x, y, otherPlayer]

                    if value > otherVal:
                        self.grid[x, y, player.ID] = otherVal
                        self.grid[x, y, otherPlayer] = -1
                        # numCaptured += 1

                else:
                    self.grid[x, y, player.ID] += 1

                    # return numCaptured

    def evalMove(self, player, move, value):
        row = move // self.width
        col = move % self.width

        sumPoints = value

        tileID = self._tileTemplate(row, col)
        numCaptured = 0
        otherPlayer = player.opponent

        for x, y in self.neighbors[tileID]:

            if not self.isAvailable(x, y):

                if self.owner(x, y) == otherPlayer:

                    otherVal = self.grid[x, y, otherPlayer]

                    if value > otherVal:
                        sumPoints += otherVal
                        numCaptured += 1

                else:
                    sumPoints += 1

        return sumPoints

    def gameOver(self):
        return len(self.available) == 0

    def getScore(self, player):
        b = self.grid[:, :, player.ID] > 0
        x = np.sum(self.grid[:, :, player.ID][b])
        return x

    #bacable
    def text(self):
        header = "     "
        topRow = "   --"

        for i in range(self.width):
            header += "  " + str(i+1) + "  ."
            topRow += "------"
        topRow += "----\n"

        out = header + "\n" + topRow

        for row in range(0, self.height):
            rowText = ""

            # add a character for rows <10 so it will right align
            if (row + 1) < 10:
                rowText += " "

            rowText += str(row + 1) + " | "

            # shift text over for even numbered rows for hex effect
            if row % 2 == 1:
                rowText += "   "

            # draw each tile in the row, including its team and strength
            for col in range(0, self.width):

                if self.owner(row, col) == LEARNER:
                    val = self.grid[row, col, LEARNER]
                    rowText += f"{Fore.RED}<%3d>{Style.RESET_ALL} " % (val)
                elif self.owner(row, col) == OPPONENT:
                    val = self.grid[row, col, OPPONENT]
                    rowText += f"{Fore.BLUE}<%3d>{Style.RESET_ALL} " % (val)
                else:
                    rowText += f"{Fore.LIGHTYELLOW_EX}<___>{Style.RESET_ALL} "

            if row % 2 == 0:
                rowText += "   "

            out += rowText + "|\n"

        out += topRow

        return out

