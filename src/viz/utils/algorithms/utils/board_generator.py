from manim import *
from typing import Optional
from tiling_algorithms.utils.types import VariableDims
from SabrinasGame.src.tiling_algorithms.utils.types import Tiles
from tiling_algorithms.utils.board_generator import BoardGenerator


class VisualBoardGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.data_generator: BoardGenerator = BoardGenerator()
        self.visual_boards: list[VGroup] = []

    def generate(self, dims: VariableDims, rand_range: tuple[int, int], tiles: Optional[Tiles] = None, label: bool = True, extend_samples: int = 1) -> None:
        start_index: int = len(self.data_generator.boards)
        self.data_generator.generate(dims, rand_range, extend_samples)
        end_index: int = len(self.data_generator.boards)

        if tiles and dims.__class__.__name__ == "ExplicitDims":
            self.data_generator.boards[-1] = tiles, dims.dims[0]

        for i in range(start_index, end_index):
            data_board, dim = self.data_generator.boards[i]
            board: VGroup = VGroup()
            for cell in data_board:
                square: Square = Square(1)
                if label:
                    square.add(Text(str(int(cell))))
                board.add(square)
            board.arrange_in_grid(dim.y, dim.x, buff=0.)
            self.visual_boards.append(board)

    def clear(self) -> None:
        self.visual_boards = []
        self.data_generator.boards = []
