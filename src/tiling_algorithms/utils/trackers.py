from typing import Any
from time import perf_counter
from dataclasses import asdict, dataclass


@dataclass
class JAlgorithmStatsTracker:
    steps_forward: int = 0
    steps_backward: int = 0
    score: float = 0

    @property
    def total_steps(self) -> int: return self.steps_forward + \
        self.steps_backward

    _external_time_accumulated: float = 0
    _external_timer_start: float = 0

    _total_time_accumulated: float = 0
    _timer_start: float = 0

    def start_timer(self) -> None:
        self._timer_start = perf_counter()

    def pause_timer(self) -> None:
        self._total_time_accumulated += perf_counter() - self._timer_start

    def stop_timer(self) -> float:
        self._total_time_accumulated += perf_counter() - self._timer_start
        return self._total_time_accumulated

    def start_external_timer(self) -> None:
        self._external_timer_start = perf_counter()

    def pause_external_timer(self) -> None:
        self._external_time_accumulated += perf_counter() - self._external_timer_start

    def stop_external_timer(self) -> float:
        self._external_time_accumulated += perf_counter() - self._external_timer_start
        return self._external_time_accumulated

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data['total_steps'] = self.total_steps

        keys_to_remove = ['_external_timer_start', '_timer_start']
        for key in keys_to_remove:
            data.pop(key, None)

        return data

    @classmethod
    def get_csv_headers(cls) -> list[str]:
        return [
            "algorithm_name", "steps_forward", "steps_backward",
            "total_steps", "score", "total_time", "normal_total_time", "external_time",
            "grid_size"
        ]


class NoTracker(JAlgorithmStatsTracker):
    ...
