from manim import *
from typing import override
from collections import defaultdict, deque
from tiling_algorithms.base import JAlgorithmBase
from tiling_algorithms.utils.types import Graph, Neighbors, Tiles, iVec2D, Edge, State

from SabrinasGame.src.tiling_algorithms.utils.core import create_neighbors


class JStateMCMFSolver(JAlgorithmBase):
    def __init__(self, cost_func):
        super().__init__(cost_func)
        self.source_idx: int = 0
        self.sink_idx: int = 0
        self.graph: Graph = defaultdict(list)
        self.history: list[State] = []

    def visual_solve(self, dim: iVec2D, tiles: Tiles, viz_board: VGroup) -> dict[tuple[int, int], Line]:
        neighbors: Neighbors = create_neighbors(dim, tiles, self.cost_func)
        self.solve(tiles, neighbors, dim)

        lines: dict[tuple[int, int], Line] = {}

        for state in self.history:
            u, v = state.pair[0], state.pair[1]
            key = (min(u, v), max(u, v))

            if key not in lines:
                lines[key] = Line(
                    viz_board[u].get_center(),
                    viz_board[v].get_center(),
                    buff=0., color=YELLOW
                )

        return lines

    def clear(self) -> None:
        self._pairs = []
        self.history = []

    @override
    def solve(self, tiles: Tiles, neighbors: Neighbors, dims: iVec2D) -> bool:
        self.tracker.start_timer()
        self.source_idx = len(tiles)
        self.sink_idx = len(tiles) + 1

        self._pairs = [-1] * len(tiles)
        self.graph = defaultdict(list)
        self._create_graph(tiles, neighbors, dims)

        while True:
            distance, parent_node, parent_edge = self._spfa(tiles)

            if distance[self.sink_idx] == float("inf"):
                break

            self.tracker.steps_forward += 1
            self._commit_construction(tiles, dims, parent_node, parent_edge)

        self.tracker.stop_timer()
        return True

    def _spfa(self, tiles: Tiles) -> tuple[list[float], list[int], list[int]]:
        distance: list[float] = [float("inf")] * (len(tiles) + 2)
        parent_node: list[int] = [-1] * (len(tiles) + 2)
        parent_edge: list[int] = [-1] * (len(tiles) + 2)
        queued: list[bool] = [False] * (len(tiles) + 2)

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
        self,
        tiles: Tiles,
        dims: iVec2D,
        parent_node: list[int],
        parent_edge: list[int],
    ) -> None:
        # Walk the augmenting path once, mutate capacities as before, and
        # collect the tile-tile ("pair") edges it crosses, source -> sink order.
        path_edges: list[tuple[int, int]] = []
        current_node: int = self.sink_idx

        while current_node != self.source_idx:
            prev_node: int = parent_node[current_node]
            edge: Edge = self.graph[prev_node][parent_edge[current_node]]
            edge.capacity -= 1
            self.graph[current_node][edge.rev].capacity += 1

            if prev_node < len(tiles) and current_node < len(tiles):
                path_edges.append((prev_node, current_node))

            current_node = prev_node

        path_edges.reverse()  # now in source -> sink order

        removals: list[iVec2D] = []
        additions: list[iVec2D] = []

        for u, v in path_edges:
            if self._is_p_a(u, dims):
                additions.append(iVec2D(u, v))
            else:
                # reverse edge: v is the p_a side
                removals.append(iVec2D(v, u))

        # Removals MUST be applied before additions: an alternating path can
        # steal a tile from its current pair before handing it a new one, and
        # recording it the other way round would corrupt self._pairs mid-walk.
        for a, b in removals:
            self._pairs[a] = -1
            self._pairs[b] = -1
            self.history.append(State(False, iVec2D(a, b)))
            self.tracker.steps_backward += 1

        for a, b in additions:
            self._pairs[a] = b
            self._pairs[b] = a
            self.history.append(State(True, iVec2D(a, b)))

    def _create_graph(self, tiles: Tiles, neighbors: Neighbors, dims: iVec2D) -> None:
        p_a: set[int] = {i for i in range(len(tiles)) if self._is_p_a(i, dims)}
        p_b: set[int] = {i for i in range(
            len(tiles)) if not self._is_p_a(i, dims)}

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

    @staticmethod
    def _is_p_a(idx: int, dims: iVec2D) -> bool:
        return ((idx // dims.x) + (idx % dims.x)) % 2 == 0

    def _add_edge(self, start: int, to: int, cost: float, capacity: int) -> None:
        self.graph[start].append(
            Edge(start, to, len(self.graph[to]), cost, capacity))
        self.graph[to].append(
            Edge(to, start, len(self.graph[start]) - 1, -cost, 0))
