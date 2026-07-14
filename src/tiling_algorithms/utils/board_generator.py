from random import randint
from tiling_algorithms.utils.types import Boards, Board, ExplicitDims, RoundRobinDims, VariableDims, iVec2D


class BoardGenerator:
    def __init__(self) -> None:
        self.boards: Boards = []

    def generate(self, dims: VariableDims, rand_range: tuple[int, int], extend_samples: int = 1) -> None:

        if isinstance(dims, RoundRobinDims):
            self.rr_generator(dims,
                              rand_range, extend_samples)
        elif isinstance(dims, ExplicitDims):
            self.ex_generator(dims,
                              rand_range, extend_samples)

    def rr_generator(self, dims: RoundRobinDims, rand_range: tuple[int, int], extend_samples: int = 1) -> None:
        widths, heights = dims.widths, dims.heights
        widths *= extend_samples
        heights *= extend_samples

        for width in widths:
            for height in heights:
                self.boards.append(([randint(*rand_range) * 1.
                                    for _ in range(width * height)], iVec2D(width, height)))

    def ex_generator(self, dims: ExplicitDims, rand_range: tuple[int, int], extend_samples: int = 1) -> None:
        complete_dims: list[tuple[int, int]] = dims.dims * extend_samples

        for width, height in complete_dims:
            self.boards.append(([randint(*rand_range) * 1.
                                 for _ in range(width * height)], iVec2D(width, height)))

    def __len__(self):
        return len(self.boards)

    def __getitem__(self, i: int) -> Board:
        return self.boards[i]

    def __setitem__(self, i: int, value: Board):
        self.boards[i] = value
