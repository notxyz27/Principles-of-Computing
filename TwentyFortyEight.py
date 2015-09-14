"""
Clone of 2048 game
"""

# import poc_2048_gui
import random
# import poc_simpletest

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
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
    return n_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self.reset()
        self._dir_initials = {UP : [(0, num) for num in range(grid_width)],
                                  DOWN : [(grid_height - 1, num) for num in range(grid_width)],
                                  LEFT : [(num, 0) for num in range(grid_height)],
                                  RIGHT : [(num, grid_width - 1) for num in range(grid_height)]}
                
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._grid = [[0 for dummy_col in range(self._width)] for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return "Yo man!"

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        local_grid = [item[:] for item in self._grid]
        x_offset = OFFSETS[direction][0]
        y_offset = OFFSETS[direction][1]
        for row, col in self._dir_initials[direction]:
            tem_list = list()
            x_index = row
            y_index = col
            while x_index in range(self._height) and y_index in range(self._width):
                tem_list.append(self._grid[x_index][y_index])
                x_index = x_index + x_offset
                y_index = y_index + y_offset
            tem_list = merge(tem_list)
            x_index = row
            y_index = col
            index = 0
            while x_index in range(self._height) and y_index in range(self._width):
                self._grid[x_index][y_index] = tem_list[index]
                x_index = x_index + x_offset
                y_index = y_index + y_offset
                index = index + 1
        if self._grid != local_grid:
            self.new_tile()
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        flag = False
        for num in self._grid:
            if 0 in num:
                flag = True
        
        if flag == False:
            print "You lost"
            return 0
            
        while flag:
            row = random.randint(0, self._height - 1)
            col = random.randint(0, self._width - 1)
            if self._grid[row][col] == 0:
                break
        if random.randint(1, 10) > 9:
            self._grid[row][col] = 4
        else:
            self._grid[row][col] = 2
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]


# poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

