import numpy as np
from qnetwork import INPUT_KEYS
from copy import deepcopy

class Utils:

    @staticmethod
    def getState(game, player,  value):
        stateValues = []
        boardInput = np.empty((1, 8, 10, 3))
        boardInput[0, :, :, :] = deepcopy(game.board.grid)
        stateValues.append(boardInput)
        stateValues.append(Utils.remainingMovesSummary(game, player))
        stateValues.append(Utils.scoreSummary(game, player))
        stateValues.append(np.ones((1, 1, 1)) * deepcopy(value))
        return stateValues

    @staticmethod
    def asModelInput(stateValues):
        return dict(zip(INPUT_KEYS, stateValues))

    @staticmethod
    def scoreSummary(game, player):
        rootingForScore = deepcopy(game.score1) if player is game.player1 else deepcopy(game.score2)
        rootingAgainstScore = deepcopy(game.score2) if player is game.player1 else deepcopy(game.score1)
        diff = rootingForScore - rootingAgainstScore
        summary = np.empty((1, 1, 3))
        summary[0, 0, 0] = rootingForScore
        summary[0, 0, 1] = rootingAgainstScore
        summary[0, 0, 2] = diff
        return summary

    @staticmethod
    def remainingMovesSummary(game, player):
        rootingForRemainingMoves = (deepcopy(game.remainingMoves1) if player is game.player1
                                    else deepcopy(game.remainingMoves2))
        rootingAgainstRemainingMoves = (deepcopy(game.remainingMoves2) if player is game.player1
                                    else deepcopy(game.remainingMoves1))
        summary = np.empty((1, 2, 20))
        summary[0, 0, :] = rootingForRemainingMoves
        summary[0, 1, :] = rootingAgainstRemainingMoves
        return summary


