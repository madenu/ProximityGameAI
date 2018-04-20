from abc import ABC
from qnetwork import model
import numpy as np
from collections import deque
import random
from utils import Utils
from copy import deepcopy
class PlayerAgent(ABC):


    def __init__(self, ID):
        self.ID = ID
        self.opponent = 2
        if ID == 2:
            self.opponent = 1

    def getMove(self, game, value):
        pass


class GreedyAgent(PlayerAgent):

    def getMove(self, game, value):

        return max(game.board.available, key=lambda x : game.board.evalMove(self, x, value))


class UserAgent(PlayerAgent):

    def getMove(self, game, value):
        x, y = 0, 0
        while not game.board.isAvailable(x-1,y-1):
            x = int(input("Enter Row : "))
            y = int(input("Enter Column : "))
        return (x-1) * game.board.width + (y-1) % game.board.width


class DeepQAgent(PlayerAgent):
    #https://github.com/keon/deep-q-learning/blob/master/dqn.py

    def __init__(self, ID, deck=deque(maxlen=2000), mod=None):
        super(DeepQAgent, self).__init__(ID)
        self.memory = deck
        self.gamma = 0.99  # discount rate
        self.epsilon = 1.  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        if mod is None:
            self.model = model()
        else:
            self.model = mod
        self.nextMove = -1

    def reset(self):
        new = DeepQAgent(ID=self.ID, deck=deepcopy(self.memory), mod=self.model)
        return new

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, game, state):
        legalMoves = game.board.available
        if np.random.rand() <= self.epsilon:
            self.nextMove = random.choice(legalMoves)
        else:
            act_values = self.model.predict(state)
            self.nextMove = np.argmax(act_values[0, tuple(legalMoves)])  # returns action
        return self.nextMove

    def toMove(self, n):
        return n // 8, n % 10

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(Utils.asModelInput(next_state))))
            target_f = self.model.predict(Utils.asModelInput(state))
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=1)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def getMove(self, game, value):

        return self.nextMove









