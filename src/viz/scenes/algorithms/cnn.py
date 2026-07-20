from manim import *
from SabrinasGame.src.tiling_algorithms.utils.types import ExplicitDims
from src.viz.utils.visual import BasePresentation, create_pairings, reset_slide


def cnn_slide(slide: BasePresentation) -> None:
    title: Text = Text("Convolutional Neural Network (CNN)")

    slide.play(FadeIn(title))

    slide.next_section()
    slide.play(FadeOut(title))

    title = Text("Training The Network", font_size=24).next_to(
        slide.slide_category, DOWN)

    slide.play(FadeIn(title))

    slide.depth_solver.clear()
    slide.board_generator.clear()
    slide.board_generator.generate(ExplicitDims(
        [slide.problematic_tiles_dim]), slide.cost_range, slide.problematic_tiles)

    visual_board: VGroup = slide.board_generator.visual_boards[-1].scale(.3).to_edge(
        LEFT)
    slide.depth_solver.solve(slide.problematic_tiles_dim,
                             slide.problematic_tiles, visual_board)

    visual_pairs: VGroup = VGroup(create_pairings(
        visual_board, slide.depth_solver.solver.pairs, fill_opacity=1.))

    visual_pairs.next_to(visual_board)
    solution_caption: Text = Text(
        "DFS/MCMF Solution", font_size=12).next_to(visual_pairs, UP)

    model_box: SurroundingRectangle = SurroundingRectangle(
        visual_board, buff=0.).center()
    model_name: Text = Text("CNN", font_size=18)

    data_to_model: LabeledArrow = LabeledArrow(Text("Input", font_size=6), start=visual_pairs.get_edge_center(
        RIGHT), end=model_box.get_edge_center(LEFT))

    slide.play(
        FadeIn(
            visual_board,
            visual_pairs,
            solution_caption,
            model_box,
            model_name,
            data_to_model,
        )
    )

    train_title: Text = Text("Config | Hyperparameters", font_size=18)
    train_parameters: Paragraph = Paragraph(
        *(
            "Mean Squared Error Loss (MSE)",
            "Stochastic Gradient Descend (SGD):",
            "\t- Learn rate = 0.001",
            "\t- Momentum = 0.9",
            "Epochs = 1000",
            "Cost Range = [1, 21)",
            "Boards:",
            "\t- Round Robin:",
            "\t\tWidths: [4, 6, 8, 10, 12, 14, 16]",
            "\t\tHeights: [4, 6, 8, 10, 12, 14, 16]",
        ),
        font_size=12,
        line_spacing=1.
    ).next_to(model_box, RIGHT, buff=1.5)

    train_title.next_to(train_parameters, UP)

    slide.play(FadeIn(train_parameters, train_title))

    slide.next_slide()
    slide.slide_tracker.inc()

    slide.play(
        FadeOut(visual_board, visual_pairs, data_to_model, title,
                train_title, train_parameters, model_name, solution_caption)
    )

    slide.wait(1)

    slide.move_camera(frame_center=model_box, zoom=10.)

    slide.play(FadeOut(model_box))

    slide.set_camera_orientation(frame_center=ORIGIN, zoom=1.)
    model_architecture(slide)

    slide.set_camera_orientation(frame_center=model_box, zoom=10.)
    slide.play(
        FadeIn(visual_board, visual_pairs, data_to_model,
               title, model_box, solution_caption)
    )

    slide.move_camera(zoom=1.)

    slide.play(FadeIn(model_name))

    slide.next_slide()

    new_title: Text = Text("Using The Network", font_size=24).next_to(
        slide.slide_category, DOWN)

    new_solution_caption: Text = Text(
        "Incomplete solution", font_size=12).next_to(visual_pairs, UP)

    to_remove_pairs: list[int] = [0, 4, 5, 9, 14]

    slide.play(
        ReplacementTransform(title, new_title),
        ReplacementTransform(solution_caption, new_solution_caption),
        FadeOut(*(visual_pairs[i] for i in to_remove_pairs))
    )
    title = new_title
    solution_caption = new_solution_caption

    dfs_text: Label = Label(
        Text("DFS Neighbor Sorting", font_size=18)).next_to(model_box, buff=1.5)

    model_to_logit: LabeledArrow = LabeledArrow(Text(
        "Raw Logits", font_size=6), start=model_box.get_edge_center(RIGHT), end=dfs_text.get_edge_center(LEFT))

    slide.play(FadeIn(model_to_logit, dfs_text))

    slide.next_slide()
    slide.slide_tracker.inc()

    reset_slide(slide)
    cnn_demo(slide)

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)


def model_architecture(slide: BasePresentation) -> None:
    title: Text = Text("CNN Architecture", font_size=24).next_to(
        slide.slide_category, DOWN)

    slide.play(FadeIn(title))
    model = slide.guided_depth_solver.solver.model

    # Layers
    conv1_layer: VGroup = VGroup(
        *create_layer(*model.conv1.kernel_size, model.conv1.out_channels)).scale(.7)
    conv2_layer: VGroup = VGroup(
        *create_layer(*model.conv2.kernel_size, model.conv2.out_channels)).scale(.7)
    pool_layer: VGroup = VGroup(create_layer(
        *model.pool.output_size, model.conv1.out_channels, fill_color=GREEN)).scale(.7)
    lin1_layer: VGroup = VGroup(create_layer(
        1, 1, model.fc1.in_features, fill_color=GREEN)).scale(.7)
    lin2_layer: VGroup = VGroup(create_layer(
        1, 1, model.fc2.in_features, fill_color=GREEN)).scale(.7)

    layers: VGroup = VGroup(conv1_layer, conv2_layer,
                            pool_layer, lin1_layer, lin2_layer)
    layers.arrange(RIGHT, buff=1.5, center=False).next_to(
        title, DOWN, buff=1.5)

    # Captions
    conv1_layer_caption: Text = Text(
        "Conv2D\nInput channels: 2\nOutput channels: 32\nKernel size: 3x3\nPadding: 1", font_size=12).next_to(conv1_layer, UP)
    conv2_layer_caption: Text = Text(
        "Conv2D\nInput channels: 32\nOutput channels: 64\nKernel size: 3x3\nPadding: 1", font_size=12).next_to(conv2_layer, UP)
    pool_layer_caption: Text = Text(
        "AdaptiveAvgPool2d\nOutput channels: 64 * 4 * 4\nKernel size: 4x4", font_size=12).next_to(pool_layer, UP)
    lin1_layer_caption: Text = Text(
        "Linear\nInput channels: 64 * 4 * 4\nOutput channels: 128", font_size=12).next_to(lin1_layer, UP)
    lin2_layer_caption: Text = Text(
        "Linear\nInput channels: 128\nOutput channels: 16 * 16", font_size=12).next_to(lin2_layer, UP)

    conv1_to_conv2: LabeledArrow = LabeledArrow(Text(
        "ReLU", font_size=6), start=conv1_layer.get_edge_center(RIGHT), end=conv2_layer.get_edge_center(LEFT))
    conv2_to_pool: Arrow = Arrow(start=conv2_layer.get_edge_center(
        RIGHT), end=pool_layer.get_edge_center(LEFT))
    pool_to_lin1: LabeledArrow = LabeledArrow(Text(
        "Flatten + ReLU", font_size=6), start=pool_layer.get_edge_center(RIGHT), end=lin1_layer.get_edge_center(LEFT)).set_z_index(lin1_layer[-2].z_index)
    lin1_to_lin2: Arrow = Arrow(start=lin1_layer.get_edge_center(
        RIGHT), end=lin2_layer.get_edge_center(LEFT))

    slide.play(
        FadeIn(
            lin2_layer,
            lin2_layer_caption,
            lin1_to_lin2,
            lin1_layer,
            lin1_layer_caption,
            pool_to_lin1,
            pool_layer_caption,
            pool_layer,
            conv2_to_pool,
            conv1_to_conv2,
            conv2_layer,
            conv2_layer_caption,
            conv1_layer,
            conv1_layer_caption,
        )
    )

    slide.move_camera(frame_center=conv1_layer)
    slide.wait(1)
    slide.move_camera(frame_center=conv2_layer)
    slide.wait(1)
    slide.move_camera(frame_center=pool_layer)
    slide.wait(1)
    slide.move_camera(frame_center=lin1_layer)
    slide.wait(1)
    slide.move_camera(frame_center=lin2_layer)
    slide.wait(1)

    slide.move_camera(frame_center=ORIGIN, zoom=.8)

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)


def cnn_demo(slide: BasePresentation) -> None:
    neighbor_sorting_text: Label = Label(
        Text("CNN sorted neighbors", font_size=18)).to_edge(LEFT)

    slide.play(FadeIn(neighbor_sorting_text))

    visual_board: VGroup = slide.board_generator.visual_boards[-1].scale(1.7)

    lines = slide.guided_depth_solver.solve(slide.problematic_tiles_dim,
                                            slide.problematic_tiles, visual_board)

    visual_pairs: VGroup = VGroup(create_pairings(
        visual_board, slide.guided_depth_solver.solver.pairs, fill_opacity=1.))

    slide.play(FadeIn(visual_board))

    visual_lines: VGroup = VGroup()

    for state in slide.guided_depth_solver.solver.history:
        u, v = state.pair[0], state.pair[1]
        key = (min(u, v), max(u, v))
        line = lines[key]

        if state.added:
            slide.play(FadeIn(line, run_time=.2))
            visual_lines.add(line)
        else:
            slide.play(FadeOut(line, run_time=.2))
            visual_lines.remove(line)

    slide.play(FadeOut(*visual_lines), FadeIn(*visual_pairs))


def create_layer(width: float, height: float, count: int, fill_color: ManimColor = BLUE) -> list[Rectangle]:
    return [
        Rectangle(
            width=width,
            height=height,
            grid_xstep=1.,
            grid_ystep=1.,
            fill_opacity=.4,
            stroke_opacity=.4,
            fill_color=fill_color
        ).set_z(0.01 * i).set_z_index(0.01 * i)
        # .shift(RIGHT * 0.01 * i + DOWN * 0.01 * i)
        for i in range(count)
    ]
