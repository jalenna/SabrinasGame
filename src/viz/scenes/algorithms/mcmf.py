from manim import *
from typing import Callable
from src.viz.utils.visual import BasePresentation, create_label, create_pairings, reset_slide
from SabrinasGame.src.tiling_algorithms.utils.core import absdiff, create_neighbors
from SabrinasGame.src.tiling_algorithms.utils.types import ExplicitDims, Neighbors, Tiles, iVec2D


def mcmf_slide(slide: BasePresentation) -> None:
    title: Text = Text("Minimum Cost Maximum Flow (MCMF)")

    slide.play(FadeIn(title))

    slide.next_section()
    slide.play(FadeOut(title))

    steps: VGroup = VGroup(
        *[
            create_label(text) for text in [
                "MCMF(board)",
                "Build bipartite graph",
                "SPFA()",
                "Is sink reachable | dist[sink] < inf",
                "Augment path",
                "Reconstruct tiles",
            ]
        ]
    )
    end_states: VGroup = VGroup(
        *[
            create_label(text) for text in [
                "Return TRUE",
            ]
        ]
    )

    steps.arrange(DOWN)
    steps.scale(.5)
    end_states.scale(.5)
    end_states[0].next_to(steps[5], DOWN)

    steps[4].next_to(steps[3], LEFT)

    mcmf_to_build_graph: Arrow = Arrow(start=steps[0].frame.get_edge_center(
        DOWN), end=steps[1].frame.get_edge_center(UP), buff=0.)
    build_graph_to_spfa: Arrow = Arrow(start=steps[1].frame.get_edge_center(
        DOWN), end=steps[2].frame.get_edge_center(UP), buff=0.)
    spfa_to_sink: Arrow = Arrow(start=steps[2].frame.get_edge_center(
        DOWN), end=steps[3].frame.get_edge_center(UP), buff=0.)
    sink_to_augment: LabeledArrow = LabeledArrow(Text("No", font_size=6), start=steps[3].frame.get_edge_center(
        LEFT), end=steps[4].frame.get_edge_center(RIGHT), buff=0.)
    augment_to_spfa: CurvedArrow = CurvedArrow(start_point=steps[4].frame.get_edge_center(
        UP), end_point=steps[2].frame.get_edge_center(LEFT), angle=-TAU / 4., tip_length=.15)
    sink_to_reconstruct: LabeledArrow = LabeledArrow(Text("Yes", font_size=6), start=steps[3].frame.get_edge_center(
        DOWN), end=steps[5].frame.get_edge_center(UP), buff=0., tip_length=.15)

    reconstruct_to_end: Arrow = Arrow(start=steps[5].frame.get_edge_center(
        DOWN), end=end_states[0].frame.get_edge_center(UP), buff=0.)

    flow_chart: VGroup = VGroup(
        *(
            steps,
            end_states,
            mcmf_to_build_graph,
            build_graph_to_spfa,
            spfa_to_sink,
            sink_to_augment,
            augment_to_spfa,
            sink_to_reconstruct,
            reconstruct_to_end,
        )
    )

    flow_chart.move_to((flow_chart.get_x(), 0, 0))

    highlights: list[SurroundingRectangle] = [
        SurroundingRectangle(steps[i].frame, buff=.1) for i in
        [1, 2, 4]
    ]

    slide.play(FadeIn(flow_chart))
    slide.play(FadeIn(*highlights))

    def expand_on_label(i: int, chart: Callable[[BasePresentation], None]) -> None:
        slide.move_camera(frame_center=highlights[i])
        slide.move_camera(zoom=8.)
        slide.play(FadeOut(flow_chart))
        slide.move_camera(zoom=20.)
        slide.play(FadeOut(*highlights))

        # reset_slide(slide)
        slide.set_camera_orientation(frame_center=ORIGIN, zoom=1.)
        slide.slide_tracker.inc()

        chart(slide)

        slide.set_camera_orientation(frame_center=highlights[i], zoom=20.)
        slide.play(FadeIn(flow_chart), FadeIn(*highlights))
        slide.move_camera(zoom=1.)
        slide.move_camera(frame_center=ORIGIN)
        slide.next_section()

    slide.next_section()

    expand_on_label(0, bipartite_slide)
    expand_on_label(1, spfa_slide)
    expand_on_label(2, augment_slide)

    slide.next_section()

    slide.play(FadeOut(*highlights))

    # flow_group: VGroup = VGroup(flow_chart, *highlights)

    slide.play(flow_chart.animate.to_edge(LEFT))

    slide.board_generator.clear()
    dim: iVec2D = iVec2D(6, 6)
    slide.board_generator.generate(ExplicitDims([dim]), slide.cost_range)
    visual_board: VGroup = slide.board_generator.visual_boards[-1].scale(.7).shift(
        RIGHT)
    data_board: Tiles = slide.board_generator.data_generator.boards[-1][0]

    visual_lines: list[Line] = []

    slide.play(FadeIn(visual_board), FadeOut(flow_chart))
    slide.play(visual_board.animate.scale(.5))
    slide.play(visual_board.animate.center())

    p_a: set[int] = {
        i for i in range(len(visual_board)) if ((i // dim.x) + (i % dim.x)) % 2 == 0
    }
    p_b: set[int] = {
        i for i in range(len(visual_board)) if ((i // dim.x) + (i % dim.x)) % 2 != 0
    }

    even_cells: VGroup = VGroup(*(visual_board[i] for i in p_a))
    odd_cells: VGroup = VGroup(*(visual_board[i] for i in p_b))

    slide.play(
        *(
            cell.animate.shift(LEFT * 2) for cell in even_cells
        ),
        *(
            cell.animate.shift(RIGHT * 2) for cell in odd_cells
        ),
    )

    slide.play(odd_cells.animate.arrange(DOWN, center=False),
               even_cells.animate.arrange(DOWN, center=False))

    slide.move_camera(frame_center=visual_board, zoom=.5)

    lines = slide.mcmf_solver.visual_solve(dim, data_board, visual_board)

    for state in slide.mcmf_solver.history:
        u, v = state.pair[0], state.pair[1]
        key = (min(u, v), max(u, v))
        line = lines[key]

        if state.added:
            slide.play(FadeIn(line, run_time=.2))
            visual_lines.append(line)
        else:
            slide.play(FadeOut(line, run_time=.2))
            visual_lines.remove(line)

    slide.next_section()

    slide.play(FadeOut(*visual_lines))

    slide.play(visual_board.animate.arrange_in_grid(
        dim.y, dim.x, center=False))

    slide.move_camera(frame_center=visual_board, zoom=1.)

    visual_pairs_correct: list[SurroundingRectangle] = create_pairings(
        visual_board, slide.mcmf_solver.pairs)
    slide.play(FadeIn(*visual_pairs_correct))
    # slide.play(FadeOut(*visual_lines), FadeIn(*visual_pairs_correct))

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)


def bipartite_slide(slide: BasePresentation) -> None:
    title: Text = Text("Bipartite Graph Creation", font_size=24).next_to(
        slide.slide_category, DOWN)

    slide.play(FadeIn(title))

    steps: VGroup = VGroup(
        *[
            create_label(text) for text in [
                "Source",
                "Even parity cells",
                "Odd parity cells",
                "Sink",
            ]
        ]
    )

    steps.arrange(RIGHT)
    steps.scale(.5)
    steps.next_to(title, DOWN)

    source_to_even: Arrow = Arrow(start=steps[0].frame.get_edge_center(
        RIGHT), end=steps[1].frame.get_edge_center(LEFT), buff=0.)
    odd_to_sink: Arrow = Arrow(start=steps[2].frame.get_edge_center(
        RIGHT), end=steps[3].frame.get_edge_center(LEFT), buff=0.)

    slide.play(FadeIn(steps, source_to_even, odd_to_sink))

    slide.board_generator.clear()
    dim: iVec2D = iVec2D(4, 4)
    slide.board_generator.generate(ExplicitDims([dim]), slide.cost_range)
    visual_board: VGroup = slide.board_generator.visual_boards[-1].scale(.7).next_to(
        steps, DOWN)
    neighbors: Neighbors = create_neighbors(
        dim, slide.board_generator.data_generator.boards[-1][0], absdiff)
    slide.play(FadeIn(visual_board))

    slide.next_section()

    p_a: set[int] = {
        i for i in range(len(visual_board)) if ((i // dim.x) + (i % dim.x)) % 2 == 0
    }
    p_b: set[int] = {
        i for i in range(len(visual_board)) if ((i // dim.x) + (i % dim.x)) % 2 != 0
    }

    even_cells: VGroup = VGroup(*(visual_board[i] for i in p_a))
    odd_cells: VGroup = VGroup(*(visual_board[i] for i in p_b))

    slide.play(
        *(
            cell.animate.shift(LEFT * 2) for cell in even_cells
        ),
        *(
            cell.animate.shift(RIGHT * 2) for cell in odd_cells
        ),
    )

    source: Label = create_label("Source")
    sink: Label = create_label("Sink")

    source.next_to(even_cells, LEFT, buff=1.)
    sink.next_to(odd_cells, RIGHT, buff=1.)

    slide.play(FadeIn(source, sink))

    slide.next_section()

    highlights: list[SurroundingRectangle] = [
        SurroundingRectangle(cells) for cells in [even_cells, odd_cells]
    ]

    source_to_even_demo: LabeledArrow = LabeledArrow(Text("To each", font_size=6), start=source.frame.get_edge_center(
        RIGHT), end=highlights[0].get_edge_center(LEFT), buff=0.)
    odd_to_sink_demo: LabeledArrow = LabeledArrow(Text("To each", font_size=6), start=highlights[1].get_edge_center(
        RIGHT), end=sink.frame.get_edge_center(LEFT), buff=0.)

    ends_edge_info: Text = Text(
        "Source/Sink Edges:\nCapacity = 1\nCost = 0", font_size=20).to_corner(DL)

    slide.play(FadeIn(source_to_even_demo, odd_to_sink_demo,
               ends_edge_info, *highlights))

    slide.next_section()

    even_to_odd: LabeledArrow = LabeledArrow(Text("To neighbor", font_size=6), start=highlights[0].get_edge_center(
        RIGHT), end=highlights[1].get_edge_center(LEFT), buff=0.)

    parities_edge_info: Text = Text(
        "Parity Edges:\nCapacity = 1\nCost = ABS(DIFF(a, b))      .", font_size=20).to_corner(DR)

    global_edge_info: Text = Text(
        "Shared Properties:\nReverse = b\nCapacity = 0\nCost = -Cost", font_size=20)

    slide.play(FadeIn(even_to_odd, parities_edge_info))

    slide.next_section()

    slide.play(FadeOut(*highlights), odd_cells.animate.scale(.5),
               even_cells.animate.scale(.5))
    slide.play(odd_cells.animate.arrange(DOWN, center=False),
               even_cells.animate.arrange(DOWN, center=False), FadeOut(even_to_odd, source_to_even_demo, odd_to_sink_demo))
    slide.move_camera(zoom=.7, frame_center=visual_board)

    slide.play(
        LaggedStart(
            *(
                FadeIn(Arrow(start=source.frame.get_edge_center(RIGHT), end=cell.get_edge_center(LEFT), stroke_width=1.,
                             tip_length=.1)) for cell in even_cells
            )
        )
    )

    slide.play(
        LaggedStart(
            *(
                FadeIn(Arrow(start=visual_board[ci].get_edge_center(RIGHT), end=visual_board[n].get_edge_center(LEFT), stroke_width=1.,
                             tip_length=.1)) for ci in p_a for n in neighbors[ci]
            )
        )
    )

    slide.play(
        LaggedStart(
            *(
                FadeIn(Arrow(start=cell.get_edge_center(RIGHT), end=sink.frame.get_edge_center(LEFT), stroke_width=1.,
                             tip_length=.1)) for cell in odd_cells
            )
        )
    )

    global_edge_info.next_to(visual_board, DOWN)

    slide.play(FadeIn(global_edge_info))

    slide.next_section()

    slide.wait(1)

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)


def spfa_slide(slide: BasePresentation) -> None:
    title: Text = Text("Shortest Path Faster Algorithm (SPFA)", font_size=24)

    slide.play(FadeIn(title))

    slide.next_section()

    slide.play(title.animate.next_to(
        slide.slide_category, DOWN))

    steps: VGroup = VGroup(
        *[
            create_label(text) for text in [
                "SPFA(source)",
                "Queue(source)",
                "Distances All Edges = inf, Distance[source] = 0",
                "Is queue empty",
                "Pop front = u",
                "Relax | Capacity > 0 and u.edge < distance[v = u.to]",
                "Update distance and push v",
            ]
        ]
    )
    end_states: VGroup = VGroup(
        *[
            create_label(text) for text in [
                "Return Distances",
            ]
        ]
    )

    steps.next_to(title, DOWN)

    steps.arrange(DOWN)
    steps.scale(.5)
    end_states.scale(.5)
    end_states[0].next_to(steps[3], RIGHT)

    spfa_to_queue_init: Arrow = Arrow(start=steps[0].frame.get_edge_center(
        DOWN), end=steps[1].frame.get_edge_center(UP), buff=0.)
    queue_init_to_dist_init: Arrow = Arrow(start=steps[1].frame.get_edge_center(
        DOWN), end=steps[2].frame.get_edge_center(UP), buff=0.)
    dist_init_to_queue: Arrow = Arrow(start=steps[2].frame.get_edge_center(
        DOWN), end=steps[3].frame.get_edge_center(UP), buff=0.)
    queue_to_pop: LabeledArrow = LabeledArrow(Text("No", font_size=6), start=steps[3].frame.get_edge_center(
        DOWN), end=steps[4].frame.get_edge_center(UP), buff=0.)
    pop_to_relax: Arrow = Arrow(start=steps[4].frame.get_edge_center(
        DOWN), end=steps[5].frame.get_edge_center(UP), buff=0.)
    relax_to_update: Arrow = Arrow(start=steps[5].frame.get_edge_center(
        DOWN), end=steps[6].frame.get_edge_center(UP), buff=0.)
    update_to_queue: CurvedArrow = CurvedArrow(start_point=steps[6].frame.get_edge_center(
        LEFT), end_point=steps[3].frame.get_edge_center(LEFT), angle=-TAU/2, tip_length=.15)

    queue_to_dist: LabeledArrow = LabeledArrow(Text("Yes", font_size=6), start=steps[3].frame.get_edge_center(
        RIGHT), end=end_states[0].frame.get_edge_center(LEFT), buff=0.)

    slide.play(
        FadeIn(
            steps,
            end_states,
            spfa_to_queue_init,
            queue_init_to_dist_init,
            dist_init_to_queue,
            queue_to_pop,
            pop_to_relax,
            relax_to_update,
            update_to_queue,
            queue_to_dist,
        )
    )

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)


def augment_slide(slide: BasePresentation) -> None:
    title: Text = Text("Path Augmentation", font_size=24)

    slide.play(FadeIn(title))

    slide.next_section()

    slide.play(title.animate.next_to(
        slide.slide_category, DOWN))

    steps: VGroup = VGroup(
        *[
            create_label(text) for text in [
                "Augment(Sink)",
                "Cell = Sink",
                "Cell == Source",
                "edge = Cell to parent",
                "Decrement edge capacity",
                "Increment reverse edge capacity",
                "cell = parent",
            ]
        ]
    )
    end_states: VGroup = VGroup(
        *[
            create_label(text) for text in [
                "Path augmented",
            ]
        ]
    )

    steps.next_to(title, DOWN)

    steps.arrange(DOWN)
    steps.scale(.5)
    end_states.scale(.5)
    end_states[0].next_to(steps[2], RIGHT)

    func_to_sink: Arrow = Arrow(start=steps[0].frame.get_edge_center(
        DOWN), end=steps[1].frame.get_edge_center(UP), buff=0.)
    sink_to_source: Arrow = Arrow(start=steps[1].frame.get_edge_center(
        DOWN), end=steps[2].frame.get_edge_center(UP), buff=0.)
    source_to_edge: LabeledArrow = LabeledArrow(Text("No", font_size=6), start=steps[2].frame.get_edge_center(
        DOWN), end=steps[3].frame.get_edge_center(UP), buff=0.)
    edge_to_forward: Arrow = Arrow(start=steps[3].frame.get_edge_center(
        DOWN), end=steps[4].frame.get_edge_center(UP), buff=0.)
    forwared_to_reverse: Arrow = Arrow(start=steps[4].frame.get_edge_center(
        DOWN), end=steps[5].frame.get_edge_center(UP), buff=0.)
    reverse_to_parent: Arrow = Arrow(start=steps[5].frame.get_edge_center(
        DOWN), end=steps[6].frame.get_edge_center(UP), buff=0.)
    parent_to_source: CurvedArrow = CurvedArrow(start_point=steps[6].frame.get_edge_center(
        LEFT), end_point=steps[2].frame.get_edge_center(LEFT), angle=-TAU/2, tip_length=.15)

    source_to_augmented: LabeledArrow = LabeledArrow(Text("Yes", font_size=6), start=steps[2].frame.get_edge_center(
        RIGHT), end=end_states[0].frame.get_edge_center(LEFT), buff=0.)

    slide.play(
        FadeIn(
            steps,
            end_states,
            func_to_sink,
            sink_to_source,
            source_to_edge,
            edge_to_forward,
            forwared_to_reverse,
            reverse_to_parent,
            parent_to_source,
            source_to_augmented,
        )
    )

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)
