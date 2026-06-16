from manim import *
from manim_slides.slide import ThreeDSlide


class SabrinasGame(ThreeDSlide):
    skip_reversing = True

    def construct(self) -> None:
        self.intro()

    def intro(self) -> None:
        title: Text = Text("Sabrina's Game", font_size=64)

        self.play(FadeIn(title))

        rule_1: Text = Text("Try to get the lowest avg abs diff", font_size=32)

        self.play(
            title.animate.shift(UP * 1.5),
            FadeIn(rule_1)
        )

        rule_2: Text = Text("Tile as many boards as you can", font_size=32)
        self.play(
            FadeIn(rule_2.shift(DOWN))
        )

        rule_3 = Text("Selected difficulty: 2 x 1 tiles", font_size=32)
        self.play(
            FadeIn(rule_3.shift(DOWN * 2))
        )

        self.next_section()

        self.fade_all_out()

    def fade_all_out(self, run_time=.2) -> None:
        self.play(
            *[FadeOut(mob, run_time=run_time)for mob in self.mobjects]
        )
