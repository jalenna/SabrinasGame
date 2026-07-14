from manim import *
from torch import nn
from typing import Any
from random import seed as rand_seed
from manim_slides.slide import ThreeDSlide
from src.viz.utils.trackers import JSlideNumberTracker
from src.algorithms.utils.core import is_valid_board_size
from src.viz.utils.algorithms.dfs import JGuidedDepthSolver
from src.viz.utils.visual import reset_slide, show_slide_number
from src.algorithms.utils.types import ExplicitDims, Tiles, iVec2D
from src.viz.utils.algorithms.utils.board_generator import VizBoardGenerator

config["max_files_cached"] = -1


class CNNSlide(ThreeDSlide):
    skip_reversing = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slide_tracker: JSlideNumberTracker = JSlideNumberTracker()
        self.current_slide_number: Text = Text(
            str(self.slide_tracker.current), font_size=32).to_edge(DR)
        self.board_generator: VizBoardGenerator = VizBoardGenerator()
        self.guided_solver: JGuidedDepthSolver = JGuidedDepthSolver()

    def construct(self) -> None:
        rand_seed(42)

        self.intro()

    def intro(self) -> None:
        show_slide_number(self, update=False)

        text: Text = Text("Convolutional Neural Network (CNN)")
        self.play(Write(text))

        self.next_slide()

        self.play(FadeOut(text))
        self.slide_tracker.inc()
        show_slide_number(self)

        dim: iVec2D = iVec2D(6, 6)
        cost_range: tuple[int, int] = (1, 21)
        viz_board = self._create_board(dim, cost_range)
        data_board: Tiles = self.board_generator.boards[-1][0]

        self.play(FadeIn(viz_board))

        self.move_camera(zoom=.5)

        self.next_section()

        conv1_layer = self.guided_solver.solver.model.conv1

        conv1_viz = self._create_conv_layer(conv1_layer)
        conv1_viz.next_to(viz_board, RIGHT * 2, buff=1)
        self.move_camera(frame_center=conv1_viz)
        self.play(FadeIn(conv1_viz))

        self.next_section()
        pool1_layer = self.guided_solver.solver.model.pool
        pool_viz = self._create_pool_layer(conv1_layer, pool1_layer)
        pool_viz.next_to(conv1_viz, RIGHT * 5, buff=1)
        self.move_camera(frame_center=pool_viz)
        self.play(FadeIn(pool_viz))

        self.next_section()
        conv2_layer = self.guided_solver.solver.model.conv2
        conv2_viz = self._create_conv_layer(conv2_layer)
        conv2_viz.next_to(pool_viz, RIGHT * 5, buff=1)
        self.move_camera(frame_center=conv2_viz)
        self.play(FadeIn(conv2_viz))

        self.next_slide()

        reset_slide(self)

    def _create_textbox(self, content: VMobject, color: ManimColor = WHITE, stroke_color: ManimColor = BLACK) -> VGroup:
        result = VGroup()
        box = Rectangle(
            height=1, width=1, fill_color=color,
            fill_opacity=1, stroke_color=stroke_color,
        )
        cont = content.move_to(box.get_center())
        result.add(box, cont)
        return result

    def _create_board(self, dim: iVec2D, rand_range: tuple[int, int]) -> VGroup:
        if not is_valid_board_size(dim):
            raise Exception("Board size and values size are not equal")

        self.board_generator.generate(ExplicitDims([dim]), rand_range)
        board: Tiles = self.board_generator.boards[-1][0]

        group: VGroup = VGroup()

        for tile in board:
            group.add(self._create_textbox(
                Text(str(int(tile)), color=BLACK, font_size=24)))

        return group.arrange_in_grid(dim.y, dim.x, 0.)

    def _create_conv_layer(self, layer: nn.Conv2d) -> VGroup:
        group: VGroup = VGroup()
        rect_group: VGroup = VGroup()

        out_channels = layer.out_channels
        kernel_size = layer.kernel_size[0]

        for i in range(out_channels):
            rect: Rectangle = Rectangle(
                height=kernel_size, width=kernel_size, grid_xstep=1., grid_ystep=1., fill_color=BLUE, fill_opacity=.7)
            rect.set_z(i * .3)
            rect_group.add(rect)

        label = Text(
            f"Conv2d: {out_channels} filters\nKernel: {kernel_size}x{kernel_size}",
            font_size=20
        ).next_to(rect_group, UP * 5)

        group.add(label, rect_group)

        return group

    def _create_pool_layer(self, prev_layer: nn.Module, pool_layer: nn.AdaptiveAvgPool2d) -> VGroup:
        group: VGroup = VGroup()
        rect_group: VGroup = VGroup()

        out_channels = getattr(prev_layer, 'out_channels', 64)
        output_size: int = pool_layer.output_size[0]

        for i in range(out_channels):
            rect = Rectangle(
                height=output_size,
                width=output_size,
                fill_color=GREEN,
                fill_opacity=0.7,
                grid_xstep=1., grid_ystep=1.,
            )

            rect.set_z(i * .3)
            rect_group.add(rect)

        label = Text(
            f"Adaptive AvgPool 2d\nOutput: {output_size}x{output_size}",
            font_size=20
        ).next_to(rect_group, UP * 5)

        group.add(label, rect_group)
        return group
