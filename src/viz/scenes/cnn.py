from manim import *
from manim_slides.slide import ThreeDSlide
from random import randrange, seed as rand_seed
from viz.utils.tile import Cell
from typing import cast
config["max_files_cached"] = -1


class CNNSlide(ThreeDSlide):
    skip_reversing = True

    _required_tiles: int = 0
    _curr_num_tiles: int = 0

    def construct(self) -> None:
        rand_seed(42)

        text: Text = Text("CNN animation #TODO")

        slide_number: Text = Text("23/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(Write(slide_number), FadeIn(text))
