from manim import *
from manim_slides.slide import ThreeDSlide
from viz.utils.tile import Tile
from typing import cast

config["max_files_cached"] = -1


class OddBoardsSlide(ThreeDSlide):
    skip_reversing = True

    boards: list[VGroup] = []

    def construct(self) -> None:
        self.monkey()
        self.analysis()
        self.reason()
        self.psuedo()

    def psuedo(self) -> None:
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=.5)

        board: Rectangle = self.create_board(8, 9)

        slide_number: Text = Text("7/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(Write(slide_number))

        self.play(Create(board))
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

        row = 0
        w, h = 8, 9
        col = 0
        while col < w:
            a, b = (1, 2)
            x, y, _ = board.get_corner(UL) + (.5, -1, 0.)
            tile = Tile(a, b, x + col, y - row, 0.)
            self.play(FadeIn(tile.visual, run_time=.2))
            col += 1

        code_text = """
        Tile from left to right
        Row += 2
        """
        t_code = Code(code_string=code_text).move_to(
            board.get_right() + 5).shift(DOWN * 2)
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        row += 2
        col = 0
        while col < w:
            a, b = (1, 2)
            x, y, _ = board.get_corner(UL) + (.5, -1, 0.)
            tile = Tile(a, b, x + col, y - row, 0.)
            self.play(FadeIn(tile.visual, run_time=.2))
            col += 1

        code_text = """
        While board not filled:
            Tile from left to right
            Row += 2
        """
        t_code = Code(code_string=code_text).move_to(
            board.get_right() + 5).shift(DOWN * 2)
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        row += 2
        col = 0
        while row != h:
            if row + 1 == h:
                break
            col = 0
            while col < w:
                a, b = (1, 2)
                x, y, _ = board.get_corner(UL) + (.5, -1, 0.)
                tile = Tile(a, b, x + col, y - row, 0.)
                self.play(FadeIn(tile.visual, run_time=.2))
                col += 1
            row += 2

        code_text = """
        While board not filled:
            If tile can't fit:
			    Rotate(Tile, 90 degrees)

            Tile from left to right
            Row += 2
        """
        t_code = Code(code_string=code_text).move_to(
            board.get_right() + 5).shift(DOWN * 2)
        self.play(ReplacementTransform(code, t_code))
        code = t_code

        col = 0
        row -= 1
        while col < w:
            x, y, _ = board.get_corner(UL) + (1., -1.5, 0.)
            a, b = (2, 1)
            if col + 1 == w:
                self.play(
                    Blink(Cross(Square(1).scale(.5)).move_to((x + col - .5, y - row, 0.))))
                break

            tile = Tile(a, b, x + col, y - row, 0.)
            self.play(FadeIn(tile.visual, run_time=.2))
            col += 2

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

        slide_number: Text = Text("6/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(Write(slide_number))

        self.play(grouped.animate.arrange())
        self.move_camera(frame_center=grouped)

        self.next_section()

        boards.insert(0, self.create_labelled_board(1, 1, BLUE_A))
        grouped = VGroup(boards)

        self.play(grouped.animate.arrange())
        self.move_camera(frame_center=grouped)

        for i in range(1, len(boards)):
            self.move_camera(frame_center=boards[i])
            self.primitive_tile(i + 1, i + 1, cast(Rectangle, boards[i][0]))

        self.move_camera(frame_center=grouped)

        self.next_section()

        self.fade_all_out()

        self.wait()

    def primitive_tile(self, w: int, h: int, board: Rectangle) -> list[Tile]:
        tiles: list[Tile] = []

        rotate = False
        row = 0
        while not rotate and row != h:
            if row > h or row + 1 == h:
                rotate = True
                row -= 1
            col = 0
            while col < w:
                a, b = (1, 2)
                x, y, _ = board.get_corner(UL) + (.5, -1, 0.)
                if rotate:
                    a, b = (2, 1)
                    x += .5
                    y -= .5

                    if col + 1 == w:
                        self.play(
                            Blink(Cross(Square(1).scale(.5)).move_to((x + col - .5, y - row, 0.))))
                        break

                tile = Tile(a, b, x + col, y - row, 0.)

                tiles.append(tile)
                self.play(FadeIn(tile.visual, run_time=.2))
                board.add(tile.visual)

                if rotate:
                    col += 1
                col += 1

            row += 2

        return tiles

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

        slide_number: Text = Text("5/24").move_to(DOWN * 7. + RIGHT * 13.)

        self.play(Write(slide_number))

        self.next_section()

        t_table: Table = Table(
            [
                [str(3 * 3), "FAIL"],
                [str(5 * 5), "FAIL"],
                [str(7 * 7), "FAIL"],
                [str(9 * 9), "FAIL"],
                [str(11 * 11), "FAIL"],
                [str(13 * 13), "FAIL"],
                [str(15 * 15), "FAIL"],
                [str(17 * 17), "FAIL"],
                ["...", "..."],
            ],
            col_labels=[Text("Grid Size"), Text("Passed")],
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": BLUE_A}
        ).scale(.5)
        self.play(
            ReplacementTransform(table, t_table)
        )
        table = t_table

        self.next_section()
        self.play(FadeOut(table), FadeOut(slide_number))

    def monkey(self) -> None:
        boards = [
            self.create_labelled_board(5, 5, BLUE_A),
            self.create_labelled_board(3, 3, BLUE_B).move_to((0., 0., 1.)),
        ]

        self.set_camera_orientation(
            phi=75 * DEGREES, theta=-60 * DEGREES, zoom=.5)

        self.play(Create(board, run_time=2, lag_ratio=.1) for board in boards)

        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=.5)

        slide_number: Text = Text("3/24").move_to(DOWN * 7. + RIGHT * 13.)

        self.play(Write(slide_number))

        self.play(
            boards[i].animate.move_to((i * 5, 0., 0.)) for i in range(len(boards))
        )

        self.next_slide()
        t_slide_number: Text = Text("4/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(ReplacementTransform(slide_number, t_slide_number))
        slide_number = t_slide_number

        self.play(
            FadeOut(board) for board in boards
        )

        passes_header: VGroup = self.create_table_row("Grid Size", "PASS/FAIL")

        self.play(FadeIn(passes_header))

        self.move_camera(frame_center=passes_header)

        self.next_section()

        self.play(FadeOut(passes_header), FadeOut(slide_number))

        pass_fail_rows: list[VGroup] = []

        pass_fail_rows.append(self.create_pass_fail_row(boards, 6, 5, "PASS"))
        self.play(FadeIn(pass_fail_rows[-1]))
        self.move_camera(frame_center=pass_fail_rows[-1])

        pass_fail_rows.append(self.create_pass_fail_row(boards, 5, 6, "PASS"))
        bottom = pass_fail_rows[-2].get_bottom()
        bottom[1] -= 3
        pass_fail_rows[-1].move_to(bottom)
        self.move_camera(frame_center=pass_fail_rows[-1], zoom=.6)
        self.play(FadeIn(pass_fail_rows[-1], run_time=.3))

        pass_fail_rows.append(self.create_pass_fail_row(boards, 6, 6, "PASS"))
        bottom = pass_fail_rows[-2].get_bottom()
        bottom[1] -= 3
        pass_fail_rows[-1].move_to(bottom)
        self.move_camera(frame_center=pass_fail_rows[-1])
        self.play(FadeIn(pass_fail_rows[-1], run_time=.3))

        pass_fail_rows.append(self.create_pass_fail_row(boards, 6, 7, "PASS"))
        bottom = pass_fail_rows[-2].get_bottom()
        bottom[1] -= 3
        pass_fail_rows[-1].move_to(bottom)
        self.move_camera(frame_center=pass_fail_rows[-1])
        self.play(FadeIn(pass_fail_rows[-1], run_time=.3))

        pass_fail_rows.append(self.create_pass_fail_row(boards, 7, 6, "PASS"))
        bottom = pass_fail_rows[-2].get_bottom()
        bottom[1] -= 3
        pass_fail_rows[-1].move_to(bottom)
        self.move_camera(frame_center=pass_fail_rows[-1])
        self.play(FadeIn(pass_fail_rows[-1], run_time=.3))

        pass_fail_rows.append(self.create_pass_fail_row(boards, 7, 7, "FAIL"))
        bottom = pass_fail_rows[-2].get_bottom()
        bottom[1] -= 3
        pass_fail_rows[-1].move_to(bottom)
        self.move_camera(frame_center=pass_fail_rows[-1], zoom=.5)
        self.play(FadeIn(pass_fail_rows[-1], run_time=.3))
        self.play(Circumscribe(pass_fail_rows[-1], color=RED_A))

        pass_fail_rows.append(self.create_pass_fail_row(boards, 7, 8, "PASS"))
        bottom = pass_fail_rows[-2].get_bottom()
        bottom[1] -= 3
        pass_fail_rows[-1].move_to(bottom)
        self.move_camera(frame_center=pass_fail_rows[-1])
        self.play(FadeIn(pass_fail_rows[-1], run_time=.2))

        pass_fail_rows.append(self.create_pass_fail_row(boards, 8, 7, "PASS"))
        bottom = pass_fail_rows[-2].get_bottom()
        bottom[1] -= 3
        pass_fail_rows[-1].move_to(bottom)
        self.move_camera(frame_center=pass_fail_rows[-1])
        self.play(FadeIn(pass_fail_rows[-1], run_time=.2))

        pass_fail_rows.append(self.create_pass_fail_row(boards, 8, 8, "PASS"))
        bottom = pass_fail_rows[-2].get_bottom()
        bottom[1] -= 3
        pass_fail_rows[-1].move_to(bottom)
        self.move_camera(frame_center=pass_fail_rows[-1])
        self.play(FadeIn(pass_fail_rows[-1], run_time=.2))

        text = Text("...").scale(2)
        bottom = pass_fail_rows[-2].get_bottom()
        bottom[1] -= 10
        text.move_to(bottom)
        self.move_camera(frame_center=text)
        for _ in range(3):
            self.play(ApplyWave(text))

        self.fade_all_out()

        self.move_camera(frame_center=(0., 0., 0.))

        self.wait()

    def fade_all_out(self, run_time=.2) -> None:
        self.play(
            *[FadeOut(mob, run_time=run_time)for mob in self.mobjects]
        )

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
