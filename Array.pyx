cimport cython
import numpy as np
cimport numpy as np

Array2D = np.ndarray


cpdef bint check_position_is_on_board(tuple position, tuple board_shape):
    return (0 <= position[0] <= board_shape[0] - 1) and (
        0 <= position[1] <= board_shape[1] - 1
    )

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)
cdef long dist(tuple pos1, tuple pos2):
    return abs(pos1[0] - pos2[0]) - abs(pos1[1] - pos2[1])


cpdef list filter_positions_off_board_list(
    list positions, tuple board_shape
):
    return [pos for pos in positions if check_position_is_on_board(pos, board_shape)]


# @profile

cpdef tuple get_col_row_positions(
    tuple pos, tuple board_shape, long max_range = 0
):
    cdef:
        long col_range
        long row_range
        list column_positions
        list row_positions
        long i

    col_range = board_shape[0] if max_range == 0 else min(board_shape[0], max_range)
    column_positions = split_at_position(
        filter_positions_off_board_list(
            [(i, pos[1]) for i in range(col_range)], board_shape
        ),
        pos,
    )
    row_range = board_shape[1] if max_range == 0 else min(board_shape[1], max_range)
    row_positions = split_at_position(
        filter_positions_off_board_list(
            [(pos[0], i) for i in range(row_range)], board_shape
        ),
        pos,
    )
    return column_positions, row_positions


cpdef list get_diagonal_positions(
    tuple pos, tuple board_shape, int max_range = 0
):
    cdef:
        list diagonal_positions
        long a
        long b
        long highest_board_shape
        long diagonal_range
        list positions

    diagonal_positions = []
    for a, b in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        highest_board_shape = max(*board_shape)
        diagonal_range = (
            highest_board_shape
            if max_range == 0
            else min(highest_board_shape, max_range)
        )
        positions = split_at_position(
            filter_positions_off_board_list(
                [(pos[0] + i * a, pos[1] + i * b) for i in range(diagonal_range)],
                board_shape,
            ),
            pos,
        )
        diagonal_positions.append(positions)
    return diagonal_positions


cpdef list get_l_positions(tuple pos, tuple board_shape):
    cdef:
        list l_offsets
        list positions

    l_offsets = [(-1, 2), (1, 2), (-1, -2), (1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
    positions = filter_positions_off_board_list(
        [(pos[0] + i, pos[1] + j) for i, j in l_offsets], board_shape
    )
    return positions


cpdef list get_surrounding_positions(tuple pos, tuple board_shape):
    cdef list positions = filter_positions_off_board_list(
        [(pos[0] + i, pos[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1)], board_shape
    )
    return positions


cpdef list split_at_position(list positions, tuple pos):
    index = positions.index(pos)
    return [positions[0:index], positions[index + 1 : len(positions)]]


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef list sort_by_distance(tuple pos, list positions):
    cdef list position_distances = sorted([(dist(pos, p), p) for p in positions])
    cdef list distances = [p[1] for p in position_distances]
    return distances
