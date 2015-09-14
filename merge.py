"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    n_line = list()
    flag = False
    for num in range(len(line)):
        if line[num] == 0:
            continue
        elif flag == False:
            n_line.append(line[num])
            flag = True
        elif line[num] == n_line[-1]:
            n_line[-1] = n_line[-1] * 2
            flag = False
        else:
            n_line.append(line[num])
            flag = True
    for num in range(len(n_line), len(line)):
        n_line.append(0)
    print n_line
    return n_line

list1 = [2, 0, 2, 4]
list2 = [0, 0, 2, 2]
list3 = [2, 2, 0, 0]
list4 = [2, 2, 2, 2, 2]
list5 = [8, 16, 16, 8]

merge(list1)
merge(list2)
merge(list3)
merge(list4)
merge(list5)