# import pandas as pd
# import tiling_algorithms.utils.config as config


# def _load_grid_df() -> pd.DataFrame:
#     df = pd.read_csv(config.results_save_path)

#     def parse_grid_size(size_str):
#         w, h = map(int, size_str.split(','))
#         return w, h

#     parsed = df['grid_size'].apply(parse_grid_size)
#     df['grid_w'] = parsed.apply(lambda t: t[0])
#     df['grid_h'] = parsed.apply(lambda t: t[1])
#     df['num_cells'] = df['grid_w'] * df['grid_h']
#     return df


# def _build_pivot(df: pd.DataFrame, values: list[str]) -> pd.DataFrame:
#     pivot_df = df.pivot_table(
#         # CHANGED: Put grid_w first so sort_index() orders by width primarily
#         index=['grid_w', 'grid_h', 'num_cells'],
#         columns='algorithm_name',
#         values=values,
#         aggfunc='mean',  # averages duplicate runs of the same algo+grid_size; NaNs stay NaN, not 0
#     )
#     return pivot_df.sort_index()  # sorts by grid_w, then grid_h, then num_cells


# def _get_aligned(pivot_df: pd.DataFrame, col: str, algo_name: str, cast) -> list:
#     key = (col, algo_name)
#     if key not in pivot_df.columns:
#         # algorithm never appears for this metric at all
#         return [None] * len(pivot_df)
#     series = pivot_df[key]
#     return [cast(v) if pd.notna(v) else None for v in series]


# def steps_for_2d_plot() -> dict:
#     df = _load_grid_df()
#     pivot_df = _build_pivot(df, values=['steps_forward', 'steps_backward'])

#     def get_aligned_data(algo_name, direction):
#         return _get_aligned(pivot_df, f'steps_{direction}', algo_name, int)

#     # CHANGED: Unpack the index tuple to match the new ['grid_w', 'grid_h', 'num_cells'] order
#     grid_sizes = [f'{w},{h}' for w, h, _ in pivot_df.index]
#     num_cells = [n for _, _, n in pivot_df.index]

#     return {
#         "forward": {
#             "DFSSolver": {
#                 "steps": get_aligned_data("JDFSSolver", "forward"),
#                 "total_time": get_aligned_data("JDFSSolver", "total_time"),
#                 "normal_time": None,
#                 "external_time": None,
#                 "score": get_aligned_data("JDFSSolver", "score"),
#             },
#             "GuidedDFSSolver": {
#                 "steps": get_aligned_data("JGuidedJDFSSolver_JDFSSolver", "forward"),
#                 "total_time": get_aligned_data("JGuidedJDFSSolver_JDFSSolver", "total_time"),
#                 "normal_time": get_aligned_data("JGuidedJDFSSolver_JDFSSolver", "normal_time"),
#                 "external_time": get_aligned_data("JGuidedJDFSSolver_JDFSSolver", "external_time"),
#                 "score": get_aligned_data("JGuidedJDFSSolver_JDFSSolver", "score"),
#             },
#             "GuidedMCMFSolver": {
#                 "steps": get_aligned_data("JGuidedJDFSSolver_JMCMFSolver", "forward"),
#                 "total_time": get_aligned_data("JGuidedJDFSSolver_JMCMFSolver", "total_time"),
#                 "normal_time": get_aligned_data("JGuidedJDFSSolver_JMCMFSolver", "normal_time"),
#                 "external_time": get_aligned_data("JGuidedJDFSSolver_JMCMFSolver", "external_time"),
#                 "score": get_aligned_data("JGuidedJDFSSolver_JMCMFSolver", "score"),
#             },
#             "MCMFSolver": {
#                 "steps": get_aligned_data("JMCMFSolver", "forward"),
#                 "total_time": get_aligned_data("JMCMFSolver", "total_time"),
#                 "normal_time": None,
#                 "external_time": None,
#                 "score": get_aligned_data("JMCMFSolver", "score"),
#             },
#         },
#         "backward": {
#             "DFSSolver": {
#                 "steps": get_aligned_data("JDFSSolver", "backward"),
#                 "total_time": None,
#                 "normal_time": None,
#                 "external_time": None,
#                 "score": None,
#             },
#             "GuidedDFSSolver": {
#                 "steps": get_aligned_data("JGuidedJDFSSolver_JDFSSolver", "backward"),
#                 "total_time": None,
#                 "normal_time": None,
#                 "external_time": None,
#                 "score": None,
#             },
#             "GuidedMCMFSolver": {
#                 "steps": get_aligned_data("JGuidedJDFSSolver_JMCMFSolver", "backward"),
#                 "total_time": None,
#                 "normal_time": None,
#                 "external_time": None,
#                 "score": None,
#             },
#         },
#         "num_cells": num_cells,
#         "grid_size": grid_sizes,
#     }


# def scores_for_2d_plot() -> dict:
#     df = _load_grid_df()
#     pivot_df = _build_pivot(df, values=['score'])

#     def get_aligned_data(algo_name):
#         return _get_aligned(pivot_df, 'score', algo_name, float)

#     grid_sizes = [f'{w},{h}' for w, h, _ in pivot_df.index]
#     num_cells = [n for _, _, n in pivot_df.index]

#     return {
#         "DFSSolver": get_aligned_data("JDFSSolver"),
#         "GuidedDFSSolver": get_aligned_data("JGuidedJDFSSolver_JDFSSolver"),
#         "GuidedMCMFSolver": get_aligned_data("JGuidedJDFSSolver_JMCMFSolver"),
#         "num_cells": num_cells,
#         "grid_size": grid_sizes,
#     }

import pandas as pd
import tiling_algorithms.utils.config as config


def _load_grid_df() -> pd.DataFrame:
    df = pd.read_csv(config.results_save_path)

    def parse_grid_size(size_str):
        w, h = map(int, size_str.split(","))
        return w, h

    parsed = df["grid_size"].apply(parse_grid_size)
    df["grid_w"] = parsed.apply(lambda t: t[0])
    df["grid_h"] = parsed.apply(lambda t: t[1])
    df["num_cells"] = df["grid_w"] * df["grid_h"]
    return df


def _build_pivot(df: pd.DataFrame, values: list[str]) -> pd.DataFrame:
    pivot_df = df.pivot_table(
        # CHANGED: Put grid_w first so sort_index() orders by width primarily
        index=["grid_w", "grid_h", "num_cells"],
        columns="algorithm_name",
        values=values,
        aggfunc="mean",  # averages duplicate runs of the same algo+grid_size; NaNs stay NaN, not 0
    )
    return pivot_df.sort_index()  # sorts by grid_w, then grid_h, then num_cells


def _get_aligned(pivot_df: pd.DataFrame, col: str, algo_name: str, cast) -> list:
    key = (col, algo_name)
    if key not in pivot_df.columns:
        # algorithm never appears for this metric at all
        return [None] * len(pivot_df)
    series = pivot_df[key]
    return [cast(v) if pd.notna(v) else None for v in series]


def steps_for_2d_plot() -> dict:
    df = _load_grid_df()

    # CHANGED: Request all necessary columns from the dataframe
    pivot_df = _build_pivot(
        df,
        values=[
            "steps_forward",
            "steps_backward",
            "total_time",
            "normal_total_time",
            "external_time",
            "score",
        ],
    )

    # CHANGED: Create a generic helper that accepts exact column names and casting types
    def get_metric(algo_name, metric_name, cast_type=float):
        # if cast_type is float:
        #     cast_type = lambda x: round(float(x), 3)

        return _get_aligned(pivot_df, metric_name, algo_name, cast_type)

    grid_sizes = [f"{w},{h}" for w, h, _ in pivot_df.index]
    num_cells = [n for _, _, n in pivot_df.index]

    return {
        "forward": {
            "DFSSolver": {
                "steps": get_metric("JDFSSolver", "steps_forward", int),
                "total_time": get_metric("JDFSSolver", "total_time", float),
                "normal_time": None,
                "external_time": None,
                "score": get_metric("JDFSSolver", "score", float),
            },
            "GuidedDFSSolver": {
                "steps": get_metric(
                    "JGuidedJDFSSolver_JDFSSolver", "steps_forward", int
                ),
                "total_time": get_metric(
                    "JGuidedJDFSSolver_JDFSSolver", "total_time", float
                ),
                "normal_time": get_metric(
                    "JGuidedJDFSSolver_JDFSSolver", "normal_total_time", float
                ),
                "external_time": get_metric(
                    "JGuidedJDFSSolver_JDFSSolver", "external_time", float
                ),
                "score": get_metric("JGuidedJDFSSolver_JDFSSolver", "score", float),
            },
            "GuidedMCMFSolver": {
                "steps": get_metric(
                    "JGuidedJDFSSolver_JMCMFSolver", "steps_forward", int
                ),
                "total_time": get_metric(
                    "JGuidedJDFSSolver_JMCMFSolver", "total_time", float
                ),
                "normal_time": get_metric(
                    "JGuidedJDFSSolver_JMCMFSolver", "normal_total_time", float
                ),
                "external_time": get_metric(
                    "JGuidedJDFSSolver_JMCMFSolver", "external_time", float
                ),
                "score": get_metric("JGuidedJDFSSolver_JMCMFSolver", "score", float),
            },
            "MCMFSolver": {
                "steps": get_metric("JMCMFSolver", "steps_forward", int),
                "total_time": get_metric("JMCMFSolver", "total_time", float),
                "normal_time": None,
                "external_time": None,
                "score": get_metric("JMCMFSolver", "score", float),
            },
        },
        "backward": {
            "DFSSolver": {
                "steps": get_metric("JDFSSolver", "steps_backward", int),
                "total_time": None,
                "normal_time": None,
                "external_time": None,
                "score": None,
            },
            "GuidedDFSSolver": {
                "steps": get_metric(
                    "JGuidedJDFSSolver_JDFSSolver", "steps_backward", int
                ),
                "total_time": None,
                "normal_time": None,
                "external_time": None,
                "score": None,
            },
            "GuidedMCMFSolver": {
                "steps": get_metric(
                    "JGuidedJDFSSolver_JMCMFSolver", "steps_backward", int
                ),
                "total_time": None,
                "normal_time": None,
                "external_time": None,
                "score": None,
            },
        },
        "num_cells": num_cells,
        "grid_size": grid_sizes,
    }
