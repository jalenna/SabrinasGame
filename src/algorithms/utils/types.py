from dataclasses import dataclass
from collections import namedtuple

iVec2D = namedtuple("IntegerVector2D", ["x", "y"])
iVec3D = namedtuple("IntegerVector3D", ["x", "y", "z"])

type Tiles = list[float]
type Pairs = list[int]
type Neighbors = list[list[int]]
type VariableDims = tuple[list[int], list[int]]


@dataclass
class Edge:
    start: int
    to: int
    rev: int
    cost: float
    capacity: int


type Graph = dict[int, list[Edge]]
