from abc import abstractmethod
from tiling_algorithms.utils.core import CostFunc
from tiling_algorithms.utils.types import iVec2D, Tiles, Neighbors, Pairs
from tiling_algorithms.utils.trackers import JAlgorithmStatsTracker, NoTracker


class JAlgorithmBase:
    def __init__(self, cost_func: CostFunc, tracker: JAlgorithmStatsTracker = NoTracker(0, 0, 0)):
        self.tracker = tracker
        self.cost_func = cost_func
        self._pairs: Pairs = []

    @abstractmethod
    def solve(self, tiles: Tiles, neighbors: Neighbors,
              dims: iVec2D) -> bool: ...

    def __call__(self, tiles: Tiles, neighbors: Neighbors, dims: iVec2D) -> bool:
        return self.solve(tiles, neighbors, dims)

    @property
    def pairs(self) -> Pairs:
        """Solved pairs"""
        return self._pairs
