import numpy as np
from tile import Cell
from typing import cast


class DFS:
    pairs: list[int | None] = []
    cells: list[Cell] = []
    _required_tiles: int = 0
    _curr_num_tiles: int = 0
    back: int = 0
    forw: int = 0

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.pairs = []
        self.cells = []
        self._required_tiles = 0
        self._curr_num_tiles = 0
        self.back = 0
        self.forw = 0

    def solve(self, w: int, h: int, costs_board: np.ndarray) -> None:
        self.reset()

        self.pairs = [None for _ in range(w * h)]

        self._required_tiles = (w * h) // 2

        self.cells = self.create_neighbors(w, h, costs_board)

        self._solve(costs_board)

    def create_neighbors(self, w: int, h: int, costs: np.ndarray) -> list[Cell]:
        result: list[Cell] = []

        for i in range(w * h):
            row: int = i // w
            col: int = i % w

            cell: Cell = Cell(row, col, costs[i])

            # Left
            if col > 0:
                cell.neighbor_ids.append(i - 1)
            # Right
            if col + 1 < w:
                cell.neighbor_ids.append(i + 1)
            # Up
            if row > 0:
                cell.neighbor_ids.append(i - w)
            # Down
            if row + 1 < h:
                cell.neighbor_ids.append(i + w)

            cell.neighbor_ids.sort(
                key=lambda x: abs(cast(int, cell.value) - costs[x])
            )

            result.append(cell)

        return result

    def _solve(self, costs_board: np.ndarray) -> bool:
        if self._required_tiles == self._curr_num_tiles:
            return True

        start = -1
        for i, pair in enumerate(self.pairs):
            if pair is None:
                start = i
                break

        if start == -1:
            return False

        self.forw += 1

        for neighbor in self.cells[start].neighbor_ids:
            if self.pairs[neighbor] is not None:
                continue

            self.pairs[neighbor] = start
            self.pairs[start] = neighbor
            self._curr_num_tiles += 1

            if self._solve(costs_board):
                return True

            self.pairs[neighbor] = None
            self.pairs[start] = None
            self._curr_num_tiles -= 1
            self.back += 1

        return False
