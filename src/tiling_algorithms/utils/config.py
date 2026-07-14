from pathlib import Path
from tiling_algorithms.utils.types import RoundRobinDims

results_save_path: Path = Path("data_out/results.csv")

board_sizes: RoundRobinDims = RoundRobinDims(
    [4, 6, 8, 10, 12, 14, 16],
    [4, 6, 8, 10, 12, 14, 16]
)

costs_range: tuple[int, int] = (1, 20)

sample_multiplier: int = 1

eval_trials: int = 100
