"""
Application 4 scripts

"""
import Project4 as help
import alg_application4_provided as provided
import random

seq_x = provided.read_protein(provided.HUMAN_EYELESS_URL)
seq_y = provided.read_protein(provided.FRUITFLY_EYELESS_URL)
score_matrix = provided.read_scoring_matrix(provided.PAM50_URL)
"""
# Question1
local_align_matrix = help.compute_alignment_matrix(seq_x, seq_y, score_matrix, False)
score, align_x, align_y = help.compute_local_alignment(seq_x, seq_y, score_matrix, local_align_matrix)

# Question2
new_seq_x = align_x.rstrip("-QQ")
new_seq_x = new_seq_x + "QQ"
new_seq_y = align_y
seq_consensus = provided.read_protein(provided.CONSENSUS_PAX_URL)
global_matrix_x = help.compute_alignment_matrix(new_seq_x, seq_consensus, score_matrix, True)
score_x_consensus, align_x1, align_y1 = help.compute_global_alignment(new_seq_x, seq_consensus, score_matrix, global_matrix_x)
global_matrix_y = help.compute_alignment_matrix(new_seq_y, seq_consensus, score_matrix, True)
score_y_consensus, align_x2, align_y2 = help.compute_global_alignment(new_seq_y, seq_consensus, score_matrix, global_matrix_y)

# Question3
alphabets = "ACBEDGFIHKMLNQPSRTWVYXZ"
seq1 = ""
seq2 = ""
for dummy_num in range(len(seq_x)):
    seq1 = alphabets[random.randint(0, 22)] + seq1
for dummy_num in range(len(seq_y)):
    seq2 = alphabets[random.randint(0, 22)] + seq2
local_align_matrix_3 = help.compute_alignment_matrix(seq1, seq2, score_matrix, False)
score3, align_x3, align_y3 = help.compute_local_alignment(seq1, seq2, score_matrix, local_align_matrix_3)

# Question4
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    scoring_distribution = dict()
    num = 0
    while num < num_trials:
        y_list = list(seq_y)
        random.shuffle(y_list)
        rand_y = ""
        for char in y_list:
            rand_y = rand_y + char
        local_align_matrix = help.compute_alignment_matrix(seq_x, rand_y, score_matrix, False)
        score = help.compute_local_alignment(seq_x, rand_y, score_matrix, local_align_matrix)[0]
        if not scoring_distribution.has_key(score):
            scoring_distribution[score] = 1
        else:
            scoring_distribution[score] += 1
        num += 1
    return scoring_distribution
s_distribution = generate_null_distribution(seq_x, seq_y, score_matrix, 1000)
provided.plt.bar(s_distribution.keys(), s_distribution.values(), 1, color = "blue")


# Question8
word_list = provided.read_words(provided.WORD_LIST_URL)
def check_spelling(checked_word, dist, word_list):
    char_set = set(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", 
    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "-"])
    score_matrix = help.build_scoring_matrix(char_set, 2, 1, 0)
    words_set = set()
    for word in word_list:
        align_matrix = help.compute_alignment_matrix(word, checked_word, score_matrix, True)
        len_word = len(word)
        len_check = len(checked_word)
        if len_word + len_check - align_matrix[len_word][len_check] <= dist:
            words_set.add(word)
    return words_set
set1 = check_spelling("humble", 1, word_list)
set2 = check_spelling("firefly", 2, word_list)
"""

# Question9
# word_set = set(word_list)
def check_spelling2(checked_word, dist, word_set):
    words_set = set()
    check_set = set()
    check_set.add("")
    for char in checked_word:
        tem_set = check_set.copy()
        for string in tem_set:
            check_set.add(string + char)
    for word in word_set:
        len_word = len(word)
        equal = 0
        max_equal = 0
        for check in check_set:
            len_check = len(check)
            index_check = 0
            index_word = 0
            while index_check < len_check:
                tem_equal = equal
                while index_word < len_word:
                    if check[index_check] == word[index_word]:
                        equal += 1
                        index_word += 1
                        break
                    index_word += 1
                if equal == tem_equal:
                    break
                index_check += 1
            if index_check == len_check and len_check > max_equal:
                max_equal = len_check
        tem_distance = len_check - max_equal + len_word - max_equal
        if tem_distance <= dist:
            words_set.add(word)
    return words_set