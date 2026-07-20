from manim import *
from src.viz.utils.visual import BasePresentation, reset_slide


def results_slide(slide: BasePresentation) -> None:
    title: Text = Text("Results")

    slide.play(FadeIn(title))

    slide.next_section()
    slide.play(FadeOut(title))

    slide.next_slide()
    slide.slide_tracker.inc()
    reset_slide(slide)
