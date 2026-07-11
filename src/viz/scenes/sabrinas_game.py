from manim import *
from manim_slides.slide import ThreeDSlide
from random import randrange, seed as rand_seed
from viz.utils.tile import Cell
from typing import cast
config["max_files_cached"] = -1


class SabrinasGame(ThreeDSlide):
    skip_reversing = True

    _required_tiles: int = 0
    _curr_num_tiles: int = 0

    def construct(self) -> None:
        rand_seed(42)

        self.intro()
        self.next_section()
        self.fade_all_out()

        self.move_camera(zoom=1.)
        self.problem()
        self.next_section()
        self.fade_all_out()

        self.move_camera(zoom=1.)
        self.psuedo()
        self.next_section()
        self.fade_all_out()

        self.move_camera(zoom=1.)
        self.demo()
        self.next_section()
        self.fade_all_out()

        self.move_camera(zoom=1.)
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

        slide_number: Text = Text("20/24").move_to(DOWN * 7. + RIGHT * 13.)

        self.play(Write(slide_number), Create(code, run_time=3))

        self.move_camera(zoom=.5)

        comp: Text = Text("O(N)").move_to(
            code.get_edge_center(DOWN))

        self.play(code.animate.shift(UP * 2))
        self.play(Write(comp))

        self.next_slide()
        t_slide_number: Text = Text("21/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(FadeOut(comp), ReplacementTransform(
            slide_number, t_slide_number))
        slide_number = t_slide_number

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

        comp = comp.move_to(
            code.get_edge_center(DOWN)).shift(shift)

        self.play(code.animate.shift(UP))
        self.play(Write(comp))

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
        self.fade_all_out()

        t_slide_number: Text = Text("22/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(ReplacementTransform(slide_number, t_slide_number))
        slide_number = t_slide_number

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

    def demo(self) -> None:
        w: int = 6
        h: int = 6
        costs = [
            1, 3,   5,  7, 2, 4,
            2, 4,   8,  9, 5, 7,
            3, 5,   8,  4, 8, 6,
            6, 8,  10,  9, 1, 1,
            5, 11, 15, 15, 9, 5,
            1, 12, 18,  3, 2, 3,
        ]
        self._required_tiles = (6 * 6) // 2
        self._curr_num_tiles = 0
        board, _ = self.create_board(w, h, costs)
        pairs: list[int | None] = [None for _ in range(w * h)]
        cells: list[Cell] = self.create_neighbors(w, h, costs)

        slide_number: Text = Text("19/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(Write(slide_number), FadeIn(board))

        history = []
        self.dfs_solve(cells, pairs, history)

        step_tracker = ValueTracker(0)
        num_steps = len(history) - 1

        visible_lines = VGroup()
        self.add(board, visible_lines)

        def update_lines(mobject):
            current_step = int(step_tracker.get_value())
            current_pairs = history[current_step]

            mobject.remove(*mobject.submobjects)

            seen = set()
            for start, neighbor in enumerate(current_pairs):
                if neighbor is not None and (start, neighbor) not in seen:
                    seen.add((start, neighbor))
                    seen.add((neighbor, start))

                    line = Line(
                        board[start].get_center(),
                        board[neighbor].get_center(),
                        buff=MED_SMALL_BUFF,
                        color=BLACK
                    )
                    mobject.add(line)

        visible_lines.add_updater(update_lines)

        self.play(
            step_tracker.animate.set_value(num_steps),
            run_time=10,
            rate_func=linear
        )

        self.move_camera(zoom=.5)

        avg_cost: float = self.calc_avg_cost(cells, pairs)

        score_text: Text = Text(
            f"Avg ABS DIFF: {avg_cost}", font_size=24).move_to(board.get_edge_center(UP), aligned_edge=DOWN).shift(UP)

        self.play(FadeIn(score_text))

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

        slide_number: Text = Text("17/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(Write(slide_number))

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
        t_slide_number: Text = Text("18/24").move_to(DOWN * 7. + RIGHT * 13.)

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
        self.play(ReplacementTransform(code, t_code),
                  ReplacementTransform(slide_number, t_slide_number))
        slide_number = t_slide_number

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

    def problem(self) -> None:
        w: int = 6
        h: int = 6
        board, costs = self.create_board(w, h)
        pairs: list[int | None] = [None for _ in range(w * h)]
        cells: list[Cell] = self.create_neighbors(w, h, costs)

        slide_number: Text = Text("15/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(Write(slide_number), FadeIn(board))

        self.next_section()

        self.greedy_tile(cells, pairs, board)

        self.move_camera(zoom=.5)

        avg_cost: float = self.calc_avg_cost(cells, pairs)

        score_text: Text = Text(
            f"Avg ABS DIFF: {avg_cost}", font_size=24).move_to(board.get_edge_center(UP), aligned_edge=DOWN).shift(UP)

        self.play(FadeIn(score_text))

        self.next_slide()
        t_slide_number: Text = Text("16/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(ReplacementTransform(slide_number, t_slide_number))
        slide_number = t_slide_number

        self.fade_all_out()

        costs = [
            1, 3,   5,  7, 2, 4,
            2, 4,   8,  9, 5, 7,
            3, 5,   8,  4, 8, 6,
            6, 8,  10,  9, 1, 1,
            5, 11, 15, 15, 9, 5,
            1, 12, 18,  3, 2, 3,
        ]
        board, _ = self.create_board(w, h)
        pairs = [None for _ in range(w * h)]
        cells = self.create_neighbors(w, h, costs)

        self.play(FadeIn(board))

        self.greedy_tile(cells, pairs, board)

        self.play(
            Circumscribe(board[30]),
            Circumscribe(board[35]),
            Blink(Cross(board[30]).scale(.5), blinks=3),
            Blink(Cross(board[35]).scale(.5), blinks=3),
        )

    def intro(self) -> None:
        title: Text = Text("Sabrina's Game", font_size=64)

        slide_number: Text = Text("14/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(Write(slide_number), FadeIn(title))

        self.play(title.animate.shift(UP))

        rules: VGroup = VGroup()
        rules.add(Text("Try to get the lowest avg abs diff", font_size=24))
        rules.add(Text("Tile as many boards as you can", font_size=24))
        rules.add(Text("Selected difficulty: 2 x 1 tiles", font_size=24))

        self.play(rules.animate.arrange(DOWN, center=False))

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
                    board[i].get_center(), board[j].get_center(), buff=MED_SMALL_BUFF, color=BLACK)
                lines.append(line)
                break

        self.play(Succession(*(FadeIn(line) for line in lines), run_time=1))

        return lines

    def dfs_solve(self, cells: list[Cell], pairs: list[int | None], history: list) -> bool:
        if self._required_tiles == self._curr_num_tiles:
            history.append(pairs.copy())  # Final state
            return True

        start = -1
        for i, pair in enumerate(pairs):
            if pair is None:
                start = i
                break

        if start == -1:
            return False

        for neighbor in cells[start].neighbor_ids:
            if pairs[neighbor] is not None:
                continue

            pairs[neighbor] = start
            pairs[start] = neighbor
            self._curr_num_tiles += 1

            # Current state
            history.append(pairs.copy())

            if self.dfs_solve(cells, pairs, history):
                return True

            pairs[neighbor] = None
            pairs[start] = None
            self._curr_num_tiles -= 1

            # Backtracked state
            history.append(pairs.copy())

        return False

    def fade_all_out(self, run_time=.2) -> None:
        self.play(
            *[FadeOut(mob, run_time=run_time)for mob in self.mobjects]
        )

    def create_textbox(self, content: VMobject, color: ManimColor = WHITE, stroke_color: ManimColor = BLACK) -> VGroup:
        result = VGroup()
        box = Rectangle(
            height=1, width=1, fill_color=color,
            fill_opacity=1, stroke_color=stroke_color,
        )
        cont = content.move_to(box.get_center())
        result.add(box, cont)
        return result

    def create_board(self, w: int, h: int, values: list[int] = []) -> tuple[VGroup, list[int]]:
        if values:
            if w * h != len(values):
                raise Exception("Board size and values size are not equal")

        group: VGroup = VGroup()

        if not values:
            t_v: list[int] = []
            for _ in range(w * h):
                t_v.append(randrange(0, 20))

            values = t_v

        for v in values:
            group.add(self.create_textbox(
                Text(str(v), color=BLACK, font_size=24)))

        return group.arrange_in_grid(h, w, 0.), values

    def create_neighbors(self, w: int, h: int, costs: list[int]) -> list[Cell]:
        result: list[Cell] = []

        for i in range(w * h):
            row: int = i // w
            col: int = i % w

            cell: Cell = Cell(row, col, costs[i])

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
                key=lambda x: abs(cast(int, cell.value) - costs[x])
            )

            result.append(cell)

        return result

    def calc_avg_cost(self, cells: list[Cell], pairs: list[int | None]) -> float:
        avg_cost = 0
        for i in range(len(pairs)):
            pair: int = cast(int, pairs[i])
            if pair > i:
                a: int = cast(int, cells[i].value)
                b: int = cast(int, cells[pair].value)
                avg_cost += abs(a - b)

        return avg_cost / (len(cells) * .5)
