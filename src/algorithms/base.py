"""Base Algorithm Module For All Algorithms"""

from abc import abstractmethod
from src.algorithms.utils.core import CostFunc
from src.algorithms.utils.types import iVec2D, Tiles, Neighbors, Pairs
from src.algorithms.utils.trackers import JAlgorithmStatsTracker


class JAlgorithmBase:
    """TODO"""

    def __init__(self, tracker: JAlgorithmStatsTracker, cost_func: CostFunc):
        self.tracker = tracker
        self.cost_func = cost_func
        self._pairs: Pairs = []

    @abstractmethod
    def solve(self, tiles: Tiles, neighbors: Neighbors, dims: iVec2D) -> Pairs: ...

    @property
    def pairs(self) -> Pairs:
        """Solved pairs"""
        return self._pairs
