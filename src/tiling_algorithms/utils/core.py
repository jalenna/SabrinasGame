from typing import Callable
from src.algorithms.utils.types import Neighbors, Pairs, Tiles, iVec2D


type CostFunc = Callable[[float, float], float]


def create_neighbors(dims: iVec2D, tiles: Tiles, cost_func: CostFunc
                     ) -> Neighbors:
    neighbors: Neighbors = []

    for i in range(dims.x * dims.y):
        row: int = i // dims.x
        col: int = i % dims.x
        current_cell: list[int] = []

        # Left
        if col > 0:
            current_cell.append(i - 1)
        # Right
        if col + 1 < dims.x:
            current_cell.append(i + 1)
        # Up
        if row > 0:
            current_cell.append(i - dims.x)
        # Down
        if row + 1 < dims.y:
            current_cell.append(i + dims.x)

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


def is_valid_board_size(dim: iVec2D) -> bool:
    return dim.x * dim.y % 2 == 0
