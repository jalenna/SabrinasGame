import torch
from manim import *
from torch import nn
from typing import Any, cast
import torch.nn.functional as F
from random import seed as rand_seed
from manim_slides.slide import ThreeDSlide
import tiling_algorithms.ml.config as ml_config
from src.viz.utils.trackers import JSlideNumberTracker
from src.viz.utils.algorithms.dfs import JGuidedDepthSolver
from src.viz.utils.visual import reset_slide, show_slide_number
from tiling_algorithms.utils.core import Pairs, is_valid_board_size
from tiling_algorithms.utils.types import ExplicitDims, Tiles, iVec2D
from src.viz.utils.algorithms.utils.board_generator import VizBoardGenerator

config["max_files_cached"] = -1


class CNNSlide(ThreeDSlide):
    skip_reversing = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slide_tracker: JSlideNumberTracker = JSlideNumberTracker(23)
        self.current_slide_number: Text = Text(
            str(self.slide_tracker.current), font_size=32).to_edge(DR)
        self.board_generator: VizBoardGenerator = VizBoardGenerator()
        self.guided_solver: JGuidedDepthSolver = JGuidedDepthSolver(
            ml_config.save_path / "JDFSSolver.pt")

    def construct(self) -> None:
        rand_seed(42)

        self.intro()
        self.cnn_architecture()
        self.demo()

    def intro(self) -> None:
        show_slide_number(self, update=False)

        title: Text = Text("Convolutional Neural Network (CNN)")
        self.play(Write(title))

        self.next_slide()

        self.play(FadeOut(title))
        self.slide_tracker.inc()
        show_slide_number(self)

        formula: Text = Text("f(x) = z")

        self.play(FadeIn(formula))

        self.next_section()

        t_formula: Text = Text("CNN(input) ~= reality")
        self.play(ReplacementTransform(formula, t_formula))
        formula = t_formula

        self.next_slide()
        self.slide_tracker.inc()
        show_slide_number(self)

        self.play(FadeOut(formula))

        dim: iVec2D = iVec2D(6, 6)
        cost_range: tuple[int, int] = (1, 21)
        viz_board: VGroup = self._create_board(dim, cost_range)
        data_board: Tiles = self.board_generator.boards[-1][0]

        board_label: Text = Text("Input")
        self.play(FadeIn(viz_board))
        self.move_camera(zoom=.5)
        board_bounds: SurroundingRectangle = SurroundingRectangle(
            viz_board, buff=MED_LARGE_BUFF)
        self.play(Create(board_bounds))
        self.play(Write(board_label.next_to(viz_board, UP, buff=1)))

        self.next_section()

        architecture_viz: VGroup = VGroup()
        model_black_box: Rectangle = Rectangle(width=dim.x, height=dim.y)
        model_label: Text = Text("CNN")
        model_black_box.add(model_label)
        architecture_viz.add(model_black_box).next_to(
            board_bounds, RIGHT, buff=2)

        arrow_to_model: Arrow = Arrow(board_bounds.get_edge_center(
            RIGHT), architecture_viz.get_edge_center(LEFT))

        self.move_camera(frame_center=architecture_viz)
        self.play(FadeIn(architecture_viz))
        self.play(Create(arrow_to_model))

        self.next_section()

        solved_viz_board: VGroup = viz_board.copy().next_to(
            model_black_box, RIGHT, buff=2 + MED_LARGE_BUFF / 2)
        solved_board_bounds: SurroundingRectangle = SurroundingRectangle(
            solved_viz_board, buff=MED_LARGE_BUFF)
        lines: dict[tuple[int, int], Line] = self.guided_solver.solve(
            dim, data_board, solved_viz_board)

        self.play(FadeIn(solved_viz_board))
        solved_board_label: Text = Text("Reality")

        arrow_model_to: Arrow = Arrow(model_black_box.get_edge_center(
            RIGHT), solved_board_bounds.get_edge_center(LEFT))

        self.play(Create(arrow_model_to))

        seq: list[Animation] = []
        for state in self.guided_solver.solver.history:
            u, v = state.pair[0], state.pair[1]
            key = (min(u, v), max(u, v))
            line = lines[key]

            if state.added:
                seq.append(FadeIn(line))
            else:
                seq.append(FadeOut(line))
        self.play(Succession(*seq, run_time=1.))
        self.play(Create(solved_board_bounds))
        self.play(Write(solved_board_label.next_to(
            solved_board_bounds, UP, buff=1)))

        self.move_camera(zoom=.4)

        self.next_section()

        self.play(arrow_model_to.animate.flip(), arrow_to_model.animate.flip())

        self.next_section()

        self.play(Create(SurroundingRectangle(architecture_viz)))
        self.wait(1)
        self.play(FadeOut(solved_board_bounds, solved_viz_board, viz_board,
                  board_bounds, solved_board_label, board_label, model_label, arrow_model_to, arrow_to_model, architecture_viz))

        self.move_camera(zoom=4.)

        reset_slide(self)
        self.slide_tracker.inc()

    def cnn_architecture(self) -> None:
        show_slide_number(self)

        dim: iVec2D = iVec2D(6, 6)
        cost_range: tuple[int, int] = (1, 21)
        viz_board: VGroup = self._create_board(dim, cost_range)
        # data_board: Tiles = self.board_generator.boards[-1][0]

        architecture_viz: VGroup = VGroup()

        conv1_layer = self.guided_solver.solver.model.conv1
        conv1_viz = self._create_conv_layer(conv1_layer)
        conv1_viz.next_to(viz_board, RIGHT * 2, buff=1)
        self.move_camera(frame_center=conv1_viz, zoom=.25)
        self.play(FadeIn(conv1_viz))
        architecture_viz.add(conv1_viz)

        self.next_section()
        pool1_layer = self.guided_solver.solver.model.pool
        pool_viz = self._create_pool_layer(conv1_layer, pool1_layer)
        pool_viz.next_to(conv1_viz, RIGHT * 5, buff=1)
        self.move_camera(frame_center=pool_viz, zoom=.2)
        self.play(FadeIn(pool_viz))
        architecture_viz.add(pool_viz)

        self.next_section()
        conv2_layer = self.guided_solver.solver.model.conv2
        conv2_viz = self._create_conv_layer(conv2_layer)
        conv2_viz.next_to(pool_viz, RIGHT * 5, buff=1)
        self.move_camera(frame_center=conv2_viz)
        self.play(FadeIn(conv2_viz))
        architecture_viz.add(conv2_viz)

        self.next_section()
        lin1_layer = self.guided_solver.solver.model.fc1
        lin1_viz = self._create_linear_layer(lin1_layer)
        lin1_viz.next_to(conv2_viz, RIGHT * 5, buff=1)
        self.move_camera(frame_center=lin1_viz)
        self.play(FadeIn(lin1_viz))
        architecture_viz.add(lin1_viz)

        self.next_section()
        lin2_layer = self.guided_solver.solver.model.fc2
        lin2_viz = self._create_linear_layer(lin2_layer, 15)
        lin2_viz.next_to(lin1_viz, RIGHT * 5, buff=1)
        self.move_camera(frame_center=lin2_viz)
        self.play(FadeIn(lin2_viz))
        architecture_viz.add(lin2_viz)

        self.next_section()

        self.move_camera(frame_center=architecture_viz, zoom=.15)
        self.play(
            Create(SurroundingRectangle(
                architecture_viz, buff=LARGE_BUFF)),
            Write(Text("CNN Architecture", font_size=72).next_to(
                architecture_viz, UP * 7))
        )

        self.next_slide()
        reset_slide(self)
        self.slide_tracker.inc()
        show_slide_number(self)

        cnn_features_img: ImageMobject = ImageMobject(
            "./assets/cnn_features_vidhya.webp")
        img_cap: Text = Text(
            "Vignesh, S. (2020, June 26).\nThe world through the eyes of a CNN.\nMedium.\nhttps://medium.com/analytics-vidhya/the-world-through-the-eyes-of-cnn-5a52c034dbeb", font_size=8, slant=ITALIC).next_to(cnn_features_img, DOWN)

        self.play(FadeIn(cnn_features_img))
        self.play(FadeIn(img_cap))

        self.next_slide()
        reset_slide(self)
        self.slide_tracker.inc()

    def demo(self) -> None:
        show_slide_number(self)

        dim: iVec2D = iVec2D(6, 6)
        cost_range: tuple[int, int] = (1, 21)
        viz_board: VGroup = self._create_board(dim, cost_range)
        data_board: Tiles = self.board_generator.boards[-1][0]

        lines: list[Line] = self.guided_solver.pure_solve(
            dim, data_board, viz_board)

        self.play(FadeIn(viz_board))
        self.wait(1)
        self.play(LaggedStart(*(FadeIn(line) for line in lines)))

        self.next_slide()
        reset_slide(self)
        self.slide_tracker.inc()
        show_slide_number(self)

        out_layer = self.guided_solver.solver.model.fc2
        viz_out_layer: VGroup = self._create_linear_layer(
            out_layer, add_label=self.guided_solver.solver.pairs)

        self.play(FadeIn(viz_out_layer))
        self.move_camera(zoom=.25)

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

    def _create_conv_layer(self, layer: nn.Conv2d, max_num: int = 6) -> VGroup:
        group: VGroup = VGroup()
        rect_group: VGroup = VGroup()

        out_channels = layer.out_channels
        kernel_size = layer.kernel_size[0]

        if out_channels > max_num:
            max_num += 1
            out_channels = max_num

        for i in range(out_channels - 1):

            kernel_group: VGroup = VGroup()
            weights = layer.weight[i].detach()

            board_filter = weights[1]
            board_filter = F.normalize(board_filter)
            board_filter = torch.abs(board_filter).flatten().tolist()

            for bf in board_filter:
                square: Square = Square(1, fill_color=BLUE, fill_opacity=bf)
                kernel_group.add(square)

            kernel_group.arrange_in_grid(kernel_size, kernel_size)
            rect_group.add(kernel_group)

        if out_channels == max_num:
            rect_group.add(Text(".\n.\n.\n"))
        rect_group.arrange_in_grid(out_channels, 1, buff=LARGE_BUFF)

        label = Text(
            f"Conv2d: {layer.out_channels} filters\nKernel: {kernel_size}x{kernel_size}",
            font_size=32
        ).next_to(rect_group, UP * 5)

        group.add(label, rect_group)

        return group

    def _create_pool_layer(self, prev_layer: nn.Module, pool_layer: nn.AdaptiveAvgPool2d, max_num: int = 6) -> VGroup:
        group: VGroup = VGroup()
        rect_group: VGroup = VGroup()

        og_out_channels = getattr(prev_layer, 'out_channels', 64)
        out_channels = og_out_channels
        output_size: int = cast(
            int, cast(tuple[int, int], pool_layer.output_size)[0])

        if out_channels > max_num:
            max_num += 1
            out_channels = max_num

        for i in range(out_channels):
            if out_channels == max_num and i == max_num // 2:
                rect_group.add(Text(".\n.\n.\n"))
                continue

            rect = Rectangle(
                height=output_size,
                width=output_size,
                fill_color=GREEN,
                fill_opacity=0.7,
                grid_xstep=1., grid_ystep=1.,
            )

            rect.set_z(i * .3)
            rect_group.add(rect)

        rect_group.arrange_in_grid(out_channels, 1, buff=LARGE_BUFF)

        label = Text(
            f"Adaptive AvgPool 2d: {og_out_channels} pools\nOutput: {output_size}x{output_size}",
            font_size=32
        ).next_to(rect_group, UP * 5)

        group.add(label, rect_group)
        return group

    def _create_linear_layer(self, layer: nn.Linear, max_num: int = 10, add_label: Pairs | None = None) -> VGroup:
        group: VGroup = VGroup()
        neuron_group: VGroup = VGroup()

        output_tensor = layer.weight
        out_features: int = output_tensor.shape[0]
        display_count: int = min(out_features, max_num)

        activations = output_tensor[1].detach()

        a_min, a_max = activations.min(), activations.max()
        normalized = (activations - a_min) / (a_max - a_min + 1e-8)

        for i in range(display_count):
            neuron: Square = Square(1, fill_color=BLUE,
                                    fill_opacity=float(normalized[i]))

            if add_label is not None:
                neuron.add(Text(str(add_label[i])))

            neuron_group.add(neuron)

        if out_features > max_num:
            neuron_group.add(Text(".\n.\n.\n"))

        neuron_group.arrange(DOWN, buff=LARGE_BUFF)

        label: Text = Text(f"Linear Layer\n{out_features} neurons", font_size=32).next_to(
            neuron_group, UP * 5)

        group.add(label, neuron_group)
        return group
