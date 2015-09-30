"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    max_scores = 0
    for num in hand:
        scores = 0
        for dice in hand:
            if dice == num:
                scores += num
        if scores > max_scores:
            max_scores = scores
    return max_scores


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = range(1, num_die_sides + 1)
    total_scores = 0
    possibles = gen_all_sequences(outcomes, num_free_dice)
    for sequence in possibles:
        tem_set = held_dice + sequence
        total_scores += score(tem_set)
    expected = float(total_scores)/len(possibles)    
    return expected


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    length = len(hand)
    for num in range(length):
        answer_set.add(tuple([hand[num]]))
        tem_list = list()
        tem_list.append([hand[num]])
        for num2 in range(num+1, length):
            tem_list2 = list()
            for item in tem_list:
                # print num, num2, item
                tem_item = list()
                tem_item.extend(item)
                tem_item.append(hand[num2])
                # print tem_item
                answer_set.add(tuple(tem_item))
                tem_list2.append(tem_item)
            tem_list.extend(tem_list2)
                
    return answer_set



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    possible_holds = gen_all_holds(hand)
    max_scores = 0
    length = len(hand)
    for sets in possible_holds:
        scores = expected_value(sets, num_die_sides, length - len(sets))
        if scores > max_scores:
            held = sets
            max_scores = scores
    return (max_scores, held)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
# run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
# hand = tuple([1, 2, 3, 4, 5])    
# p = gen_all_holds(hand)
# print p, len(p)    
    
# hand = (2, 2, 2, 2, 1)
# print score(hand)
# print expected_value((2, 2, 2), 6, 2)
# print strategy((1, ), 6)