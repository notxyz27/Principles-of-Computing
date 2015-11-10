def solve_interior_tile(self, target_row, target_col):
    move_string = ""
    cur_pos = self.current_position(target_row, target_col)
    ver_dis = target_row - cur_pos[0]
    if cur_pos[1] < target_col:
        
    self.update_puzzle(move_string)
    return move_string