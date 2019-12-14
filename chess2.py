import gym
import chess
import random
import numpy as np

#TODO test onehot and 
"""
Ideas for models:
    one layer chooses piece, that layer (altered from prob dist to certain) is fed into which one decides move
    one layer chooses piece, then that output is fed back into the model, it's run again, then the same layer's 2nd output is where to move the piece to
    4 numbers for position
    2 numbers for position (probably easiest to start with)

"""
pieceValue = {'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
              'p':-1, 'n':-2, 'b':-3, 'r':-4, 'q':-5, 'k':-6,
              '.':0}

numbers = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e':4, 'f': 5, 'g': 6, 'h': 7}
letters = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4:'e', 5: 'f', 6: 'g', 7: 'h'}

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
def oneHotBoard(b):
    OHboard = np.zeros((8,8,13))
    board = str(b).split('\n')
    
    for i in range(len(board)):
        line = board[i].split(' ')
        for j in range(len(line)):
            val = pieceValue[line[j]]
            if val < 0:
                val = -val + 6
            #print(i,j, val)
            OHboard[i][j][val] = 1
    return OHboard

def matrixBoard(b):
    mboard = np.zeros((8,8))
    board = str(b).split('\n')
    
    for i in range(len(board)):
        line = board[i].split(' ')
        for j in range(len(line)):
            val = pieceValue[line[j]]
            mboard[i][j] = val
    return mboard

def numbersToMove(b, start, end):
    #fucking off by ones...
    start = list(start)
    end = list(end)
    start[0] += 1
    start[1] += 1
    end[0] += 1
    end[1] += 1
    
    string = letters[start[0]] + str(start[1]) + letters[end[0]] + str(end[1])
    
    return chess.Move.from_uci(string)

def randomAgent(b):
    moves = list(b.legal_moves)
    return random.choice(moves)



def game(b, p1, p2):
    turn = 0
    
    while not (b.is_checkmate() or b.can_claim_draw()):
        turn += 1
        if b.turn:
            move = p1(b)
        else:
            move = p2(b)
        b.push(move)
        
        print("\nTurn", turn)
        print(b)
        
#b.turn = "is it white's turn?
        
class ChessEnv(gym.Env):
    pass
        


if __name__ == '__main__':
    b = chess.Board()
    ob = oneHotBoard(b)
    game(b, randomAgent, randomAgent)

    