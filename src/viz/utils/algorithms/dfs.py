from manim import BLACK, Line, VGroup
from src.algorithms.dfs import JDFSSolver
from src.algorithms.guided_dfs import JGuidedJDFSSolver
from src.algorithms.utils.core import absdiff, create_neighbors
from src.algorithms.utils.types import Tiles, iVec2D, Neighbors


class JDepthSolver:
    def __init__(self) -> None:
        self.cost_func = absdiff
        self.solver: JDFSSolver = JDFSSolver(self.cost_func)

    def solve(self, dim: iVec2D, tiles: Tiles, viz_board: VGroup) -> dict[tuple[int, int], Line]:
        neighbors: Neighbors = create_neighbors(dim, tiles, self.cost_func)
        self.solver.solve(tiles, neighbors, dim)

        lines: dict[tuple[int, int], Line] = {}

        for state in self.solver.history:
            u, v = state.pair[0], state.pair[1]
            key = (min(u, v), max(u, v))

            if key not in lines:
                lines[key] = Line(
                    viz_board[u].get_center(),
                    viz_board[v].get_center(),
                    buff=0., color=BLACK
                )

        return lines


class JGuidedDepthSolver:
    def __init__(self) -> None:
        self.cost_func = absdiff
        self.solver: JGuidedJDFSSolver = JGuidedJDFSSolver(self.cost_func)

    def solve(self, dim: iVec2D, tiles: Tiles, viz_board: VGroup) -> dict[tuple[int, int], Line]:
        neighbors: Neighbors = create_neighbors(dim, tiles, self.cost_func)
        self.solver.solve(tiles, neighbors, dim)

        lines: dict[tuple[int, int], Line] = {}

        for state in self.solver.history:
            u, v = state.pair[0], state.pair[1]
            key = (min(u, v), max(u, v))

            if key not in lines:
                lines[key] = Line(
                    viz_board[u].get_center(),
                    viz_board[v].get_center(),
                    buff=0., color=BLACK
                )

        return lines
