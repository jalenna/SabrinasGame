
from manim import *
from SabrinasGame.src.tiling_algorithms.utils.types import Boards, RoundRobinDims, iVec2D, ExplicitDims
from src.viz.utils.visual import BasePresentation, reset_slide


def board_generation_slide(slide: BasePresentation) -> None:
    slide.board_generator.clear()

    dim: iVec2D = iVec2D(2, 2)
    slide.board_generator.generate(ExplicitDims([dim]), slide.cost_range)

    visual_board: VGroup = slide.board_generator.visual_boards[-1]

    [
        square.submobjects[0].set_opacity(0) for square in visual_board
    ]

    title: Text = Text("Board Setup")

    widths, heights = [2, 4, 6], [2, 4, 6]

    setup_rules: Paragraph = Paragraph(
        *[
            "Board setup:",
            "\t- Flat array",
            "\t- Cost ranges: [1, 21)",
            "\t- Explicitly/Round Robin generated:",
            f"\t\t{widths} x {heights}",
            "\t- Even board sizes only:",
            "\t\tboard_size // tile_size -> int",
            "\t\t3 x 3 // 2 x 1 -> int",
            "\t\t9 // 2 != int",

        ],
        font_size=20,
        line_spacing=1,
    )

    setup_rules.to_edge(LEFT)

    slide.play(FadeIn(title))

    slide.next_section()

    slide.play(FadeOut(title))

    slide.play(FadeIn(setup_rules[0], setup_rules[1]))

    slide.play(FadeIn(visual_board))
    slide.play(visual_board.animate.arrange(RIGHT, buff=.1))

    slide.next_section()

    slide.play(FadeIn(setup_rules[2]))
    slide.play(*[
        square.submobjects[0].animate.set_opacity(1.) for square in visual_board
    ])

    slide.next_section()

    slide.play(FadeIn(setup_rules[3]), FadeOut(visual_board))

    explicit_method_label: Text = Text("Explicit Dimensions", font_size=24)
    rr_method_label: Text = Text("Round Robin Dimensions", font_size=24)

    dims: RoundRobinDims = RoundRobinDims(widths, heights)
    slide.board_generator.clear()
    slide.board_generator.generate(dims, slide.cost_range)

    visual_boards: list[VGroup] = slide.board_generator.visual_boards
    data_boards: Boards = slide.board_generator.data_generator.boards

    explicit_boards: VGroup = VGroup()

    for i in range(3):
        board_group: VGroup = VGroup()
        w, h = data_boards[i][1]
        board_group.add(Text(f"{w} x {h}"))
        board_group.add(visual_boards[i])
        board_group.arrange(DOWN)
        explicit_boards.add(board_group)

    explicit_boards.scale(.5).shift(RIGHT)

    slide.play(FadeIn(explicit_boards))
    slide.play(explicit_boards.animate.arrange(RIGHT))
    slide.play(explicit_boards.animate.shift(RIGHT * 2))
    explicit_method_label.next_to(explicit_boards, UP)
    rr_method_label.next_to(slide.slide_category, DR, buff=1.)
    slide.play(FadeIn(explicit_method_label))

    slide.next_section()

    slide.play(ReplacementTransform(explicit_method_label,
               rr_method_label), FadeOut(explicit_boards))
    slide.play(rr_method_label.animate.to_edge(UP), FadeIn(setup_rules[4]))

    boards: VGroup = VGroup()
    prev_board_group: VGroup | None = None
    for i in range(3, 8):
        board_group: VGroup = VGroup()
        w, h = data_boards[i][1]
        board_group.add(Text(f"{w} x {h}"))
        board_group.add(visual_boards[i])
        board_group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        board_group.scale(.2)

        if prev_board_group:
            board_group.next_to(prev_board_group, DOWN)
        else:
            board_group.next_to(rr_method_label, DOWN)

        prev_board_group = board_group
        boards.add(prev_board_group)

        slide.play(FadeIn(board_group))

    slide.play(FadeIn(Text("...").next_to(boards, DOWN)))

    slide.next_section()

    slide.play(FadeIn(setup_rules[5]))
    slide.play(FadeIn(setup_rules[6]))
    slide.play(FadeIn(setup_rules[7]))
    slide.play(FadeIn(setup_rules[8]))

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)
