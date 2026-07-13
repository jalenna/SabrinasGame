from dataclasses import dataclass


@dataclass
class JSlideNumberTracker:
    _current: int = 1
    _total: int = 1

    @property
    def current(self) -> int:
        return self._current

    def inc(self) -> None:
        self._total += 1
        self._current += 1
