from proximity import Proximity
from agents import DeepQAgent
from board import LEARNER
from utils import Utils
import sys
from collections import deque
batch_size = 2000
EPISODES = 5000
LOAD = True

if __name__ == '__main__':
    dekk = deque(maxlen=2000)
    args = sys.argv
    episodes = EPISODES
    load = LOAD
    if len(args) > 1:
        episodes = int(args[1])
        if len(args) > 2:
            load = False
    wins = 0.
    newlearner = DeepQAgent(LEARNER)
    # if load:
    #     learner.load('weightssss.h5')
    for e in range(episodes):
        reward = 0
        learner = newlearner
        game = Proximity(player1=learner)
        done = False
        step = 1.
        while True:
            _, val = game.nextUp()
            state = Utils.getState(game, learner, val)
            action = learner.act(game, state)
            game.makeMove()
            game.makeMove()
            if game.gameOver():
                done = True
                if game.score1 > game.score2:
                    reward = 5
                    wins += 1
                    print('WIN')
                elif game.score2 >  game.score1:
                    reward = -5
                    print('LOSS')
                nextState = Utils.getState(game, learner, 0)
                learner.remember(state, action, reward, nextState, done)
                break
            nxt, val = game.nextUp()
            nextState = Utils.getState(game, learner, val)
            learner.remember(state, action, reward, nextState, done)
        if len(learner.memory) > batch_size:
            learner.replay(batch_size)
        print(game.board.text())
        newlearner = learner.reset()
    newlearner.save('weightssss.h5')
    print('Winning Percentage : %d' % (wins / episodes))


