from dfs import DFS
from ml.board import BoardGenerator
from ml.guided_dfs import CNNGuidedDFS
from ml.config import save_path, board_size_options
from typing import cast

guided_dfs: CNNGuidedDFS = CNNGuidedDFS(save_path)
dfs: DFS = DFS()

data_gen = BoardGenerator(board_size_options)

dfs_avg: dict[str, float | int] = {
    "cost": 0,
    "forward": 0,
    "backward": 0,
}
guided_avg: dict[str, float | int] = {
    "cost": 0,
    "forward": 0,
    "backward": 0,
}

iterations: int = 10000

print("Gathering results...")
for i in range(iterations):
    board = data_gen.generate_board()
    w, h = board.shape

    flattened_board = board.flatten()

    dfs.solve(w, h, flattened_board)
    guided_dfs_pairs = guided_dfs.solve(board)

    dfs_cost: float = data_gen.calc_avg_cost(
        flattened_board, cast(list[int], dfs.pairs))
    dfs_avg["cost"] += dfs_cost
    dfs_avg["forward"] += dfs.forw
    dfs_avg["backward"] += dfs.back

    guided_cost: float = data_gen.calc_avg_cost(
        flattened_board, guided_dfs_pairs)
    guided_avg["cost"] += guided_cost
    guided_avg["forward"] += guided_dfs.forw
    guided_avg["backward"] += guided_dfs.back

    print(f"\rProgress: {i + 1}/{iterations}", end="", flush=True)

print("\nFinished gathering results")

dfs_avg["cost"] /= iterations
dfs_avg["forward"] /= iterations
dfs_avg["backward"] /= iterations
guided_avg["cost"] /= iterations
guided_avg["forward"] /= iterations
guided_avg["backward"] /= iterations


print("Saving")

results_path: str = "dfs_vs_guided.csv"

with open(results_path, "w+") as f:
    f.write("measure,avg_dfs,avg_guided\n")
    f.write(f"cost,{dfs_avg["cost"]:.3f},{guided_avg["cost"]:.3f}\n")
    f.write(f"forward,{dfs_avg["forward"]:.3f},{guided_avg["forward"]:.3f}\n")
    f.write(
        f"backward,{dfs_avg["backward"]:.3f},{guided_avg["backward"]:.3f}\n")

print(f"Done! Saved to {results_path}")
