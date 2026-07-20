from manim import *
from SabrinasGame.src.tiling_algorithms.utils.types import ExplicitDims
from src.viz.utils.visual import BasePresentation, create_pairings, normalized_neighbor_proximity, reset_slide


def dfs_slide(slide: BasePresentation) -> None:
    title: Text = Text("(Greedy) Depth First Search")

    slide.play(FadeIn(title))

    slide.next_section()

    slide.play(FadeOut(title))

    steps: VGroup = VGroup(
        *[
            Label(Text(text, font_size=20), frame_config={"buff": .1, "stroke_width": .5}, box_config={"buff": .5}) for text in [
                "DFS(board)",
                "All cells tiled",
                "Has untiled cell",
                "Pick first untiled cell (a)",
                "Has untiled neighbor",
                "Pick first untiled neighbor (b)",
                "Tile (a, b)",
                "DFS(board)",
                "Undo tile (a, b)",
            ]
        ]
    )
    end_states: VGroup = VGroup(
        *[
            Label(Text(text, font_size=20), frame_config={"buff": .1, "stroke_width": .5}, box_config={"buff": .5}) for text in [
                "Return TRUE",
                "Return FALSE",
                "Return TRUE",
                "Return FALSE",
            ]
        ]
    )

    steps.arrange(DOWN)
    steps.scale(.5)
    steps.to_corner(UL)
    end_states.scale(.5)

    end_states[0].next_to(steps[1])
    end_states[1].next_to(steps[2])
    end_states[2].next_to(steps[7])
    end_states[3].next_to(steps[4])

    dfs_to_paired: Arrow = Arrow(start=steps[0].frame.get_edge_center(
        DOWN), end=steps[1].frame.get_edge_center(UP), buff=0.)
    paired_to_has: LabeledArrow = LabeledArrow(Text("No", font_size=6), start=steps[1].frame.get_edge_center(
        DOWN), end=steps[2].frame.get_edge_center(UP), buff=0.)
    has_to_pick: LabeledArrow = LabeledArrow(Text("Yes", font_size=6), start=steps[2].frame.get_edge_center(
        DOWN), end=steps[3].frame.get_edge_center(UP), buff=0.)
    pick_to_has_neighbor: Arrow = Arrow(start=steps[3].frame.get_edge_center(
        DOWN), end=steps[4].frame.get_edge_center(UP), buff=0.)
    has_neighbor_to_pick_neighbor: LabeledArrow = LabeledArrow(Text("Yes", font_size=6), start=steps[4].frame.get_edge_center(
        DOWN), end=steps[5].frame.get_edge_center(UP), buff=0.)
    pick_neighbor_to_tile: Arrow = Arrow(start=steps[5].frame.get_edge_center(
        DOWN), end=steps[6].frame.get_edge_center(UP), buff=0.)
    tile_to_dfs: Arrow = Arrow(start=steps[6].frame.get_edge_center(
        DOWN), end=steps[7].frame.get_edge_center(UP), buff=0.)
    dfs_to_undo: LabeledArrow = LabeledArrow(Text("FALSE", font_size=6), start=steps[7].frame.get_edge_center(
        DOWN), end=steps[8].frame.get_edge_center(UP), buff=0.)

    paired_to_end: LabeledArrow = LabeledArrow(Text("Yes", font_size=6), start=steps[1].frame.get_edge_center(
        RIGHT), end=end_states[0].frame.get_edge_center(LEFT), buff=0.)
    unpaired_to_end: LabeledArrow = LabeledArrow(Text("No", font_size=6), start=steps[2].frame.get_edge_center(
        RIGHT), end=end_states[1].frame.get_edge_center(LEFT), buff=0.)
    dfs_to_end: LabeledArrow = LabeledArrow(Text("TRUE", font_size=6), start=steps[7].frame.get_edge_center(
        RIGHT), end=end_states[2].frame.get_edge_center(LEFT), buff=0.)
    neighbor_to_end: LabeledArrow = LabeledArrow(Text("No", font_size=6), start=steps[4].frame.get_edge_center(
        RIGHT), end=end_states[3].frame.get_edge_center(LEFT), buff=0.)

    slide.play(
        FadeIn(
            *(
                steps,
                end_states,
                dfs_to_paired,
                paired_to_has,
                has_to_pick,
                pick_to_has_neighbor,
                has_neighbor_to_pick_neighbor,
                pick_neighbor_to_tile,
                tile_to_dfs,
                dfs_to_undo,
                paired_to_end,
                unpaired_to_end,
                dfs_to_end,
                neighbor_to_end,
            )
        )
    )

    slide.next_section()

    slide.depth_solver.clear()
    slide.board_generator.clear()
    slide.board_generator.generate(ExplicitDims(
        [slide.problematic_tiles_dim]), slide.cost_range, slide.problematic_tiles)

    visual_board: VGroup = slide.board_generator.visual_boards[-1]
    visual_board.shift(RIGHT).scale(.8)

    slide.play(Create(visual_board))

    neighbors: list[int] = [3, 15, 8, 10]
    neighbor_costs: list[float] = [slide.problematic_tiles[v]
                                   for v in neighbors]
    intensities: list[float] = normalized_neighbor_proximity(
        slide.problematic_tiles[9], neighbor_costs)

    neighbors_ranked: VGroup = VGroup(
        [
            SurroundingRectangle(visual_board[neighbor], fill_opacity=intensities[i] * .7, fill_color=RED, buff=-0.1) for i, neighbor in enumerate(neighbors)
        ]
    )

    neighbor_creation_label: Text = Text(
        "Neighbor Ranking\nABS(DIFF()) (Lower intensity means closer)", font_size=20).next_to(visual_board, UP)

    slide.play(FadeIn(neighbor_creation_label))
    slide.play(FadeIn(neighbors_ranked), Circumscribe(
        visual_board[9], run_time=2., buff=-.1))

    lines = slide.depth_solver.solve(slide.problematic_tiles_dim,
                                     slide.problematic_tiles, visual_board)

    slide.next_section()

    slide.play(FadeOut(neighbors_ranked, neighbor_creation_label))

    visual_pairs_correct: VGroup = VGroup(create_pairings(
        visual_board, slide.depth_solver.solver.pairs))

    visual_lines: VGroup = VGroup()

    for state in slide.depth_solver.solver.history:
        u, v = state.pair[0], state.pair[1]
        key = (min(u, v), max(u, v))
        line = lines[key]

        if state.added:
            slide.play(FadeIn(line, run_time=.2))
            visual_lines.add(line)
        else:
            slide.play(FadeOut(line, run_time=.2))
            visual_lines.remove(line)

    slide.play(FadeOut(*visual_lines), FadeIn(*visual_pairs_correct))

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)
