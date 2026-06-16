import torch
import numpy as np
from .cnn import CNN


class CNNGuidedDFS:
    def __init__(self, model_path):
        self.model = CNN(out_channels=1)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

        self.back = 0
        self.forw = 0
        self._required_tiles = 0
        self._curr_num_tiles = 0

    def solve(self, costs_board: np.ndarray) -> list[int]:
        H, W = costs_board.shape
        pairs = [-1] * (H * W)

        self.back = 0
        self.forw = 0
        self._required_tiles = (H * W) // 2
        self._curr_num_tiles = 0

        initial_pairs = np.full((H, W), -1, dtype=np.float32)
        input_tensor = torch.tensor(
            np.stack([costs_board, initial_pairs]), dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            raw_output = self.model(input_tensor)

            predictions = raw_output[0].numpy()

        self._dfs_guided(pairs, predictions, H, W)
        return pairs

    def get_physical_neighbors(self, idx: int, H: int, W: int) -> list[int]:
        r, c = idx // W, idx % W
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                neighbors.append(nr * W + nc)
        return neighbors

    def _dfs_guided(self, pairs: list[int], cnn_predictions: np.ndarray, H: int, W: int) -> bool:
        if self._required_tiles == self._curr_num_tiles:
            return True

        start = -1
        for i in range(len(pairs)):
            if pairs[i] == -1:
                start = i
                break

        if start == -1:
            return False

        self.forw += 1
        r, c = start // W, start % W

        neighbors = self.get_physical_neighbors(start, H, W)

        predicted_partner_idx = cnn_predictions[r, c]
        neighbors.sort(key=lambda n_idx: abs(n_idx - predicted_partner_idx))

        for neighbor_idx in neighbors:
            if pairs[neighbor_idx] != -1:
                continue

            pairs[start] = neighbor_idx
            pairs[neighbor_idx] = start
            self._curr_num_tiles += 1

            if self._dfs_guided(pairs, cnn_predictions, H, W):
                return True

            pairs[start] = -1
            pairs[neighbor_idx] = -1
            self._curr_num_tiles -= 1
            self.back += 1

        return False
