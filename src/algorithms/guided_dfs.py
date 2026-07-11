import torch
import numpy as np
from .ml.cnn import CNN
from typing import override
from algorithms.base import JAlgorithmBase
from algorithms.utils.trackers import JAlgorithmStatsTracker
from algorithms.utils.types import Neighbors, Pairs, iVec2D, Tiles


class CNNGuidedDFS(JAlgorithmBase):
    def __init__(self, model_path: str, tracker: JAlgorithmStatsTracker):
        super.__init__(tracker)

        self.model = CNN(out_channels=1)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    @override
    def solve(self, tiles: Tiles, neighbors: Neighbors, dims: iVec2D) -> list[int]:
        board_size: int = dims[0] * dims[1]
        self._required_tiles: int = board_size // 2
        self._curr_num_tiles: int = 0
        self.pairs: Pairs = [-1 for _ in range(board_size)]
        self.neighbors: Neighbors = neighbors

        self.tracker.steps_backward = 0
        self.tracker.steps_forward = 0

        initial_pairs = np.full(dims, -1, dtype=np.float32)
        input_tensor = torch.tensor(
            np.stack([tiles, initial_pairs]), dtype=torch.float32
        ).unsqueeze(0)

        with torch.no_grad():
            raw_output = self.model(input_tensor)

            self.predictions = raw_output[0].numpy()

        return self._dfs_guided(dims)

    def _dfs_guided(
        self,
        dims: iVec2D,
    ) -> bool:
        if self._required_tiles == self._curr_num_tiles:
            return True

        start: int = -1

        for i, pair in enumerate(self.pairs):
            if pair == -1:
                start = i
                break

        if start == -1:
            return False

        self.tracker.steps_forward += 1

        width, _ = dims
        r, c = start // width, start % width

        predicted_partner_idx = self.predictions[r, c]

        sorted_neighbors: list[int] = sorted(
            self.neighbors[start], key=lambda x: abs(x - predicted_partner_idx)
        )

        for neighbor in sorted_neighbors:
            if self.pairs[neighbor] > -1:
                continue

            self.pairs[start] = neighbor
            self.pairs[neighbor] = start
            self._curr_num_tiles += 1

            if self._dfs_guided(dims):
                return True

            self.pairs[neighbor] = -1
            self.pairs[start] = -1
            self._curr_num_tiles -= 1
            self.tracker.steps_backward += 1

        return False
