from manim import *
from src.viz.utils.results import steps_for_2d_plot
from src.viz.utils.visual import BasePresentation, reset_slide


def results_slide(slide: BasePresentation) -> None:
    title: Text = Text("Evaluation")

    slide.play(FadeIn(title))

    slide.next_section()
    slide.play(FadeOut(title))

    eval_group: VGroup = VGroup(
        Text("Evaluation Setup", font_size=26),
        Paragraph(
            *(
                "Board:",
                "\tRound Robin:",
                "\t\t+ Widths: [4, 6, 8, 10, 12, 14, 16]",
                "\t\t+ Heights: [4, 6, 8, 10, 12, 14, 16]",
                "Costs range: [1, 21)",
                "Runs: 100",
            ),
            font_size=18,
        ),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

    record_group: VGroup = VGroup(
        Text("Recorded Values", font_size=26),
        Paragraph(
            *(
                "Steps Forward/Backward | Tiling/Untiling",
                "Score",
                "Total time = Run time (+ CNN time)",
            ),
            font_size=18,
        ),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

    env_setup: VGroup = VGroup(eval_group, record_group).arrange(
        DOWN, aligned_edge=LEFT, buff=1.0
    )

    slide.play(FadeIn(env_setup))

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)

    data: dict = steps_for_2d_plot()

    steps_slide(slide, data)
    times_slide(slide, data)
    scores_slide(slide, data)


def scores_slide(slide: BasePresentation, data: dict) -> None:
    plot_cell_summary: VGroup = VGroup(
        *(
            create_plot_by_cells(
                "DFSSolver",
                "forward",
                "score",
                data,
                f"DFS Solver",
                color=BLUE,
            ),
            create_plot_by_cells(
                "GuidedDFSSolver",
                "forward",
                "score",
                data,
                f"CNN (DFS Trained) + DFS Solver",
                color=RED,
            ),
            create_plot_by_cells(
                "GuidedMCMFSolver",
                "forward",
                "score",
                data,
                f"CNN (MCMF Trained) + DFS Solver",
                color=YELLOW,
            ),
            create_plot_by_cells(
                "MCMFSolver",
                "forward",
                "score",
                data,
                f"MCMF",
                color=GREEN,
            ),
        )
    ).arrange_in_grid(2, 2, buff=1.0)

    plot_title: Text = Text(
        "Avg. Score Board (ABSDIFF) By # Cells | Lower Is Better", font_size=32
    )

    plot_group: VGroup = (
        VGroup(plot_title, plot_cell_summary).arrange(DOWN, buff=1.2).scale(0.35)
    )

    plot_group.next_to(slide.slide_category, DOWN, buff=0.5)

    slide.play(FadeIn(plot_group))

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)


def steps_slide(slide: BasePresentation, data: dict) -> None:
    create_steps_slide(slide, data, "DFSSolver", "DFS Solver")
    create_steps_slide(slide, data, "GuidedDFSSolver", "CNN (DFS Trained) + DFS Solver")
    create_steps_slide(
        slide, data, "GuidedMCMFSolver", "CNN (MCMF Trained) + DFS Solver"
    )


def times_slide(slide: BasePresentation, data: dict) -> None:
    create_time_slide(slide, data, "DFSSolver", "DFS Solver")
    create_time_slide(slide, data, "GuidedDFSSolver", "CNN (DFS Trained) + DFS Solver")
    create_time_slide(
        slide, data, "GuidedMCMFSolver", "CNN (MCMF Trained) + DFS Solver"
    )
    create_time_slide(slide, data, "MCMFSolver", "MCMF Solver")


def create_time_slide(
    slide: BasePresentation, data: dict, algorithm: str, repr: str
) -> None:
    create_algorithm_result(
        algorithm, "forward", "total_time", data, slide, f"{repr} Total Time (s)"
    )
    slide.next_section()
    reset_slide(slide)

    plot_cell_summary: VGroup = (
        create_plot_by_cells(
            algorithm,
            "forward",
            "total_time",
            data,
            f"{repr} Total Time (s) By # Cells",
        )
        .scale(0.5)
        .center()
    )

    slide.play(FadeIn(plot_cell_summary))

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)


def create_steps_slide(
    slide: BasePresentation, data: dict, algorithm: str, repr: str
) -> None:
    create_algorithm_result(
        algorithm, "forward", "steps", data, slide, f"{repr} Forward/Tiling Steps"
    )
    slide.next_section()
    reset_slide(slide)
    create_algorithm_result(
        algorithm, "backward", "steps", data, slide, f"{repr} Backward/Untiling Steps"
    )
    slide.next_section()
    reset_slide(slide)

    plot_cell_summary: VGroup = VGroup(
        create_plot_by_cells(
            algorithm, "forward", "steps", data, f"{repr} Tiling Steps By # Cells"
        ),
        create_plot_by_cells(
            algorithm, "backward", "steps", data, f"{repr} Untiling Steps By # Cells"
        ),
    )

    plot_cell_summary.arrange(RIGHT, buff=1.0).scale(0.5).center()

    slide.play(FadeIn(plot_cell_summary))

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)


def create_algorithm_result(
    algorithm: str,
    direction: str,
    col: str,
    data: dict,
    slide: BasePresentation,
    repr: str,
) -> None:
    plots: VGroup = VGroup()

    algorithm_title: Text = Text(f"{repr} (Avg. 100 runs)", font_size=16).next_to(
        slide.slide_category, DOWN, buff=0.5
    )

    for i in range(0, 7 * 7, 7):
        plots.add(create_plot(algorithm, direction, col, (i, i + 7), data))

    plots.arrange_in_grid(3, 3).scale(0.3).next_to(algorithm_title, DOWN, buff=0.5)

    slide.play(FadeIn(algorithm_title, plots))


def create_plot_by_cells(
    algorithm: str,
    direction: str,
    col: str,
    data: dict,
    repr: str,
    color: ManimColor | None = None,
) -> VGroup:
    plot: VGroup = VGroup()

    y_vals = data[direction][algorithm][col]
    x_vals = data["num_cells"]

    y_min, y_max = min(y_vals), max(y_vals)
    y_step = (y_max - y_min) / 5
    if y_step == 0:
        y_step = 1

    x_length = len(y_vals)

    axes: Axes = Axes(
        x_range=[0, x_length, 1],
        y_range=[y_min, y_max + y_step, y_step],
        # y_axis_config={"include_numbers": True},
    )

    axes.x_axis.add_labels({i: size for i, size in enumerate(x_vals) if i % 5 == 0})

    # Generate y-ticks dynamically based on your step logic
    num_y_steps = int(round((y_max - y_min) / y_step))
    y_ticks = [y_min + i * y_step for i in range(num_y_steps + 2)]

    # Y-axis labels in scientific notation (keeping "0" clean if it exists)
    axes.y_axis.add_labels(
        {
            y: MathTex(format_y_label(y) if y != 0 else "0", font_size=24)
            for y in y_ticks
        }
    )

    plot.add(axes)

    dots = VGroup()

    if not color:
        color = BLUE if direction == "forward" else RED

    for i, y in enumerate(y_vals):
        if y is not None:
            dot = Dot(axes.c2p(i, y), color=color)
            dots.add(dot)

    plot.add(dots)

    algorithm_caption: Text = Text(f"{repr} (Avg. 100 runs)", font_size=24).next_to(
        plot, UP, buff=0.5
    )

    plot.add(algorithm_caption)

    return plot


def create_plot(
    algorithm: str, direction: str, col: str, limit: tuple[int, int], data: dict
) -> VGroup:
    plot: VGroup = VGroup()

    y_vals = data[direction][algorithm][col][limit[0] : limit[1]]
    grid_size = data["grid_size"][limit[0] : limit[1]]

    y_min, y_max = min(y_vals), max(y_vals)
    y_step = (y_max - y_min) / 5
    if y_step == 0:
        y_step = 1

    x_length = len(y_vals)

    axes: Axes = Axes(
        x_range=[0, x_length, 1],
        y_range=[y_min, y_max + y_step, y_step],
        # x_axis_config={"include_numbers": False},
        # y_axis_config={"include_numbers": True},
    ).scale(0.8)

    axes.x_axis.add_labels({i: size for i, size in enumerate(grid_size)})

    # Generate y-ticks dynamically
    num_y_steps = int(round((y_max - y_min) / y_step))
    y_ticks = [y_min + i * y_step for i in range(num_y_steps + 2)]

    # Y-axis labels in scientific notation
    axes.y_axis.add_labels(
        {
            y: MathTex(format_y_label(y) if y != 0 else "0", font_size=24)
            for y in y_ticks
        }
    )

    plot.add(axes)

    dots = VGroup()

    for i, y in enumerate(y_vals):
        if y is not None:
            dot = Dot(axes.c2p(i, y), color=BLUE if direction == "forward" else RED)
            dots.add(dot)

    plot.add(dots)

    return plot


def format_y_label(y: float) -> str:
    if y == 0:
        return "0"

    abs_y = abs(y)

    if 0.01 <= abs_y < 1000:
        formatted = f"{y:.3f}"
        if abs(float(formatted)) >= 1000:
            return f"{y:.1e}"
        return formatted.rstrip("0").rstrip(".")
    else:
        return f"{y:.1e}"
