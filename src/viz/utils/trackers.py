from dataclasses import dataclass


@dataclass
class JSlideNumberTracker:
    _current: int = 1
    _total: int = 1
    _prev: int = 0

    @property
    def current(self) -> int:
        return self._current

    @property
    def prev(self) -> int:
        return self._prev

    def update_prev(self) -> None:
        self._prev = self._current

    def has_updated_prev(self) -> bool:
        return self._prev == self._current

    def inc(self) -> None:
        self._prev = self.current
        self._total += 1
        self._current += 1
