import numpy as np

np.random.seed(123)  # for reproducibility

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Input, Concatenate, concatenate
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam

# INPUT KEYS
INPUT_KEYS = ['boardInput', 'remainingMovesInput', 'scoreInput', 'moveValueInput']

# INPUT CONSTANTS
BOARD_DEPTH, BOARD_ROWS, BOARD_COLUMNS = 3, 8, 10
NUMBER_OF_PLAYERS, NUMBER_OF_DISTINCT_MOVES = 2, 20

# CONVOLUTION PARAMETERS
FIRST_CONV_FILTERS, SECOND_CONV_FILTERS, THIRD_CONV_FILTERS = 6, 6, 12
FIRST_CONV_KERNEL, SECOND_CONV_KERNEL, THIRD_CONV_KERNEL = (1, 1), (2, 2), (4, 4)
FIRST_CONV_STRIDES, SECOND_CONV_STRIDES, THIRD_CONV_STRIDES = (1, 1), (1, 1), (2, 2)
FIRST_CONV_PADDING, SECOND_CONV_PADDING, THIRD_CONV_PADDING = 'same', 'same', 'same'

# ACTIVATIONS
FIRST_CONV_ACTIVATION, SECOND_CONV_ACTIVATION, THIRD_CONV_ACTIVATION = 'relu', 'relu', 'relu'
FIRST_REMAINING_MOVES_ACTIVATION, SECOND_REMAINING_MOVES_ACTIVATION = 'relu', 'relu'
SCORE_LAYER_ACTIVATION = 'relu'
STATE_SUMMARY_LAYER_ACTIVATION = 'relu'
PENULTIMATE_LAYER_ACTIVATION = 'relu'
OUTPUT_LAYER_ACTIVATION = 'linear'

# UNITS
FIRST_REMAINING_MOVES_UNITS, SECOND_REMAINING_MOVES_UNITS = 20, 20
SCORE_LAYER_UNITS = 1
STATE_SUMMARY_LAYER_UNITS = 120
MOVE_VALUE_UNITS = 40
PENULTIMATE_LAYER_UNITS = 160
OUTPUT_UNITS = 80

# MODEL PARAMS
LOSS = 'mse'



def model():

    ###### Input Placeholders
    ################################################################################################
    boardInput = Input(shape=(BOARD_ROWS, BOARD_COLUMNS, BOARD_DEPTH), name='boardInput')
    

    remainingMovesInput = Input(shape=(NUMBER_OF_PLAYERS, NUMBER_OF_DISTINCT_MOVES),
                                name='remainingMovesInput')
                                
    
    scoreInput = Input((1, NUMBER_OF_PLAYERS + 1), name='scoreInput')

    
    moveValueInput = Input((1, 1), name="moveValueInput")
    


    ###### Building the Convolutional Layers
    ################################################################################################
    firstBoardLayer = Conv2D(filters=FIRST_CONV_FILTERS, kernel_size=FIRST_CONV_KERNEL,
                             strides=FIRST_CONV_STRIDES, padding=FIRST_CONV_PADDING,
                             activation=FIRST_CONV_ACTIVATION, name='firstBoardLayer')(boardInput)
                             
    firstBoardLayer = Dropout(.05)(firstBoardLayer)

    secondBoardLayer = Conv2D(filters=SECOND_CONV_FILTERS, kernel_size=SECOND_CONV_KERNEL,
                              strides=SECOND_CONV_STRIDES, padding=SECOND_CONV_PADDING,
                              activation=SECOND_CONV_ACTIVATION,
                              name='secondBoardLayer')(firstBoardLayer)
                              
    secondBoardLayer = Dropout(.05)(secondBoardLayer)

    thirdBoardLayer = Conv2D(filters=THIRD_CONV_FILTERS, kernel_size=THIRD_CONV_KERNEL,
                              strides=THIRD_CONV_STRIDES, padding=THIRD_CONV_PADDING,
                              activation=THIRD_CONV_ACTIVATION,
                              name='thirdBoardLayer')(secondBoardLayer)
    thirdBoardLayer = Dropout(.05)(thirdBoardLayer)
    flatThirdBoardLayer = Flatten(name='flatThirdBoardLayer')(thirdBoardLayer)

    ###### Building the Moves Layers
    ################################################################################################
    firstRemainingMovesLayer = Dense(FIRST_REMAINING_MOVES_UNITS,
                                     activation=FIRST_REMAINING_MOVES_ACTIVATION,
                                     name='firstRemainingMovesLayer')(remainingMovesInput)

    firstRemainingMovesLayer = Dropout(.5)(firstRemainingMovesLayer)
    secondRemainingMovesLayer = Dense(SECOND_REMAINING_MOVES_UNITS,
                                      activation=SECOND_REMAINING_MOVES_ACTIVATION,
                                      name='secondRemainingMovesLayer')(firstRemainingMovesLayer)
    secondRemainingMovesLayer = Dropout(.5)(secondRemainingMovesLayer)
    flatSecondRemainingMovesLayer = Flatten(name='flatSecondRemainingMovesLayer')(secondRemainingMovesLayer)


    moveValueLayer = Dense(MOVE_VALUE_UNITS, name="moveValueLayer")(moveValueInput)
    
    moveValueLayer = Dropout(.5)(moveValueLayer)

    flatMoveValueLayer = Flatten(name="flatMoveValueLayer")(moveValueLayer)

    ###### Building the Score Layers
    ################################################################################################

    scoreLayer = Dense(SCORE_LAYER_UNITS, activation=SCORE_LAYER_ACTIVATION, name='scoreLayer')(
        scoreInput)
        
    scoreLayer = Dropout(.5)(scoreLayer)

    flatScoreLayer = Flatten(name='flatScoreLayer')(scoreLayer)

    ###### Combining the State Factors
    ################################################################################################
    stateLayer = Concatenate(name='stateLayer')([flatThirdBoardLayer, flatSecondRemainingMovesLayer,
                                                 flatScoreLayer, flatMoveValueLayer])

    stateSummaryLayer = Dense(STATE_SUMMARY_LAYER_UNITS, activation=STATE_SUMMARY_LAYER_ACTIVATION,
                              name='stateSummaryLayer')(stateLayer)
    stateSummaryLayer = Dropout(.5)(stateSummaryLayer)


    ###### One Last Layer
    ################################################################################################
    penultimateLayer = Dense(PENULTIMATE_LAYER_UNITS, activation=PENULTIMATE_LAYER_ACTIVATION,
                             name="penultimateLayer")(stateSummaryLayer)
                             
    penultimateLayer = Dropout(.5)(penultimateLayer)

    ###### Defining the Model Output
    ################################################################################################
    ouputLayer = Dense(OUTPUT_UNITS, activation=OUTPUT_LAYER_ACTIVATION,
                       name='output')(penultimateLayer)

    ###### Building and Compiling the Network
    ################################################################################################
    model = Model(inputs=[boardInput, remainingMovesInput, scoreInput, moveValueInput], outputs=ouputLayer)

    model.compile(optimizer=Adam(), loss=LOSS)


    return model


# # Uncomment to Test
# network = model(.1)
# network.summary()
# fakeBoard = np.random.random((1, BOARD_ROWS, BOARD_COLUMNS, BOARD_DEPTH))
# fakeMoves = np.random.random((1, NUMBER_OF_PLAYERS, NUMBER_OF_DISTINCT_MOVES))
# fakeScores = np.random.random((1, 1, NUMBER_OF_PLAYERS + 1))
# fakeMoveValue = np.ones((1,1,1)) * 20.
# fakeTarget = np.ones((1, OUTPUT_UNITS)) * 7
# 
# network.fit(x=dict(zip(
#     ['boardInput', 'remainingMovesInput', 'scoreInput',
#      'moveValueInput'],
#     [fakeBoard, fakeMoves, fakeScores, fakeMoveValue])), y=fakeTarget)
# 
# y = network.predict(x=dict(zip(
#     ['boardInput', 'remainingMovesInput', 'scoreInput',
#      'moveValueInput'],
#     [fakeBoard, fakeMoves, fakeScores, fakeMoveValue])), batch_size=1)
# print(y[0][[x in range(3) for x in range(80)]])
# network.save_weights('w.hdf5')

