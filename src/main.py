from manim import *
from typing import Any
from src.viz.utils.visual import BasePresentation
from viz.scenes.results.results import results_slide
from src.viz.scenes.board.intro import board_intro_slide
from src.viz.scenes.algorithms.algorithms import algorithms_slide
from src.viz.scenes.board.generation import board_generation_slide


class Presentation(BasePresentation):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.to_render()

    def to_render(self) -> None:
        self.slide_number_text: Text = Text(
            str(self.slide_tracker.current), font_size=32).to_edge(DR)

        self.slide_category = VGroup(
            Text(text,
                 font_size=20
                 ) for text in [
                "Game",
                "Algorithms",
                "Results"
            ]
        ).set_opacity(.2).arrange(RIGHT, aligned_edge=UP).to_edge(UP)

        self.active_category: int = 0
        self.prev_category: int = self.active_category

        self.slide_category[self.active_category].set_opacity(.75)

        def set_active_category(index: int) -> None:
            self.play(self.slide_category.animate.set_opacity(.2))
            self.play(self.slide_category[index].animate.set_opacity(.75))

        def update_text(mob):
            if (not self.slide_tracker.has_updated_prev()):
                new_text: Text = Text(str(self.slide_tracker.current),
                                      font_size=32).to_edge(DR)
                mob.become(new_text)
                self.add_fixed_in_frame_mobjects(mob)
                self.slide_tracker.update_prev()

        self.slide_number_text.add_updater(update_text)

        self.add(self.slide_number_text, self.slide_category)
        self.add_fixed_in_frame_mobjects(
            self.slide_number_text, self.slide_category)

        board_intro_slide(self)
        board_generation_slide(self)
        set_active_category(1)
        algorithms_slide(self)
        set_active_category(2)
        results_slide(self)
        self.next_slide()
