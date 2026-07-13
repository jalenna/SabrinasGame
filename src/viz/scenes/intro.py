from manim import *
from typing import Any
from random import seed as rand_seed
from manim_slides.slide import ThreeDSlide
from src.viz.utils.trackers import JSlideNumberTracker
from src.algorithms.utils.types import ExplicitDims, iVec2D
from src.viz.utils.algorithms.primitive import PrimitiveSolver
from src.viz.utils.visual import create_tiles, reset_slide, show_slide_number
from src.viz.utils.algorithms.utils.board_generator import VizBoardGenerator

config["max_files_cached"] = -1


class IntroSlide(ThreeDSlide):
    skip_reversing = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.tile_w, self.tile_h = 1, 2
        self.primitive_solver: PrimitiveSolver = PrimitiveSolver()
        self.color_gen: RandomColorGenerator = RandomColorGenerator(42)
        self.slide_tracker: JSlideNumberTracker = JSlideNumberTracker()
        self.current_slide_number: Text = Text(
            str(self.slide_tracker.current), font_size=32).to_edge(DR)

    def construct(self) -> None:
        rand_seed(42)

        self.intro()
        self.tile()

    def intro(self) -> None:
        self.set_camera_orientation(
            phi=75 * DEGREES, theta=-60 * DEGREES, zoom=.5)

        tile_offset: Vector = Vector((-20., 0., 0.))

        board_generator: VizBoardGenerator = VizBoardGenerator()
        board_generator.generate(ExplicitDims([(2, 2)]), (1, 10))
        board: Rectangle = board_generator.viz_boards[0]
        self.play(Create(board, run_time=2, lag_ratio=.1))

        tiles: list[Rectangle] = create_tiles(2, tile_offset, self.color_gen)

        self._reveal_tiles(tiles)

        self.move_camera(phi=0, theta=-90 * DEGREES)

        show_slide_number(self, update=False)

        self.next_section()

        self.play(Circumscribe(board))

        self.next_section()

        tile_bounds: Rectangle = Rectangle(5, 5).move_to(
            (
                max(tiles, key=lambda x: abs(x.get_x())
                    ).get_x(),
                max(tiles, key=lambda x: abs(x.get_y())
                    ).get_y(),
                0.
            )
        )

        self.move_camera(
            phi=75 * DEGREES, theta=-60 * DEGREES, zoom=1., frame_center=tile_bounds)

        self.play(Circumscribe(tile_bounds))

        self.move_camera(phi=0, theta=-90 * DEGREES,
                         frame_center=(0., 0., 0.), zoom=.5)

        self.next_section()

        self.play(
            *(animation for animations in self.primitive_solver.solve(iVec2D(2, 2),
                                                                      board, tiles) for animation in animations)
        )

        self.next_slide()
        reset_slide(self)

    def tile(self) -> None:
        self.slide_tracker.inc()
        show_slide_number(self)
        self.move_camera(phi=0, theta=-90 * DEGREES,
                         frame_center=(0., 0., 0.), zoom=.5)

        tile_offset: Vector = Vector((-20., 0., 0.))

        gen_dims: ExplicitDims = ExplicitDims(
            [
                (2, 3),
                (3, 2),
                (3, 3),
                (3, 4),
                (4, 3),
                (4, 4),
                (4, 5),
                (5, 4),
                (5, 5),
            ]
        )
        board_generator: VizBoardGenerator = VizBoardGenerator()
        board_generator.generate(gen_dims, (1, 10))

        tiles: list[Rectangle] = create_tiles(
            25 // 2, tile_offset, self.color_gen)

        prev_board: Rectangle = board_generator.viz_boards[0]
        self._reveal_tiles(tiles)

        tiles.reverse()

        prev_required_num_tiles: int = 0
        for i, board in enumerate(board_generator.viz_boards):
            dims: iVec2D = board_generator.boards[i][1]
            required_num_tiles: int = (dims.x * dims.y) // 2

            if i == 0:
                self.play(Create(board, run_time=1.5, lag_ratio=.1))
            else:
                self.play(tile.animate.fade(.3)
                          for tile in tiles[:prev_required_num_tiles])
                self.play(ReplacementTransform(prev_board, board))
                self.play(tile.animate.fade(0.)
                          for tile in tiles[:prev_required_num_tiles])
                prev_board = board

            self.play(
                LaggedStart(
                    *(animation for animations in self.primitive_solver.solve(dims,
                      board, tiles[:required_num_tiles]) for animation in animations),
                    run_time=1.5
                )
            )

            prev_required_num_tiles = required_num_tiles
            self.wait(1)

        im: ImageMobject = ImageMobject(
            "./assets/adress_me.jpg")
        im.height = 1.
        im.width = 1.
        im.move_to((2.4, -2.4, 0.))
        im.set_z_index(-1)
        self.move_camera(frame_center=(2., -2., 0.))
        _, _, _, _, zoom = self.camera.get_value_trackers()
        self.play(
            AnimationGroup((zoom.animate.set_value(5.),),
                           run_time=5, rate_func=rate_functions.ease_in_out_circ
                           )
        )
        self.play(FadeIn(im))

        self.wait(2)

        reset_slide(self)

    def _reveal_tiles(self, tiles: list[Rectangle]) -> None:
        self.play(Succession(GrowFromCenter(tile, run_time=.1))
                  for tile in tiles)
