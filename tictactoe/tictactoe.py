"""
Tic Tac Toe Player
"""
import copy
import math


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    o_count =0
    x_count =0
    for i in board:
        for j in i:
            if j == 'O':
                o_count+=1
            elif j == 'X':
                x_count +=1
    
    if o_count >= x_count:
        return 'X'
    else:
        return 'O'


def actions(board):
    possible_actions = set()
    
    for i,value in enumerate(board):
        for j, value1 in enumerate(value):
            if board[i][j] == None:
                possible_actions.add((i,j))
                
    return possible_actions


def result(board, action):
    board_copy = copy.deepcopy(board)
    
    i = action[0]
    j = action[1]
    if board_copy[i][j] == 'X' or board_copy[i][j] == 'O':
        raise Exception(f"{action} is not a valid action")
    else:
        play= player(board)
        board_copy[i][j] = play
    return board_copy


def winner(board):
    ways = {}
    temp3 = []
    for i,value in enumerate(board):
        temp1 = []
        temp2 = []
        for j,value in enumerate(board):
            temp1.append(board[i][j])
            temp2.append(board[j][i])
            if i ==j:
                
                temp3.append(board[i][j])
        ways[f'way{i+1}'] = temp1
        ways[f'way{i+4}'] = temp2
        ways['way7']= temp3
    ways['way8'] = [board[0][2],board[1][1],board[2][0]]
    
    for key, value in ways.items():
        
        if 'O' not in value and None not in value:
            return 'X'
        if 'X' not in value and None not in value:
            return 'O'
    
    return None


def terminal(board):
    win = winner(board)
    if win == 'X' or win == 'O':
        return True
    for i ,value in enumerate(board):
        for j in value:
            if j== None:
                return False
    return True


def utility(board):
    win = winner(board)
    if win == 'X':
        return 1
    elif win == 'O':
        return -1
    else:
        return 0


    
def minimax(board):
    end = terminal(board) 
    if end == True:
        return None
    available = actions(board)
    play = player(board)
    best_action = None
    if play == 'X':
        best_action_value = max_value(board)
        
        for action in available:
            if best_action_value == min_value(result(board,action)):
               best_action = action
               break
    if play == 'O':
        best_action_value = min_value(board)
        
        for action in available:
            if best_action_value == max_value(result(board,action)):
               best_action = action
               break
    
    return best_action


def min_value(state):
    available = actions(state)
    v = 99999999
   
    if terminal(state):
        return utility(state)
    for action in available:
        v = min(v,max_value(result(state,action)))
    return v



def max_value(state):
    available = actions(state)
    v = -99999999
   
    if terminal(state):
        return utility(state)
    for action in available:
        v = max(v,min_value(result(state,action)))
        
    return v
