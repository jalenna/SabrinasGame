from typing import Any, override
from manim import BLUE_D, Rectangle
from src.algorithms.utils.types import ExplicitDims, VariableDims
from src.algorithms.utils.board_generator import BoardGenerator


class VizBoardGenerator(BoardGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.viz_boards: list[Rectangle] = []

    @override
    def generate(self, dims: VariableDims, rand_range: tuple[int, int], extend_samples: int = 1) -> None:

        super().generate(dims, rand_range, extend_samples)

        for _, dim in self.boards:
            self.viz_boards.append(
                Rectangle(
                    width=dim.x,
                    height=dim.y,
                    grid_xstep=1.0,
                    grid_ystep=1.0
                ).set_style(stroke_width=2, stroke_color=BLUE_D)
            )
