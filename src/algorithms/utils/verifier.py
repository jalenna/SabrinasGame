from typing import Optional
from src.algorithms.base import Neighbors
from src.algorithms.utils.types import Pairs, Tiles, iVec2D


class InvalidSolution(Exception):
    ...


def solution_verifier(
    pairs: Pairs, neighbors: Neighbors
) -> None:
    if -1 in pairs:
        raise InvalidSolution("Solution contains unpaired cells")

    if len(set(pairs)) != len(pairs):
        raise InvalidSolution("Solution contains duplicates")

    for a in range(len(pairs)):
        b = pairs[a]

        if a == b:
            raise InvalidSolution("i: {a} is paired with itself")

        # a -> b, b <- a
        if pairs[b] != a:
            raise InvalidSolution(
                "{a} is paired to {b}, but {b} is not paired to {a}")

        if b not in neighbors[a]:
            raise InvalidSolution("{b} is not a neighbor of {a}")


def print_board(tiles: Tiles, dims: iVec2D, pairs: Optional[Pairs] = None) -> None:
    if pairs:
        return _print_solved_board(tiles, dims, pairs)

    for i in range(dims.x):
        for j in range(dims.y):
            print(tiles[(i * dims.y) + j], end=" ")
        print("")


def _print_solved_board(tiles: Tiles, dims: iVec2D, pairs: Pairs) -> None: ...
