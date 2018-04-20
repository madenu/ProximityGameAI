from proximity import Proximity
from agents import DeepQAgent
from board import LEARNER
from utils import Utils
import sys
batch_size = 128
EPISODES = 50000
LOAD = True

if __name__ == '__main__':
    args = sys.argv
    episodes = EPISODES
    load = LOAD
    if len(args) > 1:
        episodes = int(args[1])
        if len(args) > 2:
            load = False
    wins = 0.
    learner = DeepQAgent(LEARNER)
    if load:
        learner.load('weights.h5')
        learner.save('weightsbackup.h5')

    for e in range(episodes):
        reward = 0
        learner = learner.reset()
        game = Proximity(player1=learner)
        while True:
            _, val = game.nextUp()
            state = Utils.getState(game, learner, val)
            action = learner.act(game, state)
            game.makeMove()
            game.makeMove()
            # reward = game.score1 - game.score2
            if game.gameOver():
                if game.score1 > game.score2:
                    # reward = 500.
                    reward = 1.
                    wins += 1
                    print('WIN')
                elif game.score2 >  game.score1:
                    # reward = -500.
                    reward = -1.
                    print('LOSS')
                nextState = Utils.getState(game, learner, 0)
                learner.remember(state, action, reward, nextState, True)
                break
            nxt, val = game.nextUp()
            nextState = Utils.getState(game, learner, val)
            learner.remember(state, action, reward, nextState, False)

        if len(learner.memory) > batch_size:
            learner.replay(batch_size)
        print(game.board.text())
    learner.save('weights.h5')
    print('Winning Percentage : %d' % (wins / episodes))


