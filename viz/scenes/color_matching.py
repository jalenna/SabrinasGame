from manim import *
from manim_slides.slide import ThreeDSlide
from viz.utils.tile import Cell
from typing import cast
config["max_files_cached"] = -1


class ColorMatching(ThreeDSlide):
    skip_reversing = True

    def construct(self) -> None:
        self.intro()
        self.algorithm()

    def algorithm(self) -> None:
        w: int = 4
        h: int = 5
        board: VGroup = self.create_board(w, h)
        cells: list[Cell] = self.create_neighbors(w, h, board)
        pairs: list[int | None] = [None for _ in range(w * h)]

        self.set_camera_orientation(zoom=.5)

        code: Code = Code(
            code_string="# Your code here",
            add_line_numbers=False
        )

        self.play(
            Create(board.shift(LEFT * 5)),
            FadeIn(code.shift(RIGHT * 5))
        )

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

        self.next_section()

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

        self.next_section()

        self.greedy_tile(cells, pairs, board)

        self.next_section()

        self.fade_all_out()

        w = 6
        h = 6
        t_board: VGroup = self.create_board(w, h)
        cells = self.create_neighbors(w, h, t_board)
        pairs = [None for _ in range(w * h)]

        self.play(ReplacementTransform(board, t_board))
        board = t_board

        lines: list[Line] = self.greedy_tile(cells, pairs, board)

        self.next_section()

        seq = [FadeOut(line) for line in lines]
        self.play(Succession(*seq, run_time=.2))

        w = 8
        h = 8
        t_board = self.create_board(w, h)
        cells = self.create_neighbors(w, h, t_board)
        pairs = [None for _ in range(w * h)]

        self.move_camera(zoom=.2)
        self.play(ReplacementTransform(board, t_board))
        board = t_board

        lines = self.greedy_tile(cells, pairs, board)

        self.next_section()

        seq = [FadeOut(line) for line in lines]
        self.play(Succession(*seq, run_time=.2))

        w = 10
        h = 10
        t_board = self.create_board(w, h)
        cells = self.create_neighbors(w, h, t_board)
        pairs = [None for _ in range(w * h)]

        self.play(ReplacementTransform(board, t_board))
        board = t_board

        lines = self.greedy_tile(cells, pairs, board)

        self.next_section()

        avg_cost: int = self.calc_avg_cost(board, cast(list[int], pairs))

        score_text: Text = Text(
            f"Avg ABS DIFF: ").move_to(board.get_center()).shift(UP * 15)
        score_color: Square = Square(fill_opacity=1., color=BLACK, stroke_color=BLACK).shift(UP * 13).animate.set_color(
            ManimColor(avg_cost))

        self.play(Create(score_text))
        self.play(score_color)

        self.next_section()

        self.fade_all_out()

    def calc_avg_cost(self, board: VGroup, pairs: list[int]) -> int:
        avg_cost = 0
        for i in range(len(pairs)):
            if cast(int, pairs[i]) > i:
                a = board[i].get_color().to_integer()
                b = board[pairs[i]].get_color().to_integer()

                avg_cost += abs(a - b)
        return avg_cost

    def fade_all_out(self, run_time=.2) -> None:
        self.play(
            *[FadeOut(mob, run_time=run_time)for mob in self.mobjects]
        )

    def intro(self) -> None:
        title: Text = Text("\"Close Enough\" Matching")

        self.play(FadeIn(title))

        self.next_section()

        self.play(FadeOut(title))

        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=.5)

        board: VGroup = self.create_board(5, 5)

        self.play(Create(board, run_time=.3))

        self.next_section()

        curr_col: int = cast(ManimColor, board[0].color).to_integer()
        curr_next: int = cast(ManimColor, board[1].color).to_integer()
        curr_bot: int = cast(ManimColor, board[5].color).to_integer()

        if abs(curr_col - curr_next) < abs(curr_col - curr_bot):
            self.play(Circumscribe(
                VGroup(cast(Square, board[0]), cast(Square, board[1])), run_time=4))
        else:
            self.play(Circumscribe(
                VGroup(cast(Square, board[0]), cast(Square, board[5])), run_time=4))

        self.play(FadeOut(board))

        color_band: Line = Line(start=LEFT * 3, end=RIGHT * 3,
                                fill_opacity=1).set_color(cast(ParsableManimColor, [BLUE_C, RED_E]))
        self.play(Create(color_band))

        self.next_section()

        code: Code = Code(code_string="ABS(DIFF(A, B))",
                          add_line_numbers=False)

        self.play(FadeIn(code))

        self.wait(2)

        self.play(
            FadeOut(color_band),
            FadeOut(code)
        )

    def create_board(self, w: int, h: int) -> VGroup:
        rng: RandomColorGenerator = RandomColorGenerator(seed=42,
                                                         sample_colors=[RED_A, RED_C, RED_E, BLUE_C, BLUE_D, BLUE_E])

        group: VGroup = VGroup(Square(fill_color=rng.next(), fill_opacity=1)
                               for _ in range(w * h))

        return group.arrange_in_grid(h, w, 0.)

    def create_neighbors(self, w: int, h: int, board: VGroup) -> list[Cell]:
        result: list[Cell] = []

        for i in range(w * h):
            row: int = i // w
            col: int = i % w

            cell: Cell = Cell(row, col, board[i].get_color())

            # Left
            if col > 0:
                cell.neighbor_ids.append(i - 1)
            # Right
            if col + 1 < w:
                cell.neighbor_ids.append(i + 1)
            # Up
            if row > 0:
                cell.neighbor_ids.append(i - w)
            # Down
            if row + 1 < h:
                cell.neighbor_ids.append(i + w)

            cell.neighbor_ids.sort(
                key=lambda x: abs(cast(ManimColor, cell.value).to_integer() - board[x].get_color().to_integer()))

            result.append(cell)

        return result

    def greedy_tile(self, cells: list[Cell], pairs: list[int | None], board: VGroup) -> list[Line]:
        lines: list[Line] = []

        for i in range(len(cells)):
            if pairs[i] is not None:
                continue

            for j in cells[i].neighbor_ids:
                if pairs[j] is not None:
                    continue

                pairs[i] = j
                pairs[j] = i
                line: Line = Line(
                    board[i].get_center(), board[j].get_center(), buff=0., color=BLACK)
                lines.append(line)
                self.play(FadeIn(line, run_time=0.2))
                break

        return lines
