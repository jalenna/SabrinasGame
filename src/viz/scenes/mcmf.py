from manim import *
from typing import Any
from random import seed as rand_seed
from manim_slides.slide import ThreeDSlide
from src.viz.utils.visual import show_slide_number
from src.viz.utils.trackers import JSlideNumberTracker

config["max_files_cached"] = -1


class MCMFSlide(ThreeDSlide):
    skip_reversing = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slide_tracker: JSlideNumberTracker = JSlideNumberTracker(32)
        self.current_slide_number: Text = Text(
            str(self.slide_tracker.current), font_size=32).to_edge(DR)

    def construct(self) -> None:
        rand_seed(42)

        self.intro()

    def intro(self) -> None:
        title: Text = Text("#TODO Minimum Cost Maximum Flow")

        self.play(Write(title))

        show_slide_number(self, update=False)
