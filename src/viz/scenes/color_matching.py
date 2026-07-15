from manim import *
from typing import Any, cast
from random import seed as rand_seed
from manim_slides.slide import ThreeDSlide
from src.viz.utils.trackers import JSlideNumberTracker
from src.viz.utils.visual import reset_slide, show_slide_number
from src.viz.utils.algorithms.linear_greedy import LinearGreedySolver
from tiling_algorithms.utils.types import Tiles, iVec2D, ExplicitDims
from src.viz.utils.algorithms.utils.board_generator import VizBoardGenerator

config["max_files_cached"] = -1


class ColorMatching(ThreeDSlide):
    skip_reversing = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.color_gen: RandomColorGenerator = RandomColorGenerator(
            42, sample_colors=[RED_A, RED_C, RED_E, BLUE_C, BLUE_D, BLUE_E])
        self.board_generator: VizBoardGenerator = VizBoardGenerator()
        self.slide_tracker: JSlideNumberTracker = JSlideNumberTracker(8)
        self.current_slide_number: Text = Text(
            str(self.slide_tracker.current), font_size=32).to_edge(DR)
        self.linear_greedy_solver: LinearGreedySolver = LinearGreedySolver(
            self.color_gen)

    def construct(self) -> None:
        rand_seed(42)

        self.intro()
        self.algorithm()

    def algorithm(self) -> None:

        dim: iVec2D = iVec2D(4, 5)
        board: VGroup = self.create_board(dim)

        self.set_camera_orientation(zoom=.5)

        self.slide_tracker.inc()
        show_slide_number(self)

        code: Code = Code(
            code_string="# Your code here",
            add_line_numbers=False
        )

        self.play(
            Create(board.shift(LEFT * 5)),
            FadeIn(code.shift(RIGHT * 5))
        )

        lines: list[Line] = self.linear_greedy_solver.solve(dim,
                                                            board, self.board_generator.boards[-1][0])

        self.wait(2)

        t_code: Code = Code(
            code_string="""
            For every cell in board:
                For value in neighbor:
                    if ABS(DIFF(value, current cell)):
                        Match(cell, neighbor)
            """,
        ).shift(RIGHT * 7)
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        self.wait(2)

        t_code = Code(
            code_string="""
            For every unpaired cell in board:
                sort neighbors by ABS DIFF

                if neighbor not matched:
                    Match(cell, neighbor)
            """,
        ).shift(RIGHT * 7)
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        self.play(LaggedStart(*(FadeIn(line) for line in lines), run_time=3))

        self.next_section()

        self.play(FadeOut(*lines, code))

        self.slide_tracker.inc()
        show_slide_number(self)

        self.move_camera(zoom=.2)

        for i in range(6, 12, 2):
            dim = iVec2D(i, i)
            t_board: VGroup = self.create_board(dim)

            self.play(ReplacementTransform(board, t_board))
            board = t_board

            lines = self.linear_greedy_solver.solve(dim,
                                                    board, self.board_generator.boards[-1][0])
            self.play(LaggedStart(*(FadeIn(line) for line in lines)))

            self.wait(1)

            if i != 10:
                self.play(FadeOut(*lines))

        self.next_slide()
        self.slide_tracker.inc()
        show_slide_number(self)

        score_text: Text = Text(
            f"Avg ABS DIFF: ").move_to(board.get_center()).shift(UP * 15)

        self.play(Create(score_text))

    def intro(self) -> None:
        title: Text = Text("\"Close Enough\" Matching")

        self.play(FadeIn(title))
        show_slide_number(self, update=False)

        self.next_slide()
        self.slide_tracker.inc()
        show_slide_number(self)

        self.play(FadeOut(title))

        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=.5)

        dim: iVec2D = iVec2D(5, 5)
        board: VGroup = self.create_board(dim)

        self.play(Create(board, run_time=2))

        self.next_section()

        generated_board: Tiles = self.board_generator.boards[-1][0]
        curr_col: int = cast(
            ManimColor, self.color_gen.colors[int(generated_board[0])]).to_integer()
        curr_next: int = cast(
            ManimColor, self.color_gen.colors[int(generated_board[1])]).to_integer()
        curr_bot: int = cast(
            ManimColor, self.color_gen.colors[int(generated_board[5])]).to_integer()

        if abs(curr_col - curr_next) < abs(curr_col - curr_bot):
            self.play(Circumscribe(
                VGroup(cast(Square, board[0]), cast(Square, board[1])), run_time=4))
        else:
            self.play(Circumscribe(
                VGroup(cast(Square, board[0]), cast(Square, board[5])), run_time=4))

        self.slide_tracker.inc()
        show_slide_number(self)

        self.play(FadeOut(board))

        color_band: Line = Line(start=LEFT * 3, end=RIGHT * 3,
                                fill_opacity=1, stroke_width=10).set_color(cast(ParsableManimColor, [BLUE_C, RED_E]))
        self.play(Create(color_band))

        self.next_section()

        code: Code = Code(code_string="ABS(DIFF(A, B))",
                          add_line_numbers=False)

        self.play(FadeIn(code.shift(UP * 2)))

        self.next_section()

        reset_slide(self)

    def create_board(self, dim: iVec2D) -> VGroup:
        self.board_generator.generate(ExplicitDims(
            [dim]), (0, len(self.color_gen.colors) - 1))

        group: VGroup = VGroup()
        for i in range(dim.x * dim.y):
            square: Square = Square(fill_color=self.color_gen.colors[int(
                self.board_generator.boards[-1][0][i])], fill_opacity=1.)
            square.add(Text(str(i)).scale(.5))
            group.add(square)

        return group.arrange_in_grid(rows=dim.y, cols=dim.x, buff=0.)
