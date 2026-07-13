from typing import Generator
from manim import BLACK, Line, Mobject, RandomColorGenerator
from src.algorithms.utils.core import absdiff, create_neighbors
from src.algorithms.utils.types import Neighbors, Pairs, Tiles, iVec2D


class LinearGreedySolver:
    def __init__(self, color_gen: RandomColorGenerator) -> None:
        self.pairs: Pairs = []
        self.color_gen = color_gen

    def solve(self, dims: iVec2D, viz_board: Mobject, board: Tiles) -> list[Line]:
        self.pairs: Pairs = [-1] * (dims.x * dims.y)
        neighbors: Neighbors = create_neighbors(dims, board, lambda a, b: absdiff(self.color_gen.colors[int(
            board[int(a)])].to_integer(), self.color_gen.colors[int(board[int(b)])].to_integer()))
        lines: list[Line] = []

        for i in range(len(board)):
            if self.pairs[i] > -1:
                continue

            for j in neighbors[i]:
                if self.pairs[j] > -1:
                    continue

                self.pairs[i] = j
                self.pairs[j] = i
                lines.append(Line(
                    viz_board[i].get_center(), viz_board[j].get_center(), buff=0., color=BLACK))
                break
        return lines
