"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

# import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        
        assert target_row > 1, "target_row <= 1"
        # Check whether the value at the location is 0
        if self._grid[target_row][target_col] != 0:
            return False
        target_col += 1
        # Check whether the tiles to the right of the row are solved
        while target_col < self.get_width():
            if self._grid[target_row][target_col] != target_row * self.get_width() + target_col:
                return False
            target_col += 1
        # Check whether tiles below the row are solved
        target_row += 1
        while target_row < self.get_height():
            target_col = 0
            while target_col < self.get_width():
                if self._grid[target_row][target_col] != target_row * self.get_width() + target_col:
                    return False
                target_col += 1
            target_row += 1
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_string = ""
        cur_pos = self.current_position(target_row, target_col)
        ver_dis = target_row - cur_pos[0]
        if cur_pos[0] == target_row:
            hor_dis = target_col - cur_pos[1]
            # First move 0 to the location of target tile and target tile on the right of 0
            for dummy_step in range(hor_dis):
                move_string += "l"
            # Then implement cyclic moves till the tile is moved to solved location and 0 lies left to the location
            move_string += position_tile("u", "r", "d", "l", hor_dis, 1)
        # When current col of target tile is larger than its solved location 
        elif cur_pos[1] > target_col:
            move_string += "u"
            hor_dis = cur_pos[1] - target_col
            # First move 0 to the location of target tile and target tile on the left
            for dummy_step in range(ver_dis - 1):
                move_string += "u" 
            for dummy_step in range(hor_dis):
                move_string += "r"
            # When current row of target tile is 0 (the first row)
            if cur_pos[0] == 0:
                # Move target tile left till it lies in the same col of its solved location and target tile under 0
                move_string += position_tile("d", "l", "u", "r", hor_dis, 0)
            else:
                # Move target tile left till it lies in the same col of its solved location and target tile under 0 
                move_string += position_tile("u", "l", "d", "r", hor_dis, 0)
                move_string += "u"
            # Move target tile down till it lies in its solved location and 0 on its left
            move_string += position_tile("l", "d", "r", "u", ver_dis + 1, 1)
            move_string += "ld"
        # When the current location of the target tile is at the same col of 0
        elif cur_pos[1] == target_col:
            move_string += "u"
            # First move 0 to current location of target tile and target tile under 0
            for dummy_step in range(ver_dis - 1):
                move_string += "u"
            # Move target tile down till it lies in its solved location and 0 on its left
            move_string += position_tile("l", "d", "r", "u", ver_dis, 1)
            move_string += "ld"
        # When the current col of target tile is less than that of solved location
        else:
            move_string += "u"
            hor_dis = target_col - cur_pos[1]
            # First move 0 to the current location of target tile and target tile under 0
            for dummy_step in range(hor_dis):
                move_string += "l" 
            for dummy_step in range(ver_dis - 1):
                move_string += "u"
            # Move target tile down till it lies at the same row of solved location and 0 on its top
            move_string += position_tile("r", "d", "l", "u", ver_dis, 1)
            # Move 0 to the location of target tile and target tile on the right of 0
            move_string += "rdl"
            # Move target tile right till it lies at the target location and 0 on its left
            move_string += position_tile("u", "r", "d", "l", hor_dis, 1)
        self.update_puzzle(move_string)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_string = "ur"
        self.update_puzzle("ur")

        # When target tile is not moved to its solved position after "ur"
        if self.current_position(target_row, 0) != (target_row, 0):
            cur_pos = self.current_position(target_row, 0)
            ver_dis = target_row - 1 - cur_pos[0]
            if cur_pos[1] > 1:
                hor_dis = cur_pos[1] - 1
                # First move 0 to the location of target tile and target tile on the left
                for dummy_step in range(ver_dis):
                    move_string += "u" 
                for dummy_step in range(hor_dis):
                    move_string += "r"
                # When current row of target tile is 0 (the first row)
                if cur_pos[0] == 0:
                    # Move target tile left till it lies in the same col of its solved location and target tile under 0
                    move_string += position_tile("d", "l", "u", "r", hor_dis, 0)
                    # Move target tile down till it lies in its solved location and 0 on its left
                    move_string += position_tile("l", "d", "r", "u", ver_dis, 1)
                    move_string += "ld"
                else:
                    # Move target tile left till it lies in the same col of its solved location and target tile under 0 
                    move_string += position_tile("u", "l", "d", "r", hor_dis, 0)
                    move_string += "u"
                    move_string += position_tile("l", "d", "r", "u", ver_dis + 1, 1)
            # When the current location of the target tile is at the same col of 0
            elif cur_pos[1] == 1:
                # First move 0 to current location of target tile and target tile under 0
                for dummy_step in range(ver_dis):
                    move_string += "u"
                # Move target tile down till it lies in its solved location and 0 on its left
                move_string += position_tile("l", "d", "r", "u", ver_dis, 1)
                move_string += "ld"
            # When the current col of target tile is less than that of solved location
            elif cur_pos[0] == target_row - 1:
                move_string += "l"
            else:
                hor_dis = 1 - cur_pos[1]
                # First move 0 to the current location of target tile and target tile under 0
                move_string += "l" 
                for dummy_step in range(ver_dis):
                    move_string += "u"
                # Move target tile down till it lies at the same row of solved location and 0 on its top
                move_string += position_tile("r", "d", "l", "u", ver_dis, 1)
                # Move 0 to the location of target tile and target tile on the right of 0
                move_string += "rdl"
            self.update_puzzle(move_string[2:])
            move_string += "ruldrdlurdluurddlur"
            self.update_puzzle("ruldrdlurdluurddlur")
        for dummy_step in range(self.get_width() - 2):
            move_string += "r"
        self.update_puzzle(move_string[-self.get_width()+2:])
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0 or self._grid[1][target_col] != self.get_width() + target_col:
            return False
        index = target_col + 1
        while index < self.get_width():
            if self._grid[0][index] != index or self._grid[1][index] != self.get_width() + index:
                return False
            index += 1
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self._grid[row][col] != row * self.get_width() + col:
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[1][target_col] != 0:
            return False
        index = target_col + 1
        while index < self.get_width():
            if self._grid[0][index] != index or self._grid[1][index] != self.get_width() + index:
                return False
            index += 1
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self._grid[row][col] != row * self.get_width() + col:
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        move_string = ""
        cur_pos = self.current_position(1, target_col)
        hor_dis = target_col - cur_pos[1]
        for dummy_step in range(hor_dis):
            move_string += "l"
        if cur_pos[0] == 1:
            move_string += position_tile("u", "r", "d", "l", hor_dis, 1)
        elif cur_pos[1] == target_col:
            move_string += "uld"
        else:
            move_string += "urdl"
            move_string += position_tile("u", "r", "d", "l", hor_dis, 1)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""
    
def position_tile(dir1, dir2, dir3, dir4, ver_hor, res):
    """
    Helper function to implement cyclic movements
    
    """
    moves = ""
    num = 0
    while num < ver_hor - res:
        moves += dir1
        for dummy_step in range(ver_hor - num):
            moves += dir2
        moves += dir3
        for dummy_step in range(ver_hor - num - 1):
            moves += dir4
        num += 1
    return moves

# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
####### Test cases #######

# Test1 for lower_row_invariant
puzzle = Puzzle(4, 4, [[4, 2, 3, 7], [8, 5, 6, 10], [9, 1, 0, 11], [12, 13, 14, 15]])
print puzzle.lower_row_invariant(2, 2)

# Test2 for solve_interior_tile
puzzle.solve_interior_tile(2, 2)
print puzzle.lower_row_invariant(2, 1)
print puzzle._grid
puzzle.solve_interior_tile(2, 1)
print puzzle.lower_row_invariant(2, 0)
print puzzle._grid
puzzle.solve_col0_tile(2)
# print puzzle.lower_row_invariant(1, 3)
print puzzle._grid

puzzle1 = Puzzle(4, 4, [[5, 9, 2, 3], [14, 6, 15, 7], [12, 1, 13, 8], [4, 11, 10, 0]])
print puzzle1.lower_row_invariant(3, 3)
puzzle1.solve_interior_tile(3, 3)
print puzzle1.lower_row_invariant(3, 2)
print puzzle1._grid

puzzle2 = Puzzle(4, 4, [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11], [9, 0, 14, 15]])
print puzzle2.lower_row_invariant(3, 1)
puzzle2.solve_interior_tile(3, 1)
print puzzle2.lower_row_invariant(3, 0)
print puzzle2._grid
puzzle2.solve_col0_tile(3)
print puzzle2.lower_row_invariant(2, 3)
print puzzle2._grid