class IllegalMove(Exception):
    pass


class Board:

    _s = "XO"

    def __init__(self):
        self.reset()

    def reset(self):
        self._b = [" "] * 9
        self.nmoves = 0
        self._winner = None

    def _pos2idx(self, x: int, y: int):
        return 3 * x + y

    def __getitem__(self, idx_tuple):
        if isinstance(idx_tuple, int):
            return self._b[idx_tuple]
        if idx_tuple[1] is None:
            return self._b[idx_tuple[0]]
        return self._b[self._pos2idx(*idx_tuple)]

    def __setitem__(self, idx_tuple, value):
        if isinstance(idx_tuple, int):
            self._b[idx_tuple] = value
            return
        if idx_tuple[1] is None:
            self._b[idx_tuple[0]] = value
            return
        self._b[self._pos2idx(*idx_tuple)] = value

    def move(self, x: int, y: int = None):

        if self._winner:
            return -1
            # raise IllegalMove(f"This board has already a winner: {self._winner}")

        if self[x, y] != " ":
            return -1
            # raise IllegalMove(f"The position is already set to: {self[x, y]}")

        self[x, y] = self._s[self.nmoves % 2]
        self.nmoves += 1

        self.update_winner()
        if self._winner is None or self._winner == "tie":
            return 0
        return 1

    def _check(self, v0, v1, v2):
        if v0 == v1 and v1 == v2 and v0 != " ":
            self._winner = v0

    def get_state(self):
        return "".join(self._b)

    def update_winner(self):
        for i in range(3):
            self._check(self[i, 0], self[i, 1], self[i, 2])
            if self._winner:
                return
            self._check(self[0, i], self[1, i], self[2, i])
            if self._winner:
                return

        self._check(self[0, 0], self[1, 1], self[2, 2])
        if self._winner:
            return
        self._check(self[0, 2], self[1, 1], self[2, 0])

        if self.nmoves == 9:
            self._winner = "tie"

    def print_state(self):
        print(
            f"""
 {self[0,0]} | {self[0,1]} | {self[0,2]}
-----------
 {self[1,0]} | {self[1,1]} | {self[1,2]}
-----------
 {self[2,0]} | {self[2,1]} | {self[2,2]}
"""
        )
