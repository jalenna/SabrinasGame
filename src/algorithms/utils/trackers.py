from dataclasses import dataclass

@dataclass
class JAlgorithmStatsTracker:
    steps_forward: int
    steps_backward: int
    score: float

    @property
    def total_steps(self) -> int: return self.steps_forward + self.steps_backward
