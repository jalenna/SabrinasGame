import pandas as pd
import tiling_algorithms.utils.config as config


def steps_for_2d_plot() -> dict[str, dict[str, list[int]]]:
    df = pd.read_csv(config.results_save_path)

    def get_num_cells(size_str):
        w, h = map(int, size_str.split(','))
        return w * h

    df['num_cells'] = df['grid_size'].apply(get_num_cells)

    pivot_df = df.pivot_table(
        index=['num_cells'],
        columns='algorithm_name',
        values=['steps_forward', 'steps_backward']
    ).sort_index()

    def get_aligned_data(algo_name, direction):
        col = f'steps_{direction}'
        return pivot_df[(col, algo_name)].fillna(0).astype(int).tolist()

    num_cells = pivot_df.index.tolist()

    return {
        "forward": {
            "DFSSolver": get_aligned_data("JDFSSolver", "forward"),
            "GuidedJDFSSolver": get_aligned_data("JGuidedJDFSSolver_JDFSSolver", "forward"),
            "num_cells": num_cells
        },
        "backward": {
            "DFSSolver": get_aligned_data("JDFSSolver", "backward"),
            "GuidedJDFSSolver": get_aligned_data("JGuidedJDFSSolver_JDFSSolver", "backward"),
            "num_cells": num_cells
        }
    }


def scores_for_2d_plot() -> dict[str, list[float]]:
    df = pd.read_csv(config.results_save_path)

    def get_num_cells(size_str):
        w, h = map(int, size_str.split(','))
        return w * h

    df['num_cells'] = df['grid_size'].apply(get_num_cells)

    pivot_df = df.pivot_table(
        index=['num_cells'],
        columns='algorithm_name',
        values=["score"]
    ).sort_index()

    def get_aligned_data(algo_name):
        return pivot_df[('score', algo_name)].fillna(0).astype(float).tolist()

    num_cells: list[float] = pivot_df.index.tolist()

    return {
        "DFSSolver": get_aligned_data("JDFSSolver"),
        "GuidedJDFSSolver": get_aligned_data("JGuidedJDFSSolver_JDFSSolver"),
        "num_cells": num_cells

    }
