from typing import Optional
from src.algorithms.base import Neighbors
from src.algorithms.utils.types import Pairs, Tiles, iVec2D


def solution_verifier(
    pairs: Pairs, neighbors: Neighbors, required_num_tiles: int
) -> bool:
    if len(pairs) != required_num_tiles:
        return False

    for a in range(required_num_tiles):
        b = pairs[a]

        if a == b:
            return False

        # a -> b, b <- a
        if pairs[b] != a:
            return False

        if b not in neighbors[a]:
            return False

    return True


def print_board(tiles: Tiles, dims: iVec2D, pairs: Optional[Pairs] = None) -> None:
    if pairs:
        return _print_solved_board(tiles, dims, pairs)

    for i in range(dims[0]):
        for j in range(dims[1]):
            print(tiles[(i * j) + j], end=" ")
        print("")


def _print_solved_board(tiles: Tiles, dims: iVec2D, pairs: Pairs) -> None: ...
