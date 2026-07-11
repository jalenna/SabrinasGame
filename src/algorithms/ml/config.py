from pathlib import Path
from src.algorithms.utils.types import VariableDims

save_path: Path = Path("models/checkpoints/tiler/cnn.pt")

epochs: int = 100
log_steps: int = 200
learn_rate: float = 0.001

board_sizes: VariableDims = (
    [4, 6, 8],
    [4, 6, 8]
)
costs_range: tuple[int, int] = (1, 10)
sample_multiplier: int = 1
