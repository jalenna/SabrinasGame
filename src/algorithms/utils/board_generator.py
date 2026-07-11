from random import randint
from src.algorithms.utils.types import Tiles, VariableDims, iVec2D


class BoardGenerator:
    def __init__(self, dims: VariableDims) -> None:
        super().__init__()
        self.dims: VariableDims = dims
        self.boards: list[tuple[Tiles, iVec2D]] = []

    def generate(self, rand_range: tuple[int, int], extend_samples: int) -> None:
        widths, heights = self.dims
        widths *= extend_samples
        heights *= extend_samples

        for width in widths:
            for height in heights:
                self.boards.append(([randint(*rand_range)
                                    for _ in range(width * height)], iVec2D(width, height)))

    def __len__(self):
        return len(self.boards)

    def __getitem__(self, i: int) -> tuple[Tiles, iVec2D]:
        return self.boards[i]
