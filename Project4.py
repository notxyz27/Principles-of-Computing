"""
Project 4 -  Computing alignments of sequences

Matrix functions

alignment_matrix - grid
scoring_matrix - dictionary of dictionaries

build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
The score for any entry indexed by one or more dashes is dash_score
The score for the remaining diagonal entries is diag_score
The score for the remaining off-diagonal entries is off_diag_score

compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
global_flag - Ture: Compute global alignment matrix
global_flag - False: Compute global alignment matrix
        
Alignment functions

compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):

compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):


"""
def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Build the scoring matrix for use in computing alignments
    
    Input: alphabet is a set of characters, diag_score, dash_score, and off_diag_score are integers
    
    Output: scoring matrix as a dictionary of dictionaries
    
    """
    if len(alphabet) == 0:
        return "alphanet is empty"
    
    alphabet.add("-")
    scoring_matrix = dict()
    for char1 in alphabet:
        scoring_matrix[char1] = dict()
        for char2 in alphabet:
            if char2 == "-" or char1 == "-":
                scoring_matrix[char1][char2] = dash_score
            elif char2 == char1:
                scoring_matrix[char1][char2] = diag_score
            else:
                scoring_matrix[char1][char2] = off_diag_score
    
    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Build the alignment_matrix for use in computing alignments
    
    Input: seq_x and seq_y are two strings to find alignments, scoring_matrix is a dictionary 
    global_flag is a boolean value
    
    Output: alginment matrix as a grid (list of lists)
    
    """

    x_length = len(seq_x)
    y_length = len(seq_y)
    alignment_matrix = [[0 for dummy_col in range(y_length + 1)] for dummy_row in range(x_length + 1)]
    for indexr in range(1, x_length + 1):
        alignment_matrix[indexr][0] = alignment_matrix[indexr-1][0] + scoring_matrix[seq_x[indexr-1]]["-"]
        if (not global_flag) and alignment_matrix[indexr][0] < 0:
            alignment_matrix[indexr][0] = 0
    for indexc in range(1, y_length + 1):
        alignment_matrix[0][indexc] = alignment_matrix[0][indexc-1] + scoring_matrix["-"][seq_y[indexc-1]]
        if (not global_flag) and alignment_matrix[0][indexc] < 0:
            alignment_matrix[0][indexc] = 0
    for indexr in range(1, x_length + 1):
        for indexc in range(1, y_length + 1):
            alignment_matrix[indexr][indexc] = max(alignment_matrix[indexr-1][0] + scoring_matrix[seq_x[indexr-1]]["-"], alignment_matrix[0][indexc-1] + scoring_matrix["-"][seq_y[indexc-1]], alignment_matrix[indexr-1][indexc-1] + scoring_matrix[seq_x[indexr-1]][seq_y[indexc-1]])
            if (not global_flag) and alignment_matrix[indexr][indexc] < 0:
                alignment_matrix[indexr][indexc] = 0
    return alignment_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Compute the global alignments
    
    Input: seq_x and seq_y are two strings to find global alignments with highest score. 
    scoring_matrix is a dictionary, alignment_matrix is a grid.
    
    Output: two alignments with highest scores in format of tuple (score, align_x, align_y)
        
    """
    index_x = len(seq_x)
    index_y = len(seq_y)
    score = alignment_matrix[index_x][index_y]
    align_x = ""
    align_y = ""
    while index_x != 0 and index_y != 0:
        if alignment_matrix[index_x][index_y] == alignment_matrix[index_x-1][index_y-1] + scoring_matrix[seq_x[index_x-1]][seq_y[index_y-1]]:
            align_x = seq_x[index_x-1] + align_x
            align_y = seq_y[index_y-1] + align_y
            index_x -= 1
            index_y -= 1
        elif alignment_matrix[index_x][index_y] == alignment_matrix[index_x-1][index_y] + scoring_matrix[seq_x[index_x-1]]["-"]:
            align_x = seq_x[index_x-1] + align_x
            align_y = "-" + align_y
            index_x -= 1
        else:
            align_x = "-" + align_x
            align_y = seq_y[index_y-1] + align_y
            index_y -= 1
    while index_x != 0:
        align_x = seq_x[index_x-1] + align_x
        align_y = "-" + align_y
        index_x -= 1
    while index_y != 0:
        align_x = "-" + align_x
        align_y = seq_y[index_y-1] + align_y
        index_y -= 1
        
    return (score, align_x, align_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Compute the local alignments
    
    Input: seq_x nad seq_y are two strings to find local alignments with highest score,
    scorng matrix is a dictionary, alignment_matrix is a grid.
    
    Output: two local alignments with highest score in format of tuple (score, align_x, align_y)
    
    """
    index_x = len(seq_x)
    index_y = len(seq_y)
    align_x = ""
    align_y = ""
    score = 0
    for row in range(index_x + 1):
        for col in range(index_y + 1):
            if alignment_matrix[row][col] > score:
                score = alignment_matrix[row][col]
                index_x = row
                index_y = col
    while index_x != 0 and index_y != 0:
        if alignment_matrix[index_x][index_y] == 0:
            return (score, align_x, align_y)
        if alignment_matrix[index_x][index_y] == alignment_matrix[index_x-1][index_y-1] + scoring_matrix[seq_x[index_x-1]][seq_y[index_y-1]]:
            align_x = seq_x[index_x-1] + align_x
            align_y = seq_y[index_y-1] + align_y
            index_x -= 1
            index_y -= 1
        elif alignment_matrix[index_x][index_y] == alignment_matrix[index_x-1][index_y] + scoring_matrix[seq_x[index_x-1]]["-"]:
            align_x = seq_x[index_x-1] + align_x
            align_y = "-" + align_y
            index_x -= 1
        else:
            align_x = "-" + align_x
            align_y = seq_y[index_y-1] + align_y
            index_y -= 1
    while index_x != 0:
        if alignment_matrix[index_x][index_y] == 0:
            return (score, align_x, align_y)
        align_x = seq_x[index_x-1] + align_x
        align_y = "-" + align_y
        index_x -= 1
    while index_y != 0:
        if alignment_matrix[index_x][index_y] == 0:
            return (score, align_x, align_y)
        align_x = "-" + align_x
        align_y = seq_y[index_y-1] + align_y
        index_y -= 1
    return (score, align_x, align_y)
# Test
# Test for build_scoring_matrix
score_matrix = build_scoring_matrix(set(["a", "b", "c"]), 2, 1, -1)
print score_matrix
print build_scoring_matrix(set([]), 2, 1, 0)

#Test for compute_alignment_matrix
align_matrix = compute_alignment_matrix("abcca", "bcaa", score_matrix, True)
print align_matrix

# Test for compute_global_alignment
print compute_global_alignment("abcca", "bcaa", score_matrix, align_matrix)

# Test for compute_local_alignment
local_align_matrix = compute_alignment_matrix("abcca", "bcaa", score_matrix, False)
print local_align_matrix
print compute_local_alignment("abcca", "bcaa", score_matrix, local_align_matrix)