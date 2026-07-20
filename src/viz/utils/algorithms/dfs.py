import torch
from manim import *
from pathlib import Path
from tiling_algorithms.dfs import JDFSSolver
import tiling_algorithms.ml.config as ml_config
from tiling_algorithms.guided_dfs import JGuidedJDFSSolver
from tiling_algorithms.utils.core import absdiff, create_neighbors
from tiling_algorithms.utils.types import Tiles, iVec2D, Neighbors


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
                    buff=0., color=YELLOW
                )

        return lines

    def clear(self) -> None:
        self.solver._pairs = []
        self.solver.history = []


class JGuidedDepthSolver:
    def __init__(self, model_path: Path = ml_config.save_path / "JDFSSolver.pt") -> None:
        self.cost_func = absdiff
        self.solver: JGuidedJDFSSolver = JGuidedJDFSSolver(
            self.cost_func, model_path)

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
                    buff=0., color=YELLOW
                )

        return lines

    def pure_solve(self, dim: iVec2D, tiles: Tiles, viz_board: VGroup) -> list[Line]:
        lines: list[Line] = []

        board: torch.Tensor = torch.tensor(
            tiles, dtype=torch.float32).view(1, dim.y, dim.x)
        occupied: torch.Tensor = torch.tensor(
            [0 for _ in range(len(tiles))], dtype=torch.float32).view(1, dim.y, dim.x)

        inp = torch.cat([board, occupied]).unsqueeze(0)

        pairs = self.solver.model(inp).flatten().tolist()

        self.solver._pairs = [int(pair) for pair in pairs]

        for a, b in enumerate(self.solver._pairs[:len(tiles)]):
            if b > len(tiles):
                viz_board[a].add(Cross())
                continue

            lines.append(Line(
                viz_board[a].get_center(), viz_board[b].get_center(), buff=0., color=BLACK))

        return lines
