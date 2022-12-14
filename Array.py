from typing import List, Tuple, Set, Union, Any, Optional

# from Array_opt import check_position_is_on_board, dist


class Array2D:
    def __init__(self, shape: Tuple[int, int] = (6, 4)) -> None:
        self.shape = shape
        self._data = []
        for i in range(shape[0]):
            self._data.append(["-" for j in range(shape[1])])

    def __getitem__(self, index: int) -> Union[List[Any], Any]:
        return self._data[index]

    def __str__(self) -> str:
        repr_list = []
        for row in self._data:
            repr_row = []
            for el in row:
                repr_row.append(el)
            repr_list.append(" ".join(map(str, repr_row)))
        return "\n".join(repr_list)


Position = Tuple[int, int]
Shape = Tuple[int, int]


def check_position_is_on_board(position: Position, board_shape: Shape) -> bool:
    return (0 <= position[0] <= board_shape[0] - 1) and (
        0 <= position[1] <= board_shape[1] - 1
    )


def dist(pos1: Position, pos2: Position) -> float:
    return abs(pos1[0] - pos2[0]) - abs(pos1[1] - pos2[1])


def filter_positions_off_board_list(
    positions: List[Position], board_shape: Shape
) -> List[Position]:
    return [pos for pos in positions if check_position_is_on_board(pos, board_shape)]


def filter_positions_off_board_set(
    positions: Set[Position], board_shape: Shape
) -> Set[Position]:
    return {pos for pos in positions if check_position_is_on_board(pos, board_shape)}


def get_col_row_positions(
    pos: Position, board_shape: Shape, max_range: Optional[int] = None
) -> Tuple[List[List[Position]], List[List[Position]]]:
    col_range = board_shape[0] if max_range is None else min(board_shape[0], max_range)
    column_positions = split_at_position(
        filter_positions_off_board_list(
            [(i, pos[1]) for i in range(col_range)], board_shape
        ),
        pos,
    )
    row_range = board_shape[1] if max_range is None else min(board_shape[1], max_range)
    row_positions = split_at_position(
        filter_positions_off_board_list(
            [(pos[0], i) for i in range(row_range)], board_shape
        ),
        pos,
    )
    return column_positions, row_positions


def get_diagonal_positions(
    pos: Position, board_shape: Shape, max_range: Optional[int] = None
) -> List[List[List[Tuple[int, int]]]]:
    diagonal_positions = []
    for a, b in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        highest_board_shape = max(*board_shape)
        diagonal_range = (
            highest_board_shape
            if max_range is None
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


def get_l_positions(pos: Position, board_shape: Shape) -> Set[Position]:
    l_offsets = ((-1, 2), (1, 2), (-1, -2), (1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
    positions = filter_positions_off_board_set(
        {(pos[0] + i, pos[1] + j) for i, j in l_offsets}, board_shape
    )
    return positions


def get_surrounding_positions(pos: Position, board_shape: Shape) -> Set[Position]:
    positions = filter_positions_off_board_set(
        {(pos[0] + i, pos[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1)}, board_shape
    )
    return positions


def split_at_position(positions: List[Position], pos: Position) -> List[List[Position]]:
    index = positions.index(pos)
    return [positions[0:index], positions[index + 1 : len(positions)]]


def sort_by_distance(pos: Position, positions: List[Position]) -> List[Position]:
    position_distances = sorted([(dist(pos, p), p) for p in positions])
    distances = [p[1] for p in position_distances]
    return distances
