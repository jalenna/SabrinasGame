from manim import *
from typing import Callable
from src.viz.scenes.algorithms.dfs import dfs_slide
from src.viz.scenes.algorithms.cnn import cnn_slide
from src.viz.scenes.algorithms.mcmf import mcmf_slide
from src.viz.utils.visual import BasePresentation, reset_slide


def algorithms_slide(slide: BasePresentation) -> None:
    algorithms: VGroup = VGroup(
        *[
            Square(3, color=YELLOW).add(Text(text, font_size=24))
            for text in ["DFS", "DFS\n+\nCNN", "MCMF"]
        ]
    )

    algorithms.arrange(RIGHT)

    slide.play(FadeIn(algorithms))

    slide.next_slide()
    slide.slide_tracker.inc()

    def move_to(index: int, slide_func: Callable[[BasePresentation], None]) -> None:
        slide.move_camera(frame_center=algorithms[index])
        slide.play(algorithms[index].submobjects[0].animate.set_opacity(0.))
        slide.move_camera(zoom=10.)

        reset_slide(slide)
        slide_func(slide)

        slide.set_camera_orientation(frame_center=algorithms[index], zoom=10.)
        slide.play(FadeIn(algorithms))
        slide.move_camera(zoom=1.)
        slide.play(algorithms[index].submobjects[0].animate.set_opacity(1.))
        slide.move_camera(frame_center=algorithms)

    move_to(0, dfs_slide)
    slide.next_section()
    move_to(2, mcmf_slide)
    slide.next_section()
    move_to(1, cnn_slide)
