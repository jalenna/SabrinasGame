from abc import abstractmethod
from dataclasses import dataclass
from typing import NamedTuple, override


class iVec2D(NamedTuple):
    x: int
    y: int


class iVec3D(NamedTuple):
    x: int
    y: int
    z: int


type Tiles = list[float]
type Pairs = list[int]
type Neighbors = list[list[int]]
type Board = tuple[Tiles, iVec2D]
type Boards = list[Board]


class VariableDims:
    @abstractmethod
    def max_dims(self) -> iVec2D: ...


@dataclass
class RoundRobinDims(VariableDims):
    widths: list[int]
    heights: list[int]

    @override
    def max_dims(self) -> iVec2D:
        return iVec2D(max(self.widths), max(self.heights))


@dataclass
class ExplicitDims(VariableDims):
    dims: list[tuple[int, int]]

    @override
    def max_dims(self) -> iVec2D:
        return iVec2D(*max(self.dims, key=lambda x: x[0] * x[1]))


@dataclass
class Edge:
    start: int
    to: int
    rev: int
    cost: float
    capacity: int


type Graph = dict[int, list[Edge]]


@dataclass
class State:
    added: bool
    pair: iVec2D
