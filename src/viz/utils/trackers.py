from dataclasses import dataclass


@dataclass
class JSlideNumberingTracker:
    _current: int
    _total: int

    @property
    def current(self) -> int:
        return self._current
    
    def inc(self) -> None:
        self._total += 1
        self._current += 1