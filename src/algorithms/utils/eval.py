from . import config
from src.algorithms.dfs import JDFSSolver
from src.algorithms.mcmf import JMCMFSolver
from .board_generator import BoardGenerator
from src.algorithms.base import JAlgorithmBase
from src.algorithms.utils.types import Neighbors
from .verifier import print_board, solution_verifier
from src.algorithms.guided_dfs import GuidedJDFSSolver
from .core import absdiff, create_neighbors, calc_avg_cost

solvers: list[JAlgorithmBase] = [
    JDFSSolver(absdiff),
    JMCMFSolver(absdiff),
    GuidedJDFSSolver(absdiff),
]

board_gen: BoardGenerator = BoardGenerator(config.board_sizes)
board_gen.generate(config.costs_range, config.sample_multiplier)

for board, dims in board_gen:
    neighbors: Neighbors = create_neighbors(dims, board, absdiff)

    print_board(board, dims)
    print()

    for solver in solvers:
        solver.solve(board, neighbors, dims)
        solution_verifier(solver.pairs, neighbors)
        print(solver, "avg cost:", calc_avg_cost(board, solver.pairs))
