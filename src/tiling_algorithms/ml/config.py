from pathlib import Path
from src.algorithms.dfs import JDFSSolver
from src.algorithms.mcmf import JMCMFSolver
from src.algorithms.utils.core import absdiff
from src.algorithms.base import JAlgorithmBase
from src.algorithms.utils.types import RoundRobinDims

save_path: Path = Path("models/checkpoints/cnn/")

epochs: int = 1000
log_steps: int = 200
learn_rate: float = 0.001

board_sizes: RoundRobinDims = RoundRobinDims(
    [4, 6, 8, 10, 12, 14, 16],
    [4, 6, 8, 10, 12, 14, 16]
)
costs_range: tuple[int, int] = (1, 20)
sample_multiplier: int = 1

algorithms: list[JAlgorithmBase] = [
    JMCMFSolver(absdiff),
    JDFSSolver(absdiff),
]
