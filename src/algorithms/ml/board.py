import numpy as np
import random
import networkx as nx
from typing import cast


class BoardGenerator:
    def __init__(self, size_options: list[int] = [4, 6, 8, 10]):
        self.size_options = size_options

    def generate_board(self) -> np.ndarray:
        H = random.choice(self.size_options)
        W = random.choice(self.size_options)
        return np.random.randint(1, 21, size=(H, W)).astype(np.float32)

    def calc_avg_cost(self, costs: np.ndarray, pairs: list[int]) -> float:
        avg_cost = 0
        for i in range(len(pairs)):
            pair: int = cast(int, pairs[i])
            if pair > i:
                a: int = cast(int, costs[i])
                b: int = cast(int, costs[pair])
                avg_cost += abs(a - b)

        return avg_cost / (len(costs) * .5)

    def generate_ml_sample(self) -> tuple[np.ndarray, np.ndarray, float]:
        H = random.choice(self.size_options)
        W = random.choice(self.size_options)

        costs_board = np.random.randint(1, 21, size=(H, W)).astype(np.float32)
        flat_costs = costs_board.flatten()
        num_cells = H * W

        G = nx.Graph()
        for r in range(H):
            for c in range(W):
                current_idx = r * W + c
                if c + 1 < W:
                    right_idx = r * W + (c + 1)
                    G.add_edge(current_idx, right_idx, weight=abs(
                        flat_costs[current_idx] - flat_costs[right_idx]))
                if r + 1 < H:
                    down_idx = (r + 1) * W + c
                    G.add_edge(current_idx, down_idx, weight=abs(
                        flat_costs[current_idx] - flat_costs[down_idx]))

        # Run Blossom Algorithm
        optimal_matching = nx.algorithms.min_weight_matching(G)

        # Reconstruct the pairs array
        pairs = [-1] * num_cells
        total_diff = 0.0
        for u, v in optimal_matching:
            pairs[u] = v
            pairs[v] = u
            total_diff += abs(flat_costs[u] - flat_costs[v])

        best_score = total_diff / (num_cells / 2)

        initial_pairs_grid = np.full((H, W), -1, dtype=np.float32)
        input_tensor = np.stack([costs_board, initial_pairs_grid], axis=0)
        target_tensor = np.array(pairs, dtype=np.float32).reshape(H, W)

        return input_tensor, target_tensor, cast(float, best_score)

    def print_board_pair(self, costs_grid: np.ndarray, pairs_grid: np.ndarray):
        H, W = costs_grid.shape
        print(
            f"\n--- Costs Grid ({H}x{W}) ---       --- Pairs Grid ({H}x{W}) ---")
        for r in range(H):
            cost_row = " ".join(
                f"{int(costs_grid[r, c]):2d}" for c in range(W))
            pair_row = " ".join(
                f"{int(pairs_grid[r, c]):2d}" if pairs_grid[r, c] != -1 else " ." for c in range(W))
            print(f"| {cost_row} |       | {pair_row} |")
        print("-" * (W * 7 + 30))

    def print_board(self, costs_grid: np.ndarray):
        H, W = costs_grid.shape
        print(
            f"\n--- Costs Grid ({H}x{W}) ---")
        for r in range(H):
            cost_row = " ".join(
                f"{int(costs_grid[r, c]):2d}" for c in range(W))
            print(f"| {cost_row} |")
        print("-" * (W * 7 + 30))
