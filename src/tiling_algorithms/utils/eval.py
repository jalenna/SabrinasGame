import csv
import pandas as pd
import seaborn as sns
from typing import Any
import matplotlib.pyplot as plt
from tiling_algorithms.utils import config
from tiling_algorithms.dfs import JDFSSolver
from tiling_algorithms.mcmf import JMCMFSolver
import tiling_algorithms.ml.config as ml_config
from tiling_algorithms.base import JAlgorithmBase
from tiling_algorithms.utils.types import Neighbors
from tiling_algorithms.guided_dfs import JGuidedJDFSSolver
from tiling_algorithms.utils.verifier import solution_verifier
from tiling_algorithms.utils.board_generator import BoardGenerator
from tiling_algorithms.utils.trackers import JAlgorithmStatsTracker
from tiling_algorithms.utils.core import absdiff, create_neighbors, calc_avg_cost


def evaluate() -> None:
    solvers: list[JAlgorithmBase] = [
        JDFSSolver(absdiff),
        JMCMFSolver(absdiff),
        JGuidedJDFSSolver(
            absdiff, model_path=ml_config.save_path / "JDFSSolver.pt"),
        JGuidedJDFSSolver(
            absdiff, model_path=ml_config.save_path / "JMCMFSolver.pt"),
    ]

    for algorithm in solvers:
        algorithm.tracker = JAlgorithmStatsTracker()

    board_gen: BoardGenerator = BoardGenerator()
    board_gen.generate(config.board_sizes, config.costs_range,
                       config.sample_multiplier)

    print("Evaluating models...")

    with open(config.results_save_path, 'w', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=JAlgorithmStatsTracker.get_csv_headers())
        writer.writeheader()

        for board, dims in board_gen:
            print(f"Running dim: {dims}...")
            neighbors: Neighbors = create_neighbors(dims, board, absdiff)

            trial_results: dict[JAlgorithmBase, list[dict[str, Any]]] = {
                solver: [] for solver in solvers}

            for _ in range(config.eval_trials):
                for solver in solvers:
                    solver.tracker = JAlgorithmStatsTracker()
                    solver.solve(board, neighbors, dims)

                    solution_verifier(solver.pairs, neighbors)

                    solver.tracker.score = calc_avg_cost(board, solver.pairs)
                    trial_results[solver].append(solver.tracker.to_dict())

            for solver, results in trial_results.items():
                solver_name: str = solver.__class__.__name__
                if isinstance(solver, JGuidedJDFSSolver):
                    solver_name += "_" + solver.model_path.stem

                avg_row = {
                    'algorithm_name': solver_name,
                    'steps_forward': sum(r['steps_forward'] for r in results) / config.eval_trials,
                    'steps_backward': sum(r['steps_backward'] for r in results) / config.eval_trials,
                    'total_steps': sum(r['total_steps'] for r in results) / config.eval_trials,
                    'score': sum(r['score'] for r in results) / config.eval_trials,
                    'normal_total_time': sum(r['_total_time_accumulated'] for r in results) / config.eval_trials,
                    'external_time': sum(r['_external_time_accumulated'] for r in results) / config.eval_trials,
                    'grid_size': f"{dims.x},{dims.y}"
                }
                avg_row['total_time'] = avg_row['normal_total_time'] + \
                    avg_row['external_time']
                writer.writerow(avg_row)

    print("Finished writing results to:", config.results_save_path)


def plot_performance_clear(csv_path):
    df = pd.read_csv(csv_path)
    df['total_cells'] = df['grid_size'].apply(
        lambda x: int(x.split(',')[0]) * int(x.split(',')[1]))

    styles = {
        'JDFSSolver': {'marker': 'o', 'linestyle': '-', 'color': 'red'},
        'JMCMFSolver': {'marker': 's', 'linestyle': '--', 'color': 'blue'},
        'JGuidedJDFSSolver_JDFSSolver': {'marker': '^', 'linestyle': ':', 'color': 'green'},
        'JGuidedJDFSSolver_JMCMFSolver': {'marker': 'D', 'linestyle': '-.', 'color': 'orange'}
    }

    _, ax = plt.subplots(figsize=(10, 6))

    for algo in df['algorithm_name'].unique():
        subset = df[df['algorithm_name'] == algo].sort_values('total_cells')
        style = styles.get(algo, {'marker': 'x', 'linestyle': '-'})

        ax.plot(subset['total_cells'], subset['total_time'],
                label=algo, alpha=0.7, linewidth=2, **style)

    ax.set_yscale('log')
    ax.set_title('Comparison of Algorithm Runtime')
    ax.set_xlabel('Total Cells')
    ax.set_ylabel('Total Time (s, log scale)')
    ax.legend(loc='best')
    ax.grid(True, which="both", linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()


def plot_steps_side_by_side(csv_path):
    df = pd.read_csv(csv_path)
    df['total_cells'] = df['grid_size'].apply(
        lambda x: int(x.split(',')[0]) * int(x.split(',')[1]))

    df_dfs = df[df['algorithm_name'].str.contains('DFS')].copy()

    pivot_df = df_dfs.pivot_table(
        index='total_cells',
        columns='algorithm_name',
        values=['steps_forward', 'steps_backward']
    )

    pivot_df.columns = [f"{algo}_{step}" for step, algo in pivot_df.columns]

    ax = pivot_df.plot(kind='bar', figsize=(14, 7), width=0.8)

    ax.set_title(
        f'Forward Steps and Backtracks (Avg. {config.eval_trials} runs)')
    ax.set_xlabel('Total Number of Cells')
    ax.set_ylabel('Number of Steps')
    ax.legend(title="Algorithm & Step Type",
              bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig("./data_out/dfs_steps.eps")


def plot_execution_time(csv_path):
    df = pd.read_csv(csv_path)
    df['total_cells'] = df['grid_size'].apply(
        lambda x: int(x.split(',')[0]) * int(x.split(',')[1]))

    plt.figure(figsize=(10, 6))

    for algo in df['algorithm_name'].unique():
        subset = df[df['algorithm_name'] == algo].sort_values('total_cells')
        plt.plot(subset['total_cells'], subset['total_time'],
                 marker='o', linestyle='-', linewidth=2, label=algo)

    plt.yscale('log')
    plt.title(f'Execution Time x Grid Size (Avg. {config.eval_trials} runs)')
    plt.xlabel('Total Number of Cells')
    plt.ylabel('Total Time (s, log scale)')
    plt.legend()
    plt.grid(True, which="both", linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("./data_out/time.eps")


def plot_solution_costs(csv_path):
    df = pd.read_csv(csv_path)
    df['total_cells'] = df['grid_size'].apply(
        lambda x: int(x.split(',')[0]) * int(x.split(',')[1]))

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='total_cells', y='score', hue='algorithm_name')

    plt.title(f'Solution Costs (Avg. {config.eval_trials} runs)')
    plt.xlabel('Total Number of Cells')
    plt.ylabel('Objective Cost')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("./data_out/costs.eps")


# evaluate()
# plot_execution_time(config.results_save_path)
# plot_solution_costs(config.results_save_path)
# plot_steps_side_by_side(config.results_save_path)
