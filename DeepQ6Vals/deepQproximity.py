from proximity import Proximity
from agents import DeepQAgent
from board import LEARNER
from utils import Utils
import sys
batch_size = 128
EXPERIMENTS = 50
EPISODES = 50000
LOAD = True
FLAGS = ['-exps', '-eps', '-load']
DEFAULT_PARAMS = [EXPERIMENTS, EPISODES, LOAD]
validTrues = ['True', '-True', 'true', '-true', 't', '-t', 'T', '-T']
validFalses = ['False', '-False', 'false', '-false', 'f', '-f', 'F', '-F']


if __name__ == '__main__':
    args = sys.argv
    params = dict(zip(FLAGS, DEFAULT_PARAMS))
    for i in range(1, len(args), 2):

        flag = args[i]
        update = args[i+1]

        if flag in FLAGS:
            if flag != '-load':
                update = int(update)
            elif update in validTrues:
                update = True
            elif update in validFalses:
                update = False
            else:
                print("Invalid truth value")
                sys.exit(1)

            params.update({flag : update})
        else:
            print("Invalid flag")
            sys.exit(1)

    experiments = params['-exps']
    episodes = params['-eps']
    load = params['-load']
    firstIter = True
    wins = 0
    for experiment in range(experiments):
        learner = DeepQAgent(LEARNER)
        if load or not firstIter:
            learner.load('weights6game.h5')
            learner.save('backupweights6game.h5')
            if firstIter:
                firstIter = False

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
                    elif game.score2 >  game.score1:
                        # reward = -500.
                        reward = -1.
                    nextState = Utils.getState(game, learner, 0)
                    learner.remember(state, action, reward, nextState, True)
                    break
                nxt, val = game.nextUp()
                nextState = Utils.getState(game, learner, val)
                learner.remember(state, action, reward, nextState, False)
            if e % 100 == 0:
                print('Experiment #' +str(experiment) + '\tEpisode #' + str(e))
                if len(learner.memory) > batch_size:
                    learner.replay(batch_size, verb = 1)
                print(game.board.text())
            else:
                if len(learner.memory) > batch_size:
                    learner.replay(batch_size)

        learner.save('weights6game.h5')
    print('Winning Percentage : %d' % (wins / episodes))


