from manim import *
from random import seed as rand_seed
from typing import Any, Generator, cast
from manim_slides.slide import ThreeDSlide
from src.viz.utils.trackers import JSlideNumberTracker
from src.algorithms.utils.core import is_valid_board_size
from src.algorithms.utils.types import ExplicitDims, iVec2D
from src.viz.utils.algorithms.primitive import PrimitiveSolver
from src.viz.utils.algorithms.utils.board_generator import VizBoardGenerator
from src.viz.utils.visual import create_tiles, reset_slide, show_slide_number

config["max_files_cached"] = -1


class OddBoardsSlide(ThreeDSlide):
    skip_reversing = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slide_tracker: JSlideNumberTracker = JSlideNumberTracker(3)
        self.current_slide_number: Text = Text(
            str(self.slide_tracker.current), font_size=32).to_edge(DR)
        self.primitive_solver: PrimitiveSolver = PrimitiveSolver()
        self.color_gen: RandomColorGenerator = RandomColorGenerator(42)

    def construct(self) -> None:
        rand_seed(42)

        self.monkey()
        self.analysis()
        self.reason()
        self.psuedo()

    def psuedo(self) -> None:
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=.5)

        tile_offset: Vector = Vector((-20., 0., 0.))

        board_generator: VizBoardGenerator = VizBoardGenerator()
        dim: iVec2D = iVec2D(8, 9)
        board_generator.generate(ExplicitDims([dim]), (1, 10))
        board: Rectangle = board_generator.viz_boards[0]

        tiles: list[Rectangle] = create_tiles(
            (dim.x * dim.y) // 2, tile_offset, self.color_gen)

        self.slide_tracker.inc()
        show_slide_number(self)

        self.play(Create(board, run_time=2, lag_ratio=.1))
        self.play(board.animate.shift(LEFT * 3))

        code_text: str = """
        # Your code here
        """
        code: Code = Code(code_string=code_text).move_to(
            board.get_right() + 5).shift(DOWN * 2)

        self.play(FadeIn(code))

        code_text = """
        Tile from left to right
        """
        t_code = Code(code_string=code_text).move_to(
            board.get_right() + 5).shift(DOWN * 2)
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        solution_generator: Generator[list[Animation], None,
                                      None] = self.primitive_solver.solve(dim, board, tiles)

        solved_row: list[Animation] = next(solution_generator)
        self.play(*solved_row)

        code_text = """
        Tile from left to right
        Row += 2
        """
        t_code = Code(code_string=code_text).move_to(
            board.get_right() + 5).shift(DOWN * 2)
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        solved_row: list[Animation] = next(solution_generator)
        self.play(*solved_row)

        code_text = """
        While board not filled:
            Tile from left to right
            Row += 2
        """
        t_code = Code(code_string=code_text).move_to(
            board.get_right() + 5).shift(DOWN * 3)
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        for _ in range(2):
            solved_row: list[Animation] = next(solution_generator)
            self.play(*solved_row)

        code_text = """
        While board not filled:
            If tile can't fit:
        		    Rotate(Tile, 90 degrees)

            Tile from left to right
            Row += 2
        """
        t_code = Code(code_string=code_text).move_to(
            board.get_right() + 5).shift(DOWN * 3)
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        solved_row: list[Animation] = [
            animation for animations in solution_generator for animation in animations]
        self.play(*solved_row)

        self.wait(2)

        reset_slide(self)

    def reason(self) -> None:
        boards = [
            self.create_labelled_board(2, 2, BLUE_A),
            self.create_labelled_board(3, 3, BLUE_B),
            self.create_labelled_board(4, 4, BLUE_C),
            self.create_labelled_board(5, 5, BLUE_D),
            self.create_labelled_board(6, 6, BLUE_E),
        ]

        self.set_camera_orientation(
            phi=75 * DEGREES, theta=-60 * DEGREES, zoom=.5)

        self.play(
            FadeIn(boards[i].move_to((0., 0., i * -1.))) for i in range(-1, -len(boards), -1)
        )

        grouped = VGroup(boards)

        self.move_camera(phi=0, theta=-90 * DEGREES)

        self.slide_tracker.inc()
        show_slide_number(self)

        self.play(grouped.animate.arrange())
        self.move_camera(frame_center=grouped)

        self.next_section()

        boards.insert(0, self.create_labelled_board(1, 1, BLUE_A))
        grouped = VGroup(boards)

        self.play(grouped.animate.arrange())
        self.move_camera(frame_center=grouped)

        tile_offset: Vector = Vector((0., 10., 0.))

        for i, board_group in enumerate(boards):
            board: Rectangle = cast(Rectangle, board_group[0])
            self.move_camera(frame_center=board)
            w, h = i + 1, i + 1
            tiles: list[Rectangle] = create_tiles(
                (w * h) // 2, tile_offset, self.color_gen)
            animations: list[Animation] = [animation for animations in self.primitive_solver.solve(
                iVec2D(w, h), board, tiles) for animation in animations]

            if animations:
                self.play(LaggedStart(*animations))

            if not is_valid_board_size(iVec2D(w, h)):
                x, y, _ = board.get_corner(DR) + (-.5, .5, 0.)
                self.play(
                    Blink(Cross(Square(1).scale(.5)).move_to((x, y, 0)))
                )

        self.move_camera(frame_center=grouped)

        self.next_slide()

        reset_slide(self)

    def analysis(self) -> None:
        table: Table = Table(
            [
                ["3 x 3", "FAIL"],
                ["5 x 5", "FAIL"],
                ["7 x 7", "FAIL"],
                ["9 x 9", "FAIL"],
                ["11 x 11", "FAIL"],
                ["13 x 13", "FAIL"],
                ["15 x 15", "FAIL"],
                ["17 x 17", "FAIL"],
                ["...", "..."],
            ],
            col_labels=[Text("Grid Size"), Text("Passed")],
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": BLUE_A}
        ).scale(.5)

        self.play(FadeIn(table))

        self.slide_tracker.inc()
        show_slide_number(self)

        self.next_slide()

        reset_slide(self)

    def monkey(self) -> None:
        show_slide_number(self, update=False)

        boards = [
            self.create_labelled_board(5, 5, BLUE_A),
            self.create_labelled_board(3, 3, BLUE_B).move_to((0., 0., 1.)),
        ]

        self.set_camera_orientation(
            phi=75 * DEGREES, theta=-60 * DEGREES, zoom=.5)

        self.play(Create(board, run_time=2, lag_ratio=.1) for board in boards)

        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=.5)

        self.play(
            boards[i].animate.move_to((i * 5, 0., 0.)) for i in range(len(boards))
        )

        self.next_slide()
        self.slide_tracker.inc()
        show_slide_number(self)

        self.play(
            FadeOut(board) for board in boards
        )

        passes_header: VGroup = self.create_table_row("Grid Size", "PASS/FAIL")

        self.play(FadeIn(passes_header))

        self.move_camera(frame_center=passes_header)

        self.next_section()

        self.play(FadeOut(passes_header))

        dims: list[iVec2D] = [
            iVec2D(6, 5),
            iVec2D(5, 6),
            iVec2D(6, 6),
            iVec2D(6, 7),
            iVec2D(7, 6),
            iVec2D(7, 7),
            iVec2D(7, 8),
            iVec2D(8, 7),
            iVec2D(8, 8),
        ]

        last_row: VGroup | None = None
        for dim in dims:
            valid: bool = is_valid_board_size(dim)

            row: VGroup = self.create_pass_fail_row(
                boards, *dim, "PASS" if valid else "FAIL")

            if last_row:
                bottom = last_row.get_bottom()
                bottom[1] -= 3
                row.move_to(bottom)

            self.move_camera(frame_center=row)
            self.play(FadeIn(row, run_time=.2))

            if not valid:
                self.play(Circumscribe(row, color=RED_A))

            last_row = row

        text = Text("...").scale(2)
        if last_row:
            bottom = last_row.get_bottom()
            bottom[1] -= 10
            text.move_to(bottom)
        self.move_camera(frame_center=text)

        for _ in range(3):
            self.play(ApplyWave(text))

        reset_slide(self)

        self.next_slide()

    def create_pass_fail_row(self, boards: list[VGroup], w: int, h: int, state: str) -> VGroup:
        boards.append(self.create_labelled_board(w, h, BLUE_B).scale(.5))

        current_row: VGroup = self.create_table_row(f"{w} x {h}", state)
        current_board: VGroup = boards[-1]
        side = current_row.get_right()
        side[0] += 10
        current_board.move_to(side)

        current_group: VGroup = VGroup()
        return current_group.add(current_row, current_board)

    def create_table_row(self, before_eq: str, after_eq: str) -> VGroup:
        result = VGroup()
        text1 = Text(before_eq)
        text2 = Text(after_eq).move_to((5., 0., 0.))
        return result.add(text1, text2)

    def create_labelled_board(self, w: int, h: int, color: ManimColor) -> VGroup:
        result = VGroup()
        box = self.create_board(w, h, color)
        box_top = box.get_top()
        box_top[1] += 1
        text = Text(f"{w} x {h}").move_to(box_top)
        return result.add(box, text)

    def create_board(self, w: int, h: int, color: ManimColor = BLUE_A) -> Rectangle:
        return Rectangle(
            width=w, height=h, fill_color=color,
            grid_xstep=1.0, grid_ystep=1.0, stroke_color=color
        )
