from typing import Callable, Optional
from dataclasses import dataclass
from src.algorithms.utils.types import Neighbors, Pairs, Tiles, iVec2D


@dataclass
class JBoardParams:
    """TODO"""

    width: int
    height: int
    generatable_dims: Optional[list[list[int], list[int]]]
    costs_range: Optional[iVec2D]


type CostFunc = Callable[[float, float], float]


def create_neighbors(
    width: int, height: int, tiles: Tiles, cost_func: CostFunc
) -> Neighbors:
    neighbors: Neighbors = []

    for i in range(width * height):
        row: int = i // width
        col: int = i % width
        current_cell: list[int] = []

        # Left
        if col > 0:
            current_cell.append(i - 1)
        # Right
        if col + 1 < width:
            current_cell.append(i + 1)
        # Up
        if row > 0:
            current_cell.append(i - width)
        # Down
        if row + 1 < height:
            current_cell.append(i + width)

        current_cell.sort(key=lambda x, i=i: cost_func(tiles[i], tiles[x]))
        neighbors.append(current_cell)

    return neighbors


def calc_avg_cost(tiles: Tiles, pairs: Pairs) -> float:
    avg_cost: float = 0.0
    for tile, cost in enumerate(tiles):
        if pairs[tile] > tile:
            avg_cost += abs(tiles[pairs[tile]] - cost)

    return avg_cost / len(pairs)


def absdiff(a: float, b: float) -> float:
    return abs(a - b)
