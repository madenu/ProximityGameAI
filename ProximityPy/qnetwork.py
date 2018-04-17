import numpy as np

np.random.seed(123)  # for reproducibility

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Input, Concatenate, concatenate
from keras.layers import Conv2D, MaxPooling2D

# INPUT CONSTANTS
BOARD_ROWS, BOARD_COLUMNS, BOARD_DEPTH = 8, 10, 3
NUMBER_OF_PLAYERS, NUMBER_OF_DISTINCT_MOVES = 2, 20

# CONVOLUTION PARAMETERS
FIRST_CONV_FILTERS, SECOND_CONV_FILTERS = 6, 6
FIRST_CONV_KERNEL, SECOND_CONV_KERNEL = (3, 3), (3, 3)
FIRST_CONV_STRIDES, SECOND_CONV_STRIDES = (1, 1), (2, 2)
FIRST_CONV_PADDING, SECOND_CONV_PADDING = 'same', 'same'

# ACTIVATIONS
FIRST_CONV_ACTIVATION, SECOND_CONV_ACTIVATION = 'relu', 'relu'
FIRST_REMAINING_MOVES_ACTIVATION, SECOND_REMAINING_MOVES_ACTIVATION = 'relu', 'relu'
SCORE_LAYER_ACTIVATION = 'relu'
ACTION_ROW_LAYER_ACTIVATION, ACTION_COLUMN_LAYER_ACTIVATION = 'relu', 'relu'
STATE_SUMMARY_LAYER_ACTIVATION = 'linear'
OUTPUT_LAYER_ACTIVATION = 'linear'

# UNITS
FIRST_REMAINING_MOVES_UNITS, SECOND_REMAINING_MOVES_UNITS = 20, 20
SCORE_LAYER_UNITS = 1
ACTION_ROW_LAYER_UNITS, ACTION_COLUMN_LAYER_UNITS = 8, 10
STATE_SUMMARY_LAYER_UNITS = 10

# MODEL PARAMS
LOSS = 'mse'
OPTIMIZER = 'Adam'


def model():

    ###### Input Placeholders
    ################################################################################################
    boardInput = Input(shape=(BOARD_ROWS, BOARD_COLUMNS, BOARD_DEPTH), name='boardInput')

    remainingMovesInput = Input(shape=(NUMBER_OF_PLAYERS, NUMBER_OF_DISTINCT_MOVES),
                                name='remainingMovesInput')

    scoreInput = Input((1, NUMBER_OF_PLAYERS), name='scoreInput')

    actionRowInput = Input((1, BOARD_ROWS), name="actionRowInput")

    actionColumnInput = Input((1, BOARD_COLUMNS), name="actionColumnInput")

    ###### Building the Convolutional Layers
    ################################################################################################
    firstBoardLayer = Conv2D(filters=FIRST_CONV_FILTERS, kernel_size=FIRST_CONV_KERNEL,
                             strides=FIRST_CONV_STRIDES, padding=FIRST_CONV_PADDING,
                             activation=FIRST_CONV_ACTIVATION, name='firstBoardLayer')(boardInput)

    secondBoardLayer = Conv2D(filters=SECOND_CONV_FILTERS, kernel_size=SECOND_CONV_KERNEL,
                              strides=SECOND_CONV_STRIDES, padding=SECOND_CONV_PADDING,
                              activation=SECOND_CONV_ACTIVATION,
                              name='secondBoardLayer')(firstBoardLayer)

    flatSecondBoardLayer = Flatten(name='flatSecondBoardLayer')(secondBoardLayer)

    ###### Building the Moves Layers
    ################################################################################################
    firstRemainingMovesLayer = Dense(FIRST_REMAINING_MOVES_UNITS,
                                     activation=FIRST_REMAINING_MOVES_ACTIVATION,
                                     name='firstRemainingMovesLayer')(remainingMovesInput)

    secondRemainingMovesLayer = Dense(SECOND_REMAINING_MOVES_UNITS,
                                      activation=SECOND_REMAINING_MOVES_ACTIVATION,
                                      name='secondRemainingMovesLayer')(firstRemainingMovesLayer)

    flatSecondRemainingMovesLayer = Flatten(name='flatSecondRemainingMovesLayer')(
        secondRemainingMovesLayer)

    ###### Building the Score Layers
    ################################################################################################

    scoreLayer = Dense(SCORE_LAYER_UNITS, activation=SCORE_LAYER_ACTIVATION, name='scoreLayer')(
        scoreInput)

    flatScoreLayer = Flatten(name='flatScoreLayer')(scoreLayer)

    ###### Building the Action Layers
    ################################################################################################
    actionRowLayer = Dense(ACTION_ROW_LAYER_UNITS, activation=ACTION_ROW_LAYER_ACTIVATION,
                           name='actionRowLayer')(actionRowInput)

    actionColumnLayer = Dense(ACTION_COLUMN_LAYER_UNITS, activation=ACTION_COLUMN_LAYER_ACTIVATION,
                              name='actionColumnLayer')(actionColumnInput)

    flatActionRowLayer = Flatten(name='flatActionRowLayer')(actionRowLayer)

    flatActionColumnLayer = Flatten(name='flatActionColumnLayer')(actionColumnLayer)

    ###### Combining the State Factors
    ################################################################################################
    stateLayer = Concatenate(name='stateLayer')([flatSecondBoardLayer,
                                                 flatSecondRemainingMovesLayer, flatScoreLayer])

    stateSummaryLayer = Dense(STATE_SUMMARY_LAYER_UNITS, activation='linear',
                              name='stateSummaryLayer')(stateLayer)

    ###### Combining the States With Actions
    ################################################################################################
    mergedLayer = Concatenate(name='mergedLayer')(
        [flatActionRowLayer, flatActionColumnLayer, stateSummaryLayer])

    ###### Defining the Model Output
    ################################################################################################
    ouputLayer = Dense(1, activation=OUTPUT_LAYER_ACTIVATION, name='output')(mergedLayer)

    ###### Building and Compiling the Network
    ################################################################################################
    model = Model(inputs=[boardInput, remainingMovesInput, scoreInput, actionRowInput,
                          actionColumnInput], outputs=ouputLayer)

    model.compile(optimizer=OPTIMIZER, loss=LOSS)


    return model


# Uncomment to Test
network = model()
network.summary()
fakeBoard = np.random.random((1, BOARD_ROWS, BOARD_COLUMNS, BOARD_DEPTH))
fakeMoves = np.random.random((1, NUMBER_OF_PLAYERS, NUMBER_OF_DISTINCT_MOVES))
fakeScores = np.random.random((1, 1, NUMBER_OF_PLAYERS))
fakeActionRows = np.random.random((1, 1, 8))
fakeActionCols = np.random.random((1, 1, 10))
fakeTarget = np.ones(1) * 7

network.fit(x=dict(zip(
    ['boardInput', 'remainingMovesInput', 'scoreInput', 'actionRowInput', 'actionColumnInput'],
    [fakeBoard, fakeMoves, fakeScores, fakeActionRows, fakeActionCols])), y=fakeTarget)
