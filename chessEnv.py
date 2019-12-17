import chess
import random
import numpy as np

import gym
import gym.spaces.box as box


pieceValue = {'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
              'p':-1, 'n':-2, 'b':-3, 'r':-4, 'q':-5, 'k':-6,
              '.':0}

numbers = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e':4, 'f': 5, 'g': 6, 'h': 7}
letters = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4:'e', 5: 'f', 6: 'g', 7: 'h'}
        
#rewarded for any legal move
#makes a random move if the input isn't legal
class ChessEnv_v0(gym.Env):
    reward_range = (-1.0, 1.0) #does this matter?
    
    action_space = box.Box(0, 1, shape=(2, 64))
    observation_space = box.Box(0, 1, shape=(8, 8, 12))
    
    def reset(self):
        self.board = chess.Board()
        self.oh_board = oneHotBoard(self.board)
        return self.oh_board 
    
    def step(self, action):
        move = numbersToMove(action[0], action[1])
        legal = move in self.board.legal_moves
        if legal:
            self.board.push(move)
        else:
            move = randomAgent(self.board)
            self.board.push(move)
        self.oh_board = oneHotBoard(self.board)
        
        obs = self.oh_board
        rew = int(legal)
        done = self.board.is_checkmate() or self.board.can_claim_draw()
        info = None        
        
        return obs, rew, done, info
    
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

def numbersToMove(start, end):
    #fucking off by ones...
    start = list(start)
    end = list(end)
    #start[0] += 1 #I don't think this is nec because it's converted to letters
    start[1] += 1
    #end[0] += 1
    end[1] += 1
    
    string = letters[start[0]] + str(start[1]) + letters[end[0]] + str(end[1])
    return chess.Move.from_uci(string)


def randomAgent(b):
    moves = list(b.legal_moves)
    return random.choice(moves)
