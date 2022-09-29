class Array2D:
    def __init__(self, shape: tuple[int, int] = (6, 4)) -> None:
        self.shape = shape
        self._data = []
        for i in range(shape[0]):
            self._data.append(["-" for j in range(shape[1])])

    def __getitem__(self, index: int) -> int:
        return self._data[index]

    def __str__(self) -> str:
        repr_list = []
        for row in self._data:
            repr_row = []
            for el in row:
                repr_row.append(el)
            repr_list.append(" ".join(map(str, repr_row)))
        return "\n".join(repr_list)


Position = tuple[int, int]
Shape = tuple[int, int]


def check_position_is_on_board(position: Position, board_shape: Shape) -> bool:
    return (0 <= position[0] <= board_shape[0] - 1) and (
        0 <= position[1] <= board_shape[1] - 1
    )


def filter_positions_off_board(
    positions: list[Position], board_shape: Shape
) -> list[Position]:
    return [pos for pos in positions if check_position_is_on_board(pos, board_shape)]


def get_col_row_positions(pos: Position, board_shape: Shape) -> tuple[list[list[Position]], list[list[Position]]]: 
    column_positions = split_at_position(
        filter_positions_off_board(
            [(i, pos[1]) for i in range(board_shape[0])], board_shape
        ),
        pos,
    )
    row_positions = split_at_position(
        filter_positions_off_board(
            [(pos[0], i) for i in range(board_shape[1])], board_shape
        ),
        pos,
    )
    return column_positions, row_positions


def split_at_position(positions: list[Position], pos: Position) -> list[list[Position]]:
    index = positions.index(pos)
    return [positions[0:index], positions[index + 1 : len(positions)]]


def dist(pos1: Position, pos2: Position) -> float:
    return abs(pos1[0] - pos2[0]) - abs(pos1[1] - pos2[1])


def sort_by_distance(pos: Position, positions: list[Position]) -> list[Position]:
    position_distances = sorted([(dist(pos, p), p) for p in positions])
    distances = [p[1] for p in position_distances]
    return distances



if __name__ == "__main__":
    a = Array2D()
    print(a[0])
    print(a)
    a[0][1] = "1"
    print(a)
