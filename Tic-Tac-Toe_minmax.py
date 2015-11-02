"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    empty_squares = board.get_empty_squares()
    # print player
    # print board
    # print empty_squares
    scores = []
    for square in empty_squares:
        tem_board = board.clone()
        tem_board.move(square[0], square[1], player)
        winner = tem_board.check_win()
        if winner == None:
            scores.append([mm_move(tem_board, provided.switch_player(player))[0], square])
            # print "added:", scores
        elif winner == player:
            return SCORES[player], square
        # print square
        # print empty_squares
    # print scores
    if len(scores) > 0:
        score = scores[0][0]
        (row, col) = scores[0][1]
        for item in scores:
            if item[0]*SCORES[player] > score*SCORES[player]:
                score = item[0]
                (row, col) = item[1]
        return score, (row, col)
    return 0, (-1, -1)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
'''
board1 = provided.TTTBoard(3)
board1.move(1, 1, provided.PLAYERX)
board1.move(0, 0, provided.PLAYERO)
board1.move(0, 1, provided.PLAYERX)
board1.move(2, 1, provided.PLAYERO)
board1.move(2, 2, provided.PLAYERX)
board1.move(1, 0, provided.PLAYERO)
print mm_move(board1, provided.PLAYERX)
'''