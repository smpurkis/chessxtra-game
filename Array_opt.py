


def check_position_is_on_board(position, board_shape):
    #pythran export check_position_is_on_board((int, int), (int, int)) 
    return (0 <= position[0] <= board_shape[0] - 1) and (
        0 <= position[1] <= board_shape[1] - 1
    )
    
def dist(pos1, pos2):
    #pythran export dist((int, int), (int, int)) 
    return abs(pos1[0] - pos2[0]) - abs(pos1[1] - pos2[1])