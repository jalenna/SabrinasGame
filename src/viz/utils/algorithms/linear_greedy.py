from typing import cast
from tiling_algorithms.utils.core import absdiff, create_neighbors
from tiling_algorithms.utils.types import Neighbors, Pairs, Tiles, iVec2D


class LinearGreedySolver:
    def __init__(self) -> None:
        self.pairs: Pairs = []

    def solve(self, dims: iVec2D, board: Tiles) -> None:
        self.pairs: Pairs = [-1] * (dims.x * dims.y)

        neighbors: Neighbors = create_neighbors(dims, board, absdiff)

        for i in range(len(board)):
            if self.pairs[i] > -1:
                continue

            for j in neighbors[i]:
                if self.pairs[j] > -1:
                    continue

                self.pairs[i] = j
                self.pairs[j] = i
                break
