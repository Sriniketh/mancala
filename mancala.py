#!/usr/bin/python

import sys
from copy import deepcopy

file = open("traverse_log.txt", "w")
fileNextState = open("next_state.txt", "w")

class State:
    currentTask = 0
    currentPlayer = 0
    cutoffDepth = 0
    board = [0][0]
    mancala1 = 0
    mancala2 = 0
    #pit which brought about this state
    pit = 0
    returnValue = 0

    def getTask(self):
        return self.currentTask

    def getPlayer(self):
        return self.currentPlayer

    def getCutoffDepth(self):
        return self.cutoffDepth

    def getBoard(self):
        return self.board

    def getMancala1(self):
        return self.mancala1

    def getMancala2(self):
        return self.mancala2

    def getPit(self):
        return self.pit

    def getReturnValue(self):
        return self.returnValue

    def setPit(self, pit):
        self.pit = pit

    def setReturnValue(self, returnValue):
        self.returnValue = returnValue

    def setBoard(self, board):
        self.board = board

    def setMancala1(self, mancala1):
        self.mancala1 = mancala1

    def setMancala2(self, mancala2):
        self.mancala2 = mancala2

    def setCutoffDepth(self, cutoffDepth):
        self.cutoffDepth = cutoffDepth

    def __init__(self, currentTask, currentPlayer, cutoffDepth, board, mancala1, mancala2, pit, returnValue):
        self.currentTask = currentTask
        self.currentPlayer = currentPlayer
        self.cutoffDepth = cutoffDepth
        self.board = board
        self.mancala1 = mancala1
        self.mancala2 = mancala2
        self.pit = pit
        self.returnValue = returnValue

greedyStateObject = State(None, None, None, None, None, None, None, None)
minimaxStateObject = State(None, None, None, None, None, None, None, None)

def convert(returnValue):
    if returnValue == -30000:
        return "-Infinity"
    elif returnValue == 30000:
        return "Infinity"
    else:
        return str(returnValue)

def move(copyState, currentPit, currentPlayer):
    ##print "\t\tMOVE"
    board = copyState.getBoard()
    mancala1 = copyState.getMancala1()
    mancala2 = copyState.getMancala2()
    copyOfCurrentPit = currentPit

    ##print "\t\t",board
    ##print "\t\t",mancala2
    ##print "\t\t",mancala1
    ##print "\t\tPit ",currentPit
    ##print "\t\tPlayer ",currentPlayer

    i = 0
    j = 0
    boardLength = len(board[i])
    if currentPlayer == 1:
        i = 1
        j = 0
    elif currentPlayer == 2:
        i = 0
        j = 1
    coins = board[i][currentPit]
    board[i][currentPit] = 0
    while (coins > 0):
        ##print "\t\tcoins ",coins
        ##print "\t\tboard ",board
        ##print "\t\tmancala2 ",mancala2
        ##print "\t\tmancala1 ",mancala1
        if i == 1:
            #if currentPit is in mancala1
            if currentPit == boardLength:
                i = 0
            #if currentPit is on the last pit on the board
            elif currentPit == (boardLength - 1):
                currentPit += 1
                if currentPlayer == 1:
                    mancala1 += 1
                    coins -= 1
            else:
                currentPit += 1
                board[i][currentPit] += 1
                coins -= 1
        elif i == 0:
            #if currentPut is in mancala2
            if currentPit == -1:
                i = 1
            #if currentPit is on the last pit of the board
            elif currentPit == 0:
                currentPit -= 1
                if currentPlayer == 2:
                    mancala2 += 1
                    coins -= 1
            else:
                currentPit -= 1
                board[i][currentPit] += 1
                coins -= 1

    if (currentPit == boardLength) or (currentPit == -1):
        copyState.setBoard(board)
        copyState.setMancala1(mancala1)
        copyState.setMancala2(mancala2)
        copyState.setPit(copyOfCurrentPit)
        return (copyState, True)
    else:
        if currentPlayer == 1 and i == 1:
            if board[i][currentPit] == 1:
                mancala1 += board[j][currentPit] + 1
                board[j][currentPit] = 0
                board[i][currentPit] = 0
        elif currentPlayer == 2 and i == 0:
            if board[i][currentPit] == 1:
                mancala2 += board[j][currentPit] + 1
                board[j][currentPit] = 0
                board[i][currentPit] = 0
        copyState.setBoard(board)
        copyState.setMancala1(mancala1)
        copyState.setMancala2(mancala2)
        copyState.setPit(copyOfCurrentPit)
        return (copyState, False)

def max_value(initialState, currentPlayer, depth, againFlag, pitPosition, algorithm, alpha, beta):
    #print "MAX_VALUE"
    #print initialState.getBoard()
    global file
    returnState = None
    v = -30000
    initialState.setReturnValue(v)
    #depending on currentPlayer, choose board with i.
    i = 0
    j = 0
    nextPlayer = 0
    board = initialState.getBoard()
    mancala1 = initialState.getMancala1()
    mancala2 = initialState.getMancala2()
    player = ""
    player2 = ""
    if currentPlayer is 1:
        i = 1
        j = 0
        nextPlayer = 2
        player = "A"
        player2 = "B"
    elif currentPlayer is 2:
        i = 0
        j = 1
        nextPlayer = 1
        player = "B"
        player2 = "A"

    #terminal test
    #check for endgame i.e., one or both boards are zero
    emptyFlag = True
    for pos in range(len(board[1])):
        if board[1][pos] != 0:
            emptyFlag = False
    if emptyFlag:
        for pos in range(len(board[0])):
            mancala2 += board[0][pos]
            board[0][pos] = 0
    else:
        emptyFlag = True
        for pos in range(len(board[0])):
            if board[0][pos] != 0:
                emptyFlag = False
        if emptyFlag:
            for pos in range(len(board[1])):
                mancala1 += board[1][pos]
                board[1][pos] = 0
    #boards are zeroed
    ###print
    if emptyFlag and (depth != initialState.getCutoffDepth()):
        if againFlag:
            if (algorithm == 1) or (algorithm == 2):
                file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(30000) + "\n")
            elif algorithm == 3:
                file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(30000) + "," + convert(alpha) + "," + convert(beta) + "\n")
        else:
            if (algorithm == 1) or (algorithm == 2):
                if depth-1 is 0:
                    file.write("root," + str(depth) + "," + convert(-30000) + "\n")
                else:
                    file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(-30000) + "\n")
            elif algorithm == 3:
                if depth-1 is 0:
                    file.write("root," + str(depth) + "," + convert(-30000) + "," + convert(alpha) + "," + convert(beta) + "\n")
                else:
                    file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(-30000) + "," + convert(alpha) + "," + convert(beta) + "\n")

    if emptyFlag or (depth is initialState.getCutoffDepth() and againFlag is False):
        if initialState.getPlayer() is 1:
            return (mancala1 - mancala2),1,alpha,beta
        elif initialState.getPlayer() is 2:
            return (mancala2 - mancala1),1,alpha,beta

    #if the previous move resulted in another turn
    if againFlag:
        #print "AGAIN"
        v2 = 30000
        initialState.setReturnValue(v2)
        for currentPit in range(len(board[j])):
            if board[j][currentPit] != 0:
                #make copy of state
                copyState = deepcopy(initialState)
                copyState.setPit(currentPit)

                ##print
                if (algorithm == 1) or (algorithm == 2):
                    file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(copyState.getReturnValue()) + "\n")
                elif algorithm == 3:
                    file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(copyState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")

                ##print "Before move ",copyState.getBoard()

                ##print
                #print "Before"
                #print board
                #print "player ",currentPlayer
                #print "depth ", depth
                #print mancala2
                #print mancala1
                #print "alpha, beta", alpha, beta
                #print againFlag, "\n"

                #call move. move returns modified state and flag = true if there's another turn.
                resultState, resultFlag = move(copyState, currentPit, nextPlayer)
                ##print "After move ", resultState.getBoard()
                minimum,returnFlag,returnAlpha,returnBeta = max_value(resultState, currentPlayer, depth, resultFlag, currentPit+2, algorithm, alpha, beta)
                resultState.setReturnValue(minimum)

                ###print
                if (algorithm == 1) or (algorithm == 2):
                    file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "\n")
                elif algorithm == 3 and returnFlag is 1:
                    file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")
                elif algorithm == 3 and returnFlag is 2:
                    file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(returnAlpha) + "," + convert(returnBeta) + "\n")

                if minimum < v2:
                    v2 = minimum
                    returnState = resultState
                    initialState.setReturnValue(v2)
                if algorithm is 3:
                    if v2 <= alpha:
                        #print "pruned"
                        if returnFlag is 0:
                            file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")
                        return v2,2,alpha,beta
                    beta = min(beta, v2)
                    if returnFlag is 0:
                        file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")

                ##print
                #print "After"
                #print board
                #print "player ",currentPlayer
                #print "depth ", depth
                #print mancala2
                #print mancala1
                #print "alpha, beta", alpha, beta
                #print againFlag, "\n"

        return v2,2,alpha,beta

    #if its normal max_value
    depth += 1
    for currentPit in range(len(board[i])):
        if board[i][currentPit] != 0:
            #make copy of state
            copyState = deepcopy(initialState)
            copyState.setPit(currentPit)

            ###print
            if (algorithm == 1) or (algorithm == 2):
                if depth-1 is 0:
                    file.write("root," + str(depth-1) + "," + convert(copyState.getReturnValue()) + "\n")
                else:
                    file.write(player + str(pitPosition) + "," + str(depth-1) + "," + convert(copyState.getReturnValue()) + "\n")
            elif algorithm == 3:
                if depth-1 is 0:
                    file.write("root," + str(depth-1) + "," + convert(copyState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")
                else:
                    file.write(player + str(pitPosition) + "," + str(depth-1) + "," + convert(copyState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")

            ##print "Before move ",copyState.getBoard()

            ##print
            #print "Before"
            #print board
            #print "player ",currentPlayer
            #print "depth ", depth
            #print mancala2
            #print mancala1
            #print "alpha, beta", alpha, beta
            #print againFlag, "\n"

            #call move. move returns modified state and flag = true if there's another turn.
            resultState, resultFlag = move(copyState, currentPit, currentPlayer)
            ##print "After move ", resultState.getBoard()
            maximum,returnFlag,returnAlpha,returnBeta = min_value(resultState, nextPlayer, depth, resultFlag, currentPit+2, algorithm, alpha, beta)
            resultState.setReturnValue(maximum)

            ###print
            if (algorithm == 1) or (algorithm == 2):
                file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "\n")
            elif algorithm == 3 and returnFlag is 1:
                file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")
            elif algorithm == 3 and returnFlag is 2:
                file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(returnAlpha) + "," + convert(returnBeta) + "\n")

            #compare state to one with global state for max value (only if resultFlag is False)
            #print "RF", resultFlag
            #CHANGED changing if resultFlag is False and depth is 1: to if depth is 1:
            if depth is 1:
                global minimaxStateObject
                if minimaxStateObject.getTask() is None:
                    minimaxStateObject = resultState
                else:
                    if maximum > minimaxStateObject.getReturnValue():
                        minimaxStateObject = resultState
            if maximum > v:
                v = maximum
                returnState = resultState
                initialState.setReturnValue(v)
            if algorithm is 3:
                if v >= beta:
                    #print "pruned"
                    if returnFlag is 0:
                        file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")
                    return v,2,alpha,beta
                alpha = max(alpha, v)
                if returnFlag is 0:
                    file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")

            ##print
            #print "After"
            #print board
            #print "player ",currentPlayer
            #print "depth ", depth
            #print mancala2
            #print mancala1
            #print "alpha, beta", alpha, beta
            #print againFlag, "\n"

    return v,2,alpha,beta

def min_value(initialState, currentPlayer, depth, againFlag, pitPosition, algorithm, alpha, beta):
    #print "\tMIN_VALUE"
    #print "\t", initialState.getBoard()
    global file
    returnState = None
    returnState2 = None
    v = 30000
    initialState.setReturnValue(v)
    #depending on currentPlayer, choose board with i.
    i = 0
    j = 0
    nextPlayer = 0
    board = initialState.getBoard()
    mancala1 = initialState.getMancala1()
    mancala2 = initialState.getMancala2()
    if currentPlayer is 1:
        i = 1
        j = 0
        nextPlayer = 2
        player = "A"
        player2 = "B"
    elif currentPlayer is 2:
        i = 0
        j = 1
        nextPlayer = 1
        player = "B"
        player2 = "A"

    #terminal test
    #check for endgame i.e., one or both boards are zero
    emptyFlag = True
    for pos in range(len(board[1])):
        if board[1][pos] != 0:
            emptyFlag = False
    if emptyFlag:
        #print "board[1] is empty"
        for pos in range(len(board[0])):
            mancala2 += board[0][pos]
            board[0][pos] = 0
    else:
        emptyFlag = True
        for pos in range(len(board[0])):
            if board[0][pos] != 0:
                emptyFlag = False
        if emptyFlag:
            #print "board[0] is empty"
            for pos in range(len(board[1])):
                mancala1 += board[1][pos]
                board[1][pos] = 0
    #boards are zeroed
    ##print
    #CHANGED if emptyFlag and (depth != initialState.getCutoffDepth()) to if emptyFlag:
    if emptyFlag:
        if againFlag:
            if (algorithm == 1) or (algorithm == 2):
                file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(-30000) + "\n")
            elif algorithm == 3:
                file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(-30000) + "," + convert(alpha) + "," + convert(beta) + "\n")
        else:
            if (algorithm == 1) or (algorithm == 2):
                if depth is 0:
                    file.write("root," + str(depth) + "," + convert(-30000) + "\n")
                else:
                    file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(30000) + "\n")
            elif algorithm == 3:
                if depth is 0:
                    file.write("root," + str(depth) + "," + convert(-30000) + "," + convert(alpha) + "," + convert(beta) + "\n")
                else:
                    file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(30000) + "," + convert(alpha) + "," + convert(beta) + "\n")

    if emptyFlag or (depth is initialState.getCutoffDepth() and againFlag is False):
        #ALL LEAF NODES GET ##printED HERE
        initialState.setBoard(board)
        initialState.setMancala1(mancala1)
        initialState.setMancala2(mancala2)
        #refer to global State object
        global greedyStateObject
        if greedyStateObject.getTask() is None:
            greedyStateObject = initialState
        if initialState.getPlayer() is 1:
            if ((mancala1 - mancala2) > (greedyStateObject.getMancala1() - greedyStateObject.getMancala2())) and depth is 1:
                greedyStateObject = initialState
            return (mancala1 - mancala2),1,alpha,beta
        elif initialState.getPlayer() is 2:
            if ((mancala2 - mancala1) > (greedyStateObject.getMancala2() - greedyStateObject.getMancala1())) and depth is 1:
                greedyStateObject = initialState
            return (mancala2 - mancala1),1,alpha,beta

    #if the previous move resulted in another turn
    if againFlag:
        #print "\tAGAIN"
        v2 = -30000
        initialState.setReturnValue(v2)
        for currentPit in range(len(board[j])):
            if board[j][currentPit] != 0:
                #make copy of state
                copyState = deepcopy(initialState)
                copyState.setPit(currentPit)

                ####print
                if (algorithm == 1) or (algorithm == 2):
                    file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(copyState.getReturnValue()) + "\n")
                elif algorithm == 3:
                    file.write(player + str(pitPosition) + "," + str(depth) + "," + convert(copyState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")

                ##print "\tBefore move ",copyState.getBoard()

                ##print
                #print "\tBefore"
                #print "\t", board
                #print "\tplayer ",currentPlayer
                #print "\tdepth ", depth
                #print "\t", mancala2
                #print "\t", mancala1
                #print "\talpha, beta", alpha, beta
                #print "\t", againFlag, "\n"

                #call move. move returns modified state and flag = true if there's another turn.
                resultState, resultFlag = move(copyState, currentPit, nextPlayer)
                ##print "\tAfter move ",resultState.getBoard()
                maximum,returnFlag,returnAlpha,returnBeta = min_value(resultState, currentPlayer, depth, resultFlag, currentPit+2, algorithm, alpha, beta)
                resultState.setReturnValue(maximum)

                ###print
                if (algorithm == 1) or (algorithm == 2):
                    file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "\n")
                elif algorithm == 3 and returnFlag is 1:
                    file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")
                elif algorithm == 3 and returnFlag is 2:
                    file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(returnAlpha) + "," + convert(returnBeta) + "\n")

                #compare state to one with global state for max value (only if resultFlag is False)
                #CHANGED if resultFlag is False and depth is 1: to if depth is 1:
                if depth is 1:
                    global minimaxStateObject
                    if minimaxStateObject.getTask() is None:
                        minimaxStateObject = resultState
                    else:
                        if maximum > minimaxStateObject.getReturnValue():
                            minimaxStateObject = resultState
                if maximum > v2:
                    v2 = maximum
                    returnState2 = resultState
                    initialState.setReturnValue(v2)
                if algorithm is 3:
                    if v2 >= beta:
                        #print "pruned"
                        if returnFlag is 0:
                            file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")
                        return v2,2,alpha,beta
                    alpha = max(alpha, v2)
                    if returnFlag is 0:
                        file.write(player + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")

                ##print
                #print "\tAfter"
                #print "\t", board
                #print "\tplayer ",currentPlayer
                #print "\tdepth ", depth
                #print "\t", mancala2
                #print "\t", mancala1
                #print "\talpha, beta", alpha, beta
                #print "\t", againFlag, "\n"

        return v2,2,alpha,beta

    #if its normal min_value
    depth += 1
    for currentPit in range(len(board[i])):
        if board[i][currentPit] != 0:
            #make copy of state
            copyState = deepcopy(initialState)
            copyState.setPit(currentPit)

            ###print
            if (algorithm == 1) or (algorithm == 2):
                file.write(player + str(pitPosition) + "," + str(depth-1) + "," + convert(copyState.getReturnValue()) + "\n")
            elif algorithm == 3:
                file.write(player + str(pitPosition) + "," + str(depth-1) + "," + convert(copyState.getReturnValue()) +  "," + convert(alpha) + "," + convert(beta) + "\n")

            ##print "\tBefore move ",copyState.getBoard()

            ##print
            #print "\tBefore"
            #print "\t", board
            #print "\tplayer ",currentPlayer
            #print "\tdepth ", depth
            #print "\t", mancala2
            #print "\t", mancala1
            #print "\talpha, beta", alpha, beta
            #print "\t", againFlag, "\n"

            #call move. move returns modified state and flag = true if there's another turn.
            resultState, resultFlag = move(copyState, currentPit, currentPlayer)
            ##print "\tAfter move ",resultState.getBoard()
            minimum,returnFlag,returnAlpha,returnBeta = max_value(resultState, nextPlayer, depth, resultFlag, currentPit+2, algorithm, alpha, beta)
            resultState.setReturnValue(minimum)

            ###print
            if (algorithm == 1) or (algorithm == 2):
                file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "\n")
            elif algorithm == 3 and returnFlag is 1:
                 file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")
            elif algorithm == 3 and returnFlag is 2:
                 file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(returnAlpha) + "," + convert(returnBeta) + "\n")

            if minimum < v:
                v = minimum
                returnState = resultState
                initialState.setReturnValue(v)
            if algorithm is 3:
                if v <= alpha:
                    #print "pruned"
                    if returnFlag is 0:
                        file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")
                    return v,2,alpha,beta
                beta = min(beta, v)
                if returnFlag is 0:
                    file.write(player2 + str(currentPit+2) + "," + str(depth) + "," + convert(resultState.getReturnValue()) + "," + convert(alpha) + "," + convert(beta) + "\n")

            ##print
            #print "\tAfter"
            #print "\t", board
            #print "\tplayer ",currentPlayer
            #print "\tdepth ", depth
            #print "\t", mancala2
            #print "\t", mancala1
            #print "\talpha, beta", alpha, beta
            #print "\t", againFlag, "\n"

    return v,2,alpha,beta

def greedy(state):
    global greedyStateObject
    global file
    global fileNextState
    state.setCutoffDepth(1)
    result,returnFlag,returnAlpha,returnBeta = max_value(state, state.getPlayer(), 0, False, 0, 1, -30000, 30000)
    board = greedyStateObject.getBoard()
    fileNextState.write(str(board) + "\n")
    fileNextState.write(str(greedyStateObject.getMancala2()) + "\n")
    fileNextState.write(str(greedyStateObject.getMancala1()) + "\n")

def minimax(state):
    global file
    global fileNextState
    result,returnFlag,returnAlpha,returnBeta = max_value(state, state.getPlayer(), 0, False, 0, 2, -30000, 30000)
    file.write("root,0," + str(result) + "\n")
    board = minimaxStateObject.getBoard()
    fileNextState.write(str(board) + "\n")
    fileNextState.write(str(minimaxStateObject.getMancala2()) + "\n")
    fileNextState.write(str(minimaxStateObject.getMancala1()) + "\n")

def alphabeta(state):
    global file
    global fileNextState
    alpha = -30000
    beta = 30000
    result,returnFlag,returnAlpha,returnBeta = max_value(state, state.getPlayer(), 0, False, 0, 3, alpha, beta);
    board = minimaxStateObject.getBoard()
    file.write("root,0," + str(result) +  "," + convert(returnAlpha) + "," + convert(returnBeta) + "\n")
    fileNextState.write(str(board) + "\n")
    fileNextState.write(str(minimaxStateObject.getMancala2()) + "\n")
    fileNextState.write(str(minimaxStateObject.getMancala1()) + "\n")

def main():
    global file
    global fileNextState
    with open(sys.argv[2], "r") as f:
        input = f.readlines()
    input = [x.strip() for x in input]
    boardList = []
    boardList.append([int(n) for n in input[3].split()])
    boardList.append([int(n) for n in input[4].split()])
    state = State(int(input[0]), int(input[1]), int(input[2]), boardList, int(input[6]), int(input[5]), 0, -30000)

    if int(input[0]) is 1:
        file.write("Node,Depth,Value\n")
        greedy(state)
    elif int(input[0]) is 2:
        file.write("Node,Depth,Value\n")
        minimax(state)
    elif int(input[0]) is 3:
        file.write("Node,Depth,Value,Alpha,Beta\n")
        alphabeta(state)

    file.close()
    fileNextState.close()

if __name__ == "__main__":main() 
