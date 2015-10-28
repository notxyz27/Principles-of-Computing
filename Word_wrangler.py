"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    num = None
    new_list = []
    for item in list1:
        if item != num:
            num = item
            new_list.append(item)
        else:
            continue
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    combined_list = []
    index1 = 0
    index2 = 0
    len1 = len(list1)
    len2 = len(list2)
    while index1 < len1 and index2 < len2:
        if list1[index1] < list2[index2]:
            index1 += 1
        elif list1[index1] > list2[index2]:
            index2 += 1
        else:
            combined_list.append(list1[index1])
            index1 += 1
            index2 += 1
    return combined_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    combined_list = []
    index1 = 0
    index2 = 0
    len1 = len(list1)
    len2 = len(list2)
    while index1 < len1 and index2 < len2:
        if list1[index1] < list2[index2]:
            combined_list.append(list1[index1])
            index1 += 1
        elif list1[index1] > list2[index2]:
            combined_list.append(list2[index2])
            index2 += 1
        else:
            combined_list.append(list1[index1])
            combined_list.append(list2[index2])
            index1 +=1
            index2 +=1
    if index1 == len1:
        combined_list += list2[index2:]
    if index2 == len2:
        combined_list += list1[index1:]
    return combined_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        mid = len(list1)/2
        sub_list1 = list1[0:mid]
        sub_list2 = list1[mid:len(list1)]
        sub_list1 = merge_sort(sub_list1)
        sub_list2 = merge_sort(sub_list2)
        list1 = merge(sub_list1, sub_list2)
    return list1

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    strings_list = []
    if len(word) == 0:
        return [""]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
    for string in rest_strings:
        index = 0
        while index <= len(string):
            strings_list.append(string[:index] + first + string[index:])
            index += 1
    return strings_list + rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename) # only useful for codeskulptor
    netfile = urllib2.urlopen(url)
    data = []
    for item in netfile.readlines():
        data.append(item[:-1])
    return data

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    
    
