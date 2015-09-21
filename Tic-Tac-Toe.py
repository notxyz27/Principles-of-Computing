"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function takes a current board and the next player to move
    """
    empty_squares = board.get_empty_squares()
    dim = board.get_dim()
    
    for dummy_num in range(dim * dim):
        if board.check_win() != None:
            break
        index = random.randomint(0, len(empty_squares)-1)
        pos = empty_squares.pop(index)
        board.move(pos[0], pos[1], player)
        
        player = provided.switch_player(player)
    
    return

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores with the same dimension as the Tic-Tac-Toe board
    """
    winner = oard.check_win()
    dim = board.get_dim()
    for row in range(dim):
        for col in range(dim):
            player_in = board.square(row, col)
    return
def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores
    """
    best = None
    empty_squares = board.get_empty_squares()
    for row, col in empty_squares:
        if scores[row][col] > best:
            best = scores[row][col]
            best_row = row
            best_col = col
            
    return (best_row, best_col)

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is
    """
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
dim = 3
board = provided.TTTBoard(dim)
scores_grid = [[0 for dummy_col in range(dim)] for dummy_row in range(dim)]
# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
