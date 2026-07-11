import torch
from typing import override
from src.algorithms.ml.cnn import CNN
import src.algorithms.ml.config as config
from src.algorithms.base import JAlgorithmBase
from src.algorithms.utils.types import Neighbors, Tiles, iVec2D


class GuidedJDFSSolver(JAlgorithmBase):
    def __init__(self, cost_func):
        super().__init__(cost_func)
        self._required_tiles: int = 0
        self._curr_num_tiles: int = 0
        self.neighbors: Neighbors = []
        self.tiles: Tiles = []
        self.dims: iVec2D = iVec2D(0, 0)
        self.model: CNN = CNN()

    @override
    def solve(self, tiles: Tiles, neighbors: Neighbors, dims: iVec2D) -> bool:
        board_size: int = dims.x * dims.y
        self._required_tiles = board_size // 2
        self._curr_num_tiles = 0
        self._pairs = [-1] * len(tiles)
        self.neighbors = neighbors
        self.tiles = tiles
        self.dims = dims
        self._load_model()

        return self._solve()

    def _solve(self) -> bool:
        if self._required_tiles == self._curr_num_tiles:
            return True

        start: int = -1
        for i, pair in enumerate(self._pairs):
            if pair == -1:
                start = i
                break

        if start == -1:
            return False

        self.tracker.steps_forward += 1

        neighbors = self._guide(start)
        for neighbor in neighbors:
            if self._pairs[neighbor] > -1:
                continue

            self._pairs[start] = neighbor
            self._pairs[neighbor] = start
            self._curr_num_tiles += 1

            if self._solve():
                return True

            self._pairs[neighbor] = -1
            self._pairs[start] = -1
            self._curr_num_tiles -= 1
            self.tracker.steps_backward += 1

        return False

    def _get_model_input(self) -> torch.Tensor:
        board: torch.Tensor = torch.tensor(
            self.tiles, dtype=torch.float32).view(1, self.dims.y, self.dims.x)
        occupied: torch.Tensor = torch.tensor(
            [1. if p == -1 else 0. for p in self._pairs], dtype=torch.float32).view(1, self.dims.y, self.dims.x)

        return torch.cat([board, occupied]).unsqueeze(0)

    def _guide(self, current: int) -> list[int]:
        input_data = self._get_model_input()

        with torch.no_grad():
            logits = self.model(input_data)

        neighbors: list[int] = self.neighbors[current]

        return sorted(neighbors, key=lambda x: logits[0, x].item(), reverse=True)

    def _load_model(self) -> None:
        self.model = CNN()
        self.model.load_state_dict(torch.load(
            config.save_path, weights_only=True))
        self.model.eval()
