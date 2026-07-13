import torch
from . import config
from random import randint
from typing import override
from torch.utils.data import Dataset
from src.algorithms.mcmf import JMCMFSolver
from src.algorithms.utils.core import absdiff, create_neighbors
from src.algorithms.utils.types import ExplicitDims, Neighbors, RoundRobinDims, Tiles, VariableDims, Pairs, iVec2D


class BoardMLTrainData(Dataset):
    def __init__(self) -> None:
        super().__init__()
        self.boards: list[torch.Tensor] = []
        self.solutions: list[torch.Tensor] = []
        self._solver: JMCMFSolver = JMCMFSolver(absdiff)

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
                board: Tiles = [randint(*rand_range)
                                for _ in range(width * height)]
                self.boards.append(torch.Tensor(board).view(1, height, width))
                self.solutions.append(torch.Tensor(self._solve(
                    board, iVec2D(width, height))))

    def ex_generator(self, dims: ExplicitDims, rand_range: tuple[int, int], extend_samples: int = 1) -> None:
        complete_dims: list[tuple[int, int]] = dims.dims * extend_samples

        for width, height in complete_dims:
            board: Tiles = [randint(*rand_range)
                            for _ in range(width * height)]
            self.boards.append(torch.Tensor(board).view(1, height, width))
            self.solutions.append(torch.Tensor(self._solve(
                board, iVec2D(width, height))))

    def _solve(self, board: Tiles, dims: iVec2D) -> Pairs:
        neighbors: Neighbors = create_neighbors(dims, board, absdiff)
        self._solver(board, neighbors, dims)
        return self._solver.pairs

    def __len__(self):
        return len(self.boards)

    @override
    def __getitem__(self, index) -> tuple[torch.Tensor, torch.Tensor]:
        board = self.boards[index]
        mask = torch.ones_like(board)
        input_tensor = torch.cat([board, mask], dim=0)

        solution = self.solutions[index].view(-1)  # Flatten
        w, h = config.board_sizes.max_dims()
        max_size: int = w * h
        padded_solution = torch.zeros(max_size, dtype=torch.float32)
        padded_solution[:solution.size(0)] = solution

        return input_tensor, padded_solution
