from dataclasses import dataclass
from typing import override
from src.algorithms.base import JAlgorithmBase
from src.algorithms.utils.types import Neighbors, Tiles, iVec2D


@dataclass
class State:
    added: bool
    pair: iVec2D


class JDFSSolver(JAlgorithmBase):
    def __init__(self, cost_func):
        super().__init__(cost_func)
        self._required_tiles: int = 0
        self._curr_num_tiles: int = 0
        self.neighbors: Neighbors = []
        self.history: list[State] = []

    @override
    def solve(self, tiles: Tiles, neighbors: Neighbors, dims: iVec2D) -> bool:
        board_size: int = dims.x * dims.y
        self._required_tiles = board_size // 2
        self._curr_num_tiles = 0
        self._pairs = [-1] * len(tiles)
        self.neighbors = neighbors
        return self._solve()

    def _solve(self) -> bool:
        if self._required_tiles == self._curr_num_tiles:
            return True

        start: int = -1
        for i, pair in enumerate(self._pairs):
            if pair == -1:
                start = i
                break

        if start == -1:
            return False

        self.tracker.steps_forward += 1

        for neighbor in self.neighbors[start]:
            if self._pairs[neighbor] > -1:
                continue

            self._pairs[start] = neighbor
            self._pairs[neighbor] = start
            self._curr_num_tiles += 1
            self.history.append(State(True, iVec2D(start, neighbor)))

            if self._solve():
                return True

            self._pairs[neighbor] = -1
            self._pairs[start] = -1
            self.history.append(State(False, iVec2D(start, neighbor)))
            self._curr_num_tiles -= 1
            self.tracker.steps_backward += 1

        return False
