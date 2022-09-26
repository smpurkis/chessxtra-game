class Array2D:
    def __init__(self, shape: tuple[int, int] = (4, 6)) -> None:
        self.shape = shape
        self._data = [["-" for i in range(shape[0])] for j in range(shape[1])]

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


if __name__ == "__main__":
    a = Array2D()
    print(a[0])
    print(a)
    a[0][1] = "1"
    print(a)
