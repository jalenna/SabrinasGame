from manim import *
from typing import Any
from random import seed
from manim_slides.slide import ThreeDSlide
from src.viz.utils.trackers import JSlideNumberTracker
from src.viz.utils.algorithms.mcmf import JStateMCMFSolver
from SabrinasGame.src.tiling_algorithms.utils.core import absdiff
from src.viz.utils.algorithms.linear_greedy import LinearGreedySolver
from src.viz.utils.algorithms.dfs import JDepthSolver, JGuidedDepthSolver
from SabrinasGame.src.tiling_algorithms.utils.types import Pairs, Tiles, iVec2D
from src.viz.utils.algorithms.utils.board_generator import VisualBoardGenerator

color_generator: RandomColorGenerator = RandomColorGenerator(42)


class BasePresentation(ThreeDSlide):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        seed(42)
        self.board_generator: VisualBoardGenerator = VisualBoardGenerator()
        self.slide_tracker: JSlideNumberTracker = JSlideNumberTracker()
        self.skip_reversing = True
        self.depth_solver: JDepthSolver = JDepthSolver()
        self.guided_depth_solver: JGuidedDepthSolver = JGuidedDepthSolver()
        self.linear_solver: LinearGreedySolver = LinearGreedySolver()
        self.mcmf_solver: JStateMCMFSolver = JStateMCMFSolver(absdiff)
        self.cost_range: tuple[int, int] = (1, 20)
        self.problematic_tiles_dim: iVec2D = iVec2D(6, 6)
        self.problematic_tiles: Tiles = [
            1., 3.,   5.,  7., 2., 4.,
            2., 4.,   8.,  9., 5., 7.,
            3., 5.,   8.,  4., 8., 6.,
            6., 8.,  10.,  9., 1., 1.,
            5., 11., 15., 15., 9., 5.,
            1., 12., 18.,  3., 2., 3.,
        ]
        self.slide_category: VGroup = VGroup()


def reset_slide(slide: ThreeDSlide) -> None:
    fade_all_out(slide)
    slide.move_camera(zoom=1., frame_center=(0., 0., 0.))


def fade_all_out(slide: ThreeDSlide, run_time: float = .2) -> None:
    mobs_to_fade = [
        mob for mob in slide.mobjects
        if (mob is not getattr(slide, 'slide_number_text', None)) and (mob is not getattr(slide, "slide_category", None))
    ]

    if mobs_to_fade:
        slide.play(
            *[FadeOut(mob, run_time=run_time) for mob in mobs_to_fade]
        )


def create_pairings(visual_board: VGroup, pairs: Pairs, fill_opacity: float = .4) -> list[SurroundingRectangle]:
    tiles: list[SurroundingRectangle] = []

    for a, b in enumerate(pairs):
        color: ManimColor = color_generator.next()
        if b == -1:
            continue
        tiles.append(SurroundingRectangle(
            visual_board[a], visual_board[b], color=color, fill_color=color, fill_opacity=fill_opacity, buff=-0.1))

    return tiles


def create_tiles(count: int) -> list[Rectangle]:
    return [create_tile() for _ in range(count)]


def create_tile() -> Rectangle:
    tile: Rectangle = Rectangle(
        color=color_generator.next(),
        height=2,
        width=1,
    )
    return tile


def normalized_neighbor_proximity(cost: float, neighbors: list[float]) -> list[float]:
    result: list[float] = [absdiff(cost, n) for n in neighbors]
    furthest: float = max(result)
    result = [v / furthest for v in result]
    return result


def create_label(text: str) -> Label:
    return Label(Text(text, font_size=20), frame_config={"buff": .1, "stroke_width": .5}, box_config={"buff": .5})
