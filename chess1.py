# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 17:30:54 2019

@author: Tim
"""

import chess
import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense, Flatten
from keras.layers import Conv2D

pieceValue = {'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
              'p':-1, 'n':-2, 'b':-3, 'r':-4, 'q':-5, 'k':-6}

letters = {'a': 0, 'b': 1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h': 7}

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
def makeBetter(s):
    result = ''
    for char in s:
        if isInt(char):
            result += char * int(char)
        else:
            result += char
    return result

def getMatrix(board):
    m = np.zeros((8, 8), int)
    s = board.epd()
    s = s.split(' ')[0]
    s = s.split('/')
    for i in range(len(s)):
        s[i] = makeBetter(s[i])
    
    for i in range(len(s)):
        string = s[i]
        for j in range(len(string)):
            if not isInt(string[j]):
                m[i][j] = pieceValue[string[j]]
    return m

def getMoves(board):
    moves = board.legal_moves
    matrices = []
    boards = []
    moovs = []
    for move in moves:
        board.push(move)
        matrices.append(getMatrix(board))
        boards.append(board.copy())
        moovs.append(move)
        board.pop()
    return moovs

def matrixToBoard(m):
    board = chess.Board()
    board.clear()
    #TODO
    
#Players
def random(board):
    moves = getMoves(board)
    return moves[np.random.randint(len(moves))]

def human(board):
    move = input("Move (e9 k0): ")
    start, end = move.split(' ')
    start = letters[start[0]] + (int(start[1])-1)*8
    end = letters[end[0]] + (int(end[1])-1)*8
    move = chess.Move(start, end)
    while move not in board.legal_moves:
        print("That move was ILLEGAL! Try again.")
        move = input("Move (e9 k0): ")
        start, end = move.split(' ')
        start = letters[start[0]] + (int(start[1])-1)*8
        end = letters[end[0]] + (int(end[1])-1)*8
        move = chess.Move(start, end)
        
    return move

#TODO convnet
#TODO rollouts
    
model = Sequential()
model.add(Conv2D(32, (3,3), input_shape=(8,8, 1)))
model.add(Conv2D(32, (3,3)))
model.add(Conv2D(32, (3,3)))
model.add(Flatten())
model.add(Dense(20))
model.add(Dense(3, activation='softmax'))
model.compile('adam', 'mse')
    
def AI(board, model=model, p2=False):
    moves = getMoves(board)
    bestVal = 0
    bestMove = None
    for move in moves:
        board.push(move)
        m = getMatrix(board)
        m = m.reshape((1,8,8,1))
        probs = model.predict(m)[0]
        win = probs[int(p2)] 
        tie = probs[2]
        val = win + 0.5 * tie
        if val > bestVal:
            bestVal = val
            bestMove = move
        board.pop()
    return bestMove
        
    
#ALRIGHT, policy is too difficult for a game like chess, Imma only do the value part. 

def MCTS():
    return 0
    
    
def play(p1, p2, verbose = True):
    board = chess.Board()
    p1Turn = True
    if verbose: print(board)
    if p1==AI: history = []
    while not board.is_game_over():
        if p1Turn:
            move = p1(board)
        else:
            move = p2(board)
            
        board.push(move)
        #TODO check
        p1Turn = not p1Turn
        if verbose: print(board)
        if verbose: print("\n\n\n")
        if p1==AI:
            history.append(getMatrix(board).reshape(1,8,8,1))
            
    """
    if p1==AI:    
        global model
        if board.result() == '1-0':
            result = [1,0,0]
        elif board.result()=='0-1':
            result = [0,1,0]
        else:
            result = [0,0,1]
        result = np.array(result).reshape((1,3))
        for board in history:
            model.fit(board, result)
    """
    return board.result()


    
    
results = []
for i in range(100):
    result = play(AI, random, verbose=False)
    print("Game #"+str(i)+":", end="")
    if result == '1-0':
        print("White Wins!")
    elif result == '0-1':
        print("Black Wins")
    else:
        print("Tie!")
    results.append(result)
    if not len(results) % 10:
        print('White:', results.count('1-0')/len(results), 
              ' Black:', results.count('0-1')/len(results), 
              'Ties:', results.count('1/2-1/2')/len(results))
        


    
    