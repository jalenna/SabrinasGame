from manim import *
from typing import Any
from random import seed as rand_seed
from manim_slides.slide import ThreeDSlide
from src.viz.utils.trackers import JSlideNumberTracker
from src.viz.utils.visual import reset_slide, show_slide_number
from src.viz.utils.results import scores_for_2d_plot, steps_for_2d_plot

config["max_files_cached"] = -1


class ResultsSlide(ThreeDSlide):
    skip_reversing = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slide_tracker: JSlideNumberTracker = JSlideNumberTracker(30)
        self.current_slide_number: Text = Text(
            str(self.slide_tracker.current), font_size=32).to_edge(DR)

    def construct(self) -> None:
        rand_seed(42)

        self.steps()
        self.scores()

    def scores(self) -> None:
        show_slide_number(self)

        scores_dict: dict[str, list[float]] = scores_for_2d_plot()

        scores_dfs: list[float] = scores_dict["DFSSolver"]
        scores_gdfs: list[float] = scores_dict["GuidedJDFSSolver"]

        max_score: float = max(max(scores_dfs), max(scores_gdfs))

        num_cells: list[int] = [int(i) for i in scores_dict["num_cells"]]

        data_length = len(num_cells)

        score_axes = Axes(
            x_range=[0, data_length - 1, 1],
            y_range=[0, max_score],
            x_axis_config={"label_constructor": Text,
                           "include_ticks": True, "include_numbers": False},
            y_axis_config={"label_constructor": Text,
                           "include_ticks": True, "include_numbers": True}
        )

        labels_dict = {
            i: str(num_cells[i])
            for i in range(0, data_length, 5)
        }

        score_axes.add_coordinates(labels_dict)
        # backward_axis.add_coordinates(labels_dict)

        x_label = Text("Number of Cells (N)", font_size=24,
                       color=WHITE).next_to(score_axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Abs Diff Avg 100 runs", font_size=24, color=WHITE).next_to(
            score_axes.y_axis, LEFT, buff=0.3).rotate(90 * DEGREES)
        axis_labels = VGroup(x_label, y_label)

        x_range = [0, len(scores_dfs) - 1, 1]

        score_dfs_graph = score_axes.plot(
            lambda x: scores_dfs[int(x)],
            x_range=x_range,
            color=RED,
            use_smoothing=False
        )

        score_gdfs_graph = score_axes.plot(
            lambda x: scores_gdfs[int(x)],
            x_range=x_range,
            color=GREEN,
            use_smoothing=False
        )

        gdfs_label = Text("Guided DFS", font_size=32, color=GREEN).next_to(
            score_axes.get_edge_center(UP), UP)

        dfs_label = Text("DFS", font_size=32, color=RED).next_to(
            gdfs_label, UP)

        self.move_camera(zoom=.5, frame_center=score_axes)

        self.play(
            Create(score_axes),
            Write(axis_labels),
        )

        self.wait(0.5)

        self.play(
            Create(score_dfs_graph),
            Create(score_gdfs_graph),
            FadeIn(dfs_label),
            FadeIn(gdfs_label)
        )

    def steps(self) -> None:
        show_slide_number(self, update=False)

        steps_dict: dict[str, dict[str, list[int]]] = steps_for_2d_plot()

        steps_forward_dfs: list[int] = steps_dict["forward"]["DFSSolver"]
        steps_backward_dfs: list[int] = steps_dict["backward"]["DFSSolver"]
        steps_forward_gdfs: list[int] = steps_dict["forward"]["GuidedJDFSSolver"]
        steps_backward_gdfs: list[int] = steps_dict["backward"]["GuidedJDFSSolver"]
        max_steps_forward: int = max(max(steps_dict["forward"]["DFSSolver"]), max(
            steps_dict["forward"]["GuidedJDFSSolver"]))
        max_steps_backward: int = max(max(steps_dict["backward"]["DFSSolver"]), max(
            steps_dict["backward"]["GuidedJDFSSolver"]))

        num_cells: list[int] = steps_dict["forward"]["num_cells"]

        data_length = len(num_cells)

        forward_axis = Axes(
            x_range=[0, data_length - 1, 1],
            y_range=[0, max_steps_forward, 30],
            x_axis_config={"label_constructor": Text,
                           "include_ticks": True, "include_numbers": False},
            y_axis_config={"label_constructor": Text,
                           "include_ticks": True, "include_numbers": True}
        )

        backward_axis = Axes(
            x_range=[0, data_length - 1, 1],
            y_range=[0, max_steps_backward, 30],
            x_axis_config={"label_constructor": Text,
                           "include_ticks": True, "include_numbers": False},
            y_axis_config={"label_constructor": Text,
                           "include_ticks": True, "include_numbers": True}
        )

        labels_dict = {
            i: str(num_cells[i])
            for i in range(0, data_length, 5)
        }

        forward_axis.add_coordinates(labels_dict)
        # backward_axis.add_coordinates(labels_dict)

        plot_group: VGroup = VGroup()
        plot_group.add(forward_axis, backward_axis)
        plot_group.arrange(buff=2)

        x_label = Text("Number of Cells (N)", font_size=24,
                       color=WHITE).next_to(forward_axis.x_axis, DOWN, buff=0.3)
        forward_y_label = Text("Steps Forward Avg. 100 runs", font_size=24, color=WHITE).next_to(
            forward_axis.y_axis, LEFT, buff=0.3).rotate(90 * DEGREES)
        forward_axis_labels = VGroup(x_label, forward_y_label)
        backward_y_label = Text("Steps Backward Avg. 100 runs", font_size=24, color=WHITE).next_to(
            backward_axis.y_axis, RIGHT, buff=0.3).rotate(90 * DEGREES)

        x_range = [0, len(steps_forward_dfs) - 1, 1]

        forward_dfs_graph = forward_axis.plot(
            lambda x: steps_forward_dfs[int(x)],
            x_range=x_range,
            color=RED,
            use_smoothing=False
        )

        backward_dfs_graph = backward_axis.plot(
            lambda x: steps_backward_dfs[int(x)],
            x_range=x_range,
            color=RED,
            use_smoothing=False
        )

        forward_gdfs_graph = forward_axis.plot(
            lambda x: steps_forward_gdfs[int(x)],
            x_range=x_range,
            color=GREEN,
            use_smoothing=False
        )

        backward_gdfs_graph = backward_axis.plot(
            lambda x: steps_backward_gdfs[int(x)],
            x_range=x_range,
            color=GREEN,
            use_smoothing=False
        )

        gdfs_label = Text("Guided DFS", font_size=32, color=GREEN).next_to(
            plot_group.get_edge_center(UP), UP)

        dfs_label = Text("DFS", font_size=32, color=RED).next_to(
            gdfs_label, UP)

        self.move_camera(zoom=.4, frame_center=plot_group)

        self.play(
            Create(forward_axis),
            Create(backward_axis),
            Write(forward_axis_labels),
            Write(backward_y_label),
        )

        self.wait(0.5)

        self.play(
            Create(forward_dfs_graph),
            Create(backward_dfs_graph),
            Create(forward_gdfs_graph),
            Create(backward_gdfs_graph),
            FadeIn(dfs_label),
            FadeIn(gdfs_label)
        )

        self.next_slide()
        self.slide_tracker.inc()
        reset_slide(self)
