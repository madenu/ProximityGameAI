from board import Board
import agents
from random import shuffle as shuffle
from board import UNCLAIMED, LEARNER, OPPONENT, HEIGHT, WIDTH, DEPTH
from time import sleep
from colorama import Fore
from colorama import Style
import numpy as np
class Proximity(object):

    def __init__(self, height=8, width=10, player1=agents.UserAgent(LEARNER), player2=agents.GreedyAgent(OPPONENT), firstMove = 0):

        self.board = Board(height, width)
        self.player1 = player1
        self.player2 = player2
        self.turns1 = [x for x in range(1, 21)] * 2
        self.turns2 = [y for y in range(1, 21)] * 2
        self.remainingMoves1 = np.ones(20, dtype=np.int) * 2
        self.remainingMoves2 = np.ones(20, dtype=np.int) * 2
        shuffle(self.turns1)
        shuffle(self.turns2)
        self.playerToAct = firstMove
        self.score1 = 0
        self.score2 = 0


    def nextUp(self):
        if self.gameOver():
            return 0, 0
        if self.playerToAct == 0:
            return self.player1.ID, self.turns1[0]
        return self.player2.ID, self.turns2[0]

    def gameOver(self):
        return self.board.gameOver()

    def makeMove(self):
        if self.playerToAct == 0:
            value = self.turns1.pop(0)
            self.board.move(self.player1, self.player1.getMove(self, value), value)
            self.remainingMoves1[value - 1] -= 1
        else:
            value = self.turns2.pop(0)
            self.board.move(self.player2, self.player2.getMove(self, value), value)
            self.remainingMoves2[value - 1] -= 1
        self.updateScore()
        self.playerToAct = (self.playerToAct + 1) % 2

    def updateScore(self):
        self.score1 = self.board.getScore(self.player1)
        self.score2 = self.board.getScore(self.player2)




if __name__ == '__main__':

    x = Proximity(8,10,agents.UserAgent(LEARNER))

    while not x.gameOver():
        nxt, val = x.nextUp()
        print(f"{Fore.RED}Your Score : %d,{Style.RESET_ALL}" % (x.score1), end="")
        print(f"{Fore.BLUE} Their Score : %d{Style.RESET_ALL}" % (x.score2))
        print(x.board.text())
        print("Next Move : " + ("You" if nxt == LEARNER else "Computer"))
        print("Next Move Value : " + str(val))
        if nxt == OPPONENT:
            sleep(3)
        x.makeMove()

    if x.score1 < x.score2:
        print(f"{Fore.BLUE} YOU LOST, YOU SUCK{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED} YOU WON, FUCK THE COMPUTER{Style.RESET_ALL}")
    print(x.board.text())
    print(f"{Fore.LIGHTYELLOW_EX}Thanks for playing :D{Style.RESET_ALL}")


