from manim import *
from typing import Any
from random import seed as rand_seed
from manim_slides.slide import ThreeDSlide
from src.viz.utils.algorithms.dfs import JDepthSolver
from src.viz.utils.trackers import JSlideNumberTracker
from src.viz.utils.visual import reset_slide, show_slide_number
from src.algorithms.utils.types import Tiles, iVec2D, ExplicitDims
from src.viz.utils.algorithms.linear_greedy import LinearGreedySolver
from src.algorithms.utils.core import calc_avg_cost, is_valid_board_size
from src.viz.utils.algorithms.utils.board_generator import VizBoardGenerator

config["max_files_cached"] = -1


class SabrinasGame(ThreeDSlide):
    skip_reversing = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slide_tracker: JSlideNumberTracker = JSlideNumberTracker()
        self.current_slide_number: Text = Text(
            str(self.slide_tracker.current), font_size=32).to_edge(DR)
        self.linear_greedy_solver: LinearGreedySolver = LinearGreedySolver()
        self.depth_solver: JDepthSolver = JDepthSolver()
        self.board_generator: VizBoardGenerator = VizBoardGenerator()

    def construct(self) -> None:
        rand_seed(42)

        self.intro()
        self.problem()
        self.psuedo()
        self.demo()
        self.complexity()

    def complexity(self) -> None:
        code_str: str = """
        For every unpaired cell in board:
            sort neighbors by ABS DIFF

            if neighbor not matched:
                Match(cell, neighbor)
        """

        code: Code = Code(
            code_string=code_str
        )

        show_slide_number(self)

        self.move_camera(zoom=.5)

        comp: Text = Text("O(N)").move_to(
            code.get_edge_center(DOWN))

        self.play(code.animate.shift(UP * 2))
        self.play(Write(comp))

        self.next_slide()
        self.slide_tracker.inc()
        show_slide_number(self)

        t_code: Code = Code(
            code_string="""
            Fn dfs():
                if every cell paired:
                    return DONE

                start = First unpaired cell
                sort neighbors by ABS DIFF

                For neighbor in neighbors:
                    Match(cell, neighbor)

                    if dfs():
                        return DONE
                    else:
                        UnMatch(cell, neighbor)
            """,
        )

        self.play(ReplacementTransform(code, t_code))
        code = t_code

        shift = DOWN

        comp = comp.animate.move_to(
            code.get_edge_center(DOWN)).shift(shift)

        self.play(code.animate.shift(UP))
        self.play(comp)

        self.next_section()

        t_comp: Text = Text("O(N * d)").move_to(
            code.get_edge_center(DOWN)).shift(shift)
        self.play(ReplacementTransform(comp, t_comp))
        comp = t_comp

        self.next_section()

        t_comp: Text = Text(
            "O(N * d * d * d * ... * d)").move_to(
            code.get_edge_center(DOWN)).shift(shift)
        self.play(ReplacementTransform(comp, t_comp))
        comp = t_comp

        self.next_section()

        t_comp: Text = Text("O(N * d^N)").move_to(
            code.get_edge_center(DOWN)).shift(shift)
        self.play(ReplacementTransform(comp, t_comp))
        comp = t_comp

        self.next_section()

        t_comp: Text = Text("O(N * d^N/2)").move_to(
            code.get_edge_center(DOWN)).shift(shift)
        self.play(ReplacementTransform(comp, t_comp))
        comp = t_comp

        self.next_section()

        reset_slide(self)
        self.slide_tracker.inc()
        show_slide_number(self)

        axis = Axes(
            x_range=[0, 30, 5],
            y_range=[0, 100, 20],
            x_length=9,
            y_length=6,
        ).to_edge(DL, buff=1.0)

        x_label = Text("Number of Cells (N)", font_size=24,
                       color=WHITE).next_to(axis.x_axis, DOWN, buff=0.3)
        y_label = Text("Complexity O(f(V))", font_size=24, color=WHITE).next_to(
            axis.y_axis, LEFT, buff=0.3).rotate(90 * DEGREES)
        axis_labels = VGroup(x_label, y_label)

        greedy_graph = axis.plot(
            lambda x: 2 * x,
            color=GREEN,
            x_range=[0, 30]
        )

        dfs_graph = axis.plot(
            lambda x: x * (4 ** (x / 2)),
            color=RED,
            x_range=[0, 4.5]
        )

        greedy_text = Text("O(N)", font_size=32, color=GREEN).next_to(
            greedy_graph.get_end(), UR, buff=0.1)
        dfs_text = MarkupText("O(N * 4<sup>N/2</sup>)", font_size=32,
                              color=RED).next_to(dfs_graph.get_end(), UL, buff=0.2)

        self.move_camera(frame_center=axis.get_center() + RIGHT, zoom=.5)

        self.play(
            Create(axis),
            Write(axis_labels),
        )
        self.wait(0.5)

        self.play(
            Create(greedy_graph),
            Write(greedy_text),
        )
        self.wait(0.5)

        self.play(
            Create(dfs_graph),
            Write(dfs_text),
        )

        self.next_slide()
        self.slide_tracker.inc()
        reset_slide(self)

    def demo(self) -> None:
        dim: iVec2D = iVec2D(6, 6)
        costs: list[float] = [
            1., 3.,   5.,  7., 2., 4.,
            2., 4.,   8.,  9., 5., 7.,
            3., 5.,   8.,  4., 8., 6.,
            6., 8.,  10.,  9., 1., 1.,
            5., 11., 15., 15., 9., 5.,
            1., 12., 18.,  3., 2., 3.,
        ]
        cost_range: tuple[int, int] = (1, 21)
        viz_board = self._create_board(dim, cost_range)
        self.board_generator.boards[-1] = (costs, dim)
        data_board: Tiles = self.board_generator.boards[-1][0]

        show_slide_number(self)

        self.play(FadeIn(viz_board))

        lines: dict[tuple[int, int], Line] = self.depth_solver.solve(
            dim, data_board, viz_board)

        for state in self.depth_solver.solver.history:
            u, v = state.pair[0], state.pair[1]
            key = (min(u, v), max(u, v))
            line = lines[key]

            if state.added:
                self.play(FadeIn(line, run_time=.2))
            else:
                self.play(FadeOut(line, run_time=.2))

        self.move_camera(zoom=.5)

        avg_cost: float = calc_avg_cost(
            data_board, self.depth_solver.solver.pairs)

        score_text: Text = Text(
            f"Avg ABS DIFF: {avg_cost}", font_size=24).move_to(viz_board.get_edge_center(UP), aligned_edge=DOWN).shift(UP)

        self.play(FadeIn(score_text))

        self.next_slide()
        self.slide_tracker.inc()
        reset_slide(self)

    def psuedo(self) -> None:
        code_str: str = """
        For every unpaired cell in board:
            sort neighbors by ABS DIFF

            if neighbor not matched:
                Match(cell, neighbor)
        """

        code: Code = Code(
            code_string=code_str
        )

        show_slide_number(self)

        self.play(Create(code, run_time=3))

        self.next_section()

        t_code: Code = Code(
            code_string="""
            For every unpaired cell in board:
                sort neighbors by ABS DIFF

                if neighbor not matched:
                    Match(cell, neighbor)

            if size of unpaired cells > 0:
            """,
        )
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        self.wait(2)

        t_code: Code = Code(
            code_string="""
            For every unpaired cell in board:
                sort neighbors by ABS DIFF

                if neighbor not matched:
                    Match(cell, neighbor)

            if size of unpaired cells > 0:
                UnMatch(cell, neighbor)
            """,
        )
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        self.next_section()

        t_code: Code = Code(
            code_string="""
            For every unpaired cell in board:
                sort neighbors by ABS DIFF

                if neighbor not matched:
                    Match(cell, neighbor)

                if size of unpaired cells > 0:
                    UnMatch(cell, neighbor)
            """,
        )
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        self.next_slide()
        self.slide_tracker.inc()
        show_slide_number(self)

        t_code: Code = Code(
            code_string="""
            Fn dfs():
                start = First unpaired cell
                sort neighbors by ABS DIFF

                For neighbor in neighbors:
                    Match(cell, neighbor)

                    if size of unpaired cells > 0:
                        UnMatch(cell, neighbor)
            """,
        )

        code = t_code

        self.wait(2)

        t_code: Code = Code(
            code_string="""
            Fn dfs():
                start = First unpaired cell
                sort neighbors by ABS DIFF

                For neighbor in neighbors:
                    Match(cell, neighbor)

                    dfs()

                    if size of unpaired cells > 0:
                        UnMatch(cell, neighbor)
            """,
        )
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        self.next_section()

        t_code: Code = Code(
            code_string="""
            Fn dfs():
                if every cell paired:
                    return DONE

                start = First unpaired cell
                sort neighbors by ABS DIFF

                For neighbor in neighbors:
                    Match(cell, neighbor)

                    if dfs():
                        return DONE
                    else:
                        UnMatch(cell, neighbor)
            """,
        )
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        self.next_slide()
        self.slide_tracker.inc()
        reset_slide(self)

    def problem(self) -> None:
        dim: iVec2D = iVec2D(6, 6)

        cost_range: tuple[int, int] = (1, 21)
        viz_board: VGroup = self._create_board(dim, cost_range)
        data_board: Tiles = self.board_generator.boards[-1][0]

        self.play(FadeIn(viz_board))

        show_slide_number(self)

        self.next_section()

        lines = self.linear_greedy_solver.solve(dim, viz_board, data_board)
        self.play(LaggedStart(*(FadeIn(line) for line in lines)))

        self.move_camera(zoom=.5)

        avg_cost: float = calc_avg_cost(
            data_board, self.linear_greedy_solver.pairs)

        score_text: Text = Text(
            f"Avg ABS DIFF: {avg_cost}", font_size=24).move_to(viz_board.get_edge_center(UP), aligned_edge=DOWN).shift(UP)

        self.play(FadeIn(score_text))

        self.next_slide()
        reset_slide(self)

        self.slide_tracker.inc()
        show_slide_number(self)

        costs: list[float] = [
            1., 3.,   5.,  7., 2., 4.,
            2., 4.,   8.,  9., 5., 7.,
            3., 5.,   8.,  4., 8., 6.,
            6., 8.,  10.,  9., 1., 1.,
            5., 11., 15., 15., 9., 5.,
            1., 12., 18.,  3., 2., 3.,
        ]
        viz_board: VGroup = self._create_board(dim, cost_range)
        self.board_generator.boards[-1] = (costs, dim)
        data_board: Tiles = self.board_generator.boards[-1][0]

        self.play(FadeIn(viz_board))

        lines = self.linear_greedy_solver.solve(dim, viz_board, data_board)
        self.play(LaggedStart(*(FadeIn(line) for line in lines)))

        self.play(
            Circumscribe(viz_board[30]),
            Circumscribe(viz_board[35]),
            Blink(Cross(viz_board[30]).scale(.5), blinks=3),
            Blink(Cross(viz_board[35]).scale(.5), blinks=3),
        )

        self.next_slide()
        self.slide_tracker.inc()
        reset_slide(self)

    def intro(self) -> None:
        title: Text = Text("Sabrina's Game", font_size=64)

        show_slide_number(self)

        self.play(title.animate.shift(UP))

        rules: VGroup = VGroup()
        rules.add(Text("Try to get the lowest avg abs diff", font_size=24))
        rules.add(Text("Tile as many boards as you can", font_size=24))
        rules.add(Text("Selected difficulty: 2 x 1 tiles", font_size=24))

        self.play(rules.animate.arrange(DOWN, center=False))

        self.next_slide()
        self.slide_tracker.inc()
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
