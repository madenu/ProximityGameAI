from abc import ABC

class PlayerAgent(ABC):


    def __init__(self, ID):
        self.ID = ID

    def getMove(self, board, value):
        pass


class GreedyAgent(PlayerAgent):

    def getMove(self, board, value):

        return max(board.available, key=lambda x : board.evalMove(self.ID, *x, value))


class UserAgent(PlayerAgent):

    def getMove(self, board, value):
        x, y = 0, 0
        while not board.isAvailable(x-1,y-1):
            x = int(input("Enter Row : "))
            y = int(input("Enter Column : "))
        return x-1, y-1

