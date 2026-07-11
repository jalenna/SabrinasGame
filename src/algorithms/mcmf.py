"""
Min Cost Flow Solver Module
"""

from typing import override
from collections import defaultdict, deque
from src.algorithms.base import JAlgorithmBase
from src.algorithms.utils.types import Graph, Neighbors, Tiles, iVec2D, Edge


class MCMFSolver(JAlgorithmBase):
    """TODO"""

    def __init__(self, tracker, cost_func):
        super().__init__(tracker, cost_func)
        self.source_idx: int = 0
        self.sink_idx: int = 0
        self.graph: Graph = defaultdict[Graph](list)

    @override
    def solve(self, tiles: Tiles, neighbors: Neighbors, dims: iVec2D) -> bool:
        self.source_idx = len(tiles)
        self.sink_idx = len(tiles) + 1

        self.graph = defaultdict[Graph](list)
        self._create_graph(tiles, neighbors, dims)

        while True:
            distance, parent_node, parent_edge = self._spfa(tiles)

            if distance[self.sink_idx] == float("inf"):
                break

            self._commit_construction(parent_node, parent_edge)

        self._reconstruct(tiles, dims)

    def _spfa(self, tiles: Tiles) -> tuple[list[float], list[int], list[int]]:
        distance: list[float] = [float("inf")] * len(tiles + 2)
        parent_node: list[int] = [-1] * len(tiles + 2)
        parent_edge: list[int] = [-1] * len(tiles + 2)
        queued: list[bool] = [False] * len(tiles + 2)

        distance[self.source_idx] = 0.0

        queue: deque[int] = deque([self.source_idx])

        while queue:
            current_node: int = queue.popleft()
            queued[current_node] = False

            for i, edge in enumerate(self.graph[current_node]):
                current_distance: float = distance[current_node] + edge.cost
                if edge.capacity > 0 and current_distance < distance[edge.to]:
                    distance[edge.to] = current_distance
                    parent_node[edge.to] = current_node
                    parent_edge[edge.to] = i

                    if not queued[edge.to]:
                        queue.append(edge.to)
                        queued[edge.to] = True

        return distance, parent_node, parent_edge

    def _commit_construction(
        self, parent_node: list[int], parent_edge: list[int]
    ) -> None:
        current_node: int = self.sink_idx

        while current_node != self.source_idx:
            prev_node: int = parent_node[current_node]
            edge: Edge = self.graph[prev_node][parent_edge[current_node]]
            edge.capacity -= 1
            self.graph[current_node][edge.rev].capacity += 1
            current_node = prev_node

    def _reconstruct(self, tiles: Tiles, dims: iVec2D) -> None:
        self._pairs = [-1] * len(tiles)
        p_a: set[int] = {
            i for i in range(len(tiles)) if ((i // dims.x) + (i % dims.x)) % 2 == 0
        }
        for a in p_a:
            for edge in self.graph[a]:
                if edge.capacity == 0 and edge.to < len(tiles):
                    self._pairs[a] = edge.to
                    self._pairs[edge.to] = a

    def _create_graph(self, tiles: Tiles, neighbors: Neighbors, dims: iVec2D) -> None:

        p_a: set[int] = {
            i for i in range(len(tiles)) if ((i // dims.x) + (i % dims.x)) % 2 == 0
        }
        p_b: set[int] = {
            i for i in range(len(tiles)) if ((i // dims.x) + (i % dims.x)) % 2 != 0
        }

        for a in p_a:
            self._add_edge(start=self.source_idx, to=a, capacity=1, cost=0)

        for b in p_b:
            self._add_edge(start=b, to=self.sink_idx, capacity=1, cost=0)

        for a in p_a:
            for b in neighbors[a]:
                if b in p_b:
                    self._add_edge(
                        start=a,
                        to=b,
                        capacity=1,
                        cost=self.cost_func(tiles[a], tiles[b]),
                    )

    def _add_edge(self, start: int, to: int, cost: int, capacity: int) -> None:
        self.graph[start].append(Edge(start, to, len(self.graph[to]), cost, capacity))
        self.graph[to].append(Edge(to, start, len(self.graph[start]) - 1, -cost, 0))
