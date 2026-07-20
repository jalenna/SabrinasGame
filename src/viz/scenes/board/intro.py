from manim import *
from src.viz.utils.visual import BasePresentation, create_pairings, reset_slide
from SabrinasGame.src.tiling_algorithms.utils.core import absdiff, create_neighbors
from SabrinasGame.src.tiling_algorithms.utils.types import Neighbors, Tiles, iVec2D, ExplicitDims


def board_intro_slide(slide: BasePresentation) -> None:
    goals(slide)
    rules(slide)


def goals(slide: BasePresentation) -> None:

    slide.board_generator.generate(
        ExplicitDims([slide.problematic_tiles_dim]),
        slide.cost_range,
        tiles=slide.problematic_tiles
    )
    visual_board: VGroup = slide.board_generator.visual_boards[-1]
    neighbors: Neighbors = create_neighbors(
        slide.problematic_tiles_dim, slide.problematic_tiles, absdiff)

    slide.depth_solver.solver.solve(
        slide.problematic_tiles, neighbors, slide.problematic_tiles_dim)
    slide.linear_solver.solve(
        slide.problematic_tiles_dim, slide.problematic_tiles)

    visual_pairs_correct: VGroup = VGroup(create_pairings(
        visual_board, slide.depth_solver.solver.pairs))
    visual_pairs_incorrect: VGroup = VGroup(create_pairings(
        visual_board, slide.linear_solver.pairs))

    title: Text = Text("Sabrina's Game")

    goal_group: VGroup = VGroup(
        [
            Text(text,
                 font_size=20,
                 should_center=False,
                 line_spacing=1,
                 ) for text in [
                "Goal:\nGiven a board of weighted cells:",
                "\t- Completely tile the board: no gaps",
                "\t- Score as low as possible",
            ]
        ]
    )

    goal_group.arrange_in_grid(3, 1, col_alignments="l")
    goal_group.center()
    goal_group.to_edge(LEFT)

    visual_board.next_to(goal_group)
    visual_pairs_incorrect.move_to(visual_board)
    visual_pairs_correct.move_to(visual_board)

    slide.play(FadeIn(title))

    slide.next_section()

    slide.play(title.animate.scale(.75))
    slide.play(title.animate.to_corner(UL))

    slide.play(FadeIn(goal_group[0]), Create(visual_board))
    slide.play(FadeIn(goal_group[1]))

    slide.wait(1)

    slide.play(
        FadeIn(
            visual_pairs_incorrect
        )
    )
    slide.play(
        Circumscribe(visual_board[30]),
        Blink(Cross(visual_board[30]), blinks=2, hide_at_end=True),
        Circumscribe(visual_board[35]),
        Blink(Cross(visual_board[35]), blinks=2, hide_at_end=True),
    )
    slide.play(
        FadeOut(
            visual_pairs_incorrect
        ),
        FadeIn(visual_pairs_correct)
    )
    slide.play(
        Circumscribe(
            VGroup(visual_board[30], visual_board[31]), color=GREEN, run_time=2),
        Circumscribe(
            VGroup(visual_board[34], visual_board[35]), color=GREEN, run_time=2),
    )

    slide.next_section()

    slide.play(FadeIn(goal_group[2]))

    slide.play(FadeOut(visual_board))
    slide.play(visual_pairs_correct.animate.arrange(DOWN))
    slide.play(visual_pairs_correct.animate.scale(0.1))

    pairs_brace: Brace = Brace(visual_pairs_correct, direction=RIGHT)
    sum_text: Text = Text("AVG(SUM(T)))\nT=ABS(DIFF(a, b)", font_size=24)
    sum_text.next_to(pairs_brace, RIGHT)
    slide.play(FadeIn(pairs_brace), FadeIn(sum_text))

    slide.play(goal_group.animate.shift(UP))

    slide.next_slide()
    slide.slide_tracker.inc()

    slide.play(FadeOut(title, pairs_brace, sum_text, visual_pairs_correct))

    slide.play(goal_group.animate.to_corner(UL))


def rules(slide: BasePresentation) -> None:

    dim: iVec2D = iVec2D(4, 4)
    slide.board_generator.clear()
    slide.board_generator.generate(ExplicitDims([dim]), slide.cost_range)

    visual_board: VGroup = slide.board_generator.visual_boards[-1]

    rule_group: VGroup = VGroup(
        [
            Text(text,
                 font_size=20,
                 should_center=False,
                 line_spacing=1,
                 ) for text in [
                     "Tiling rules:",
                     "\t- Cells can only connect orthogonally: up, down, left, right",
                     "\t- Tiles cannot contain duplicate cells: (a, a) is invalid",
                     "\t- A tile must contain 2 cells: (a, None) is invalid",
                     "\t- One tiling per cell: (a, b) & (a, c) is invalid",
            ]
        ]
    )
    rule_group.arrange_in_grid(5, 1, col_alignments="l")
    rule_group.center()
    rule_group.to_edge(LEFT)

    visual_board.next_to(rule_group, RIGHT)

    slide.play(FadeIn(rule_group[0]))
    slide.play(FadeIn(rule_group[1]))

    slide.play(Create(visual_board, run_time=1.))

    surround_top: SurroundingRectangle = SurroundingRectangle(
        visual_board[1], visual_board[5], buff=-.1)
    surround_bottom: SurroundingRectangle = SurroundingRectangle(
        visual_board[5], visual_board[9], buff=-.1)
    surround_left: SurroundingRectangle = SurroundingRectangle(
        visual_board[4], visual_board[5], buff=-.1)
    surround_right: SurroundingRectangle = SurroundingRectangle(
        visual_board[5], visual_board[6], buff=-.1)

    slide.play(Create(surround_top))
    slide.play(ReplacementTransform(surround_top, surround_bottom))
    slide.play(ReplacementTransform(surround_bottom, surround_left))
    slide.play(ReplacementTransform(surround_left, surround_right))
    slide.play(FadeOut(surround_right))

    slide.next_section()

    surround_top = SurroundingRectangle(visual_board[0], buff=-.1)

    slide.play(FadeIn(rule_group[2]))
    slide.play(Create(surround_top))
    to_itself: CurvedArrow = CurvedArrow(
        start_point=visual_board[0].get_corner(UL) + RIGHT * 0.2,
        end_point=visual_board[0].get_corner(UR) + LEFT * 0.2,
        angle=-TAU / 2
    )
    cross_label: Cross = Cross().scale(.2).next_to(to_itself, UP)
    slide.play(Create(to_itself), FadeIn(cross_label))

    slide.next_section()

    slide.play(FadeOut(to_itself))

    slide.play(FadeIn(rule_group[3]))

    invisible_square_left: Square = Square(1).next_to(
        visual_board[0], LEFT, buff=0.)
    invisible_square_top: Square = Square(1).next_to(
        visual_board[0], UP, buff=0.)
    surround_left = SurroundingRectangle(
        invisible_square_left, visual_board[0], buff=-.1)
    slide.play(cross_label.animate.next_to(invisible_square_left, UP),
               ReplacementTransform(surround_top, surround_left))
    surround_top = SurroundingRectangle(
        visual_board[0], invisible_square_top, buff=-.1)
    slide.play(ReplacementTransform(surround_left, surround_top))

    slide.next_section()

    slide.play(FadeOut(surround_top))
    slide.play(FadeIn(rule_group[4]))

    surround_right = SurroundingRectangle(
        visual_board[0], visual_board[1], color=RED, fill_color=RED, fill_opacity=.4, buff=-.1)
    surround_bottom = SurroundingRectangle(
        visual_board[0], visual_board[4], color=ORANGE, fill_color=ORANGE, fill_opacity=.4, buff=-.1)
    slide.play(Create(surround_right),
               cross_label.animate.next_to(visual_board, UP))
    slide.play(Create(surround_bottom))
    surround_top = SurroundingRectangle(
        visual_board[4], visual_board[8], color=ORANGE, fill_color=ORANGE, fill_opacity=.4, buff=-.1)
    slide.play(ReplacementTransform(surround_bottom,
               surround_top), FadeOut(cross_label))

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)
