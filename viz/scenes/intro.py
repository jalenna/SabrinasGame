from manim import *
from manim_slides.slide import ThreeDSlide
from viz.utils.tile import Tile
from random import random

config["max_files_cached"] = -1


class IntroSlide(ThreeDSlide):
    skip_reversing = True

    def construct(self) -> None:

        board: Rectangle = Rectangle(
            width=2, height=2, grid_xstep=1.0, grid_ystep=1.0).set_style(stroke_width=2, stroke_color=BLUE_D).set_z_index(99)

        self.set_camera_orientation(
            phi=75 * DEGREES, theta=-60 * DEGREES, zoom=.5)

        self.play(Create(board, run_time=2, lag_ratio=.1))

        tile_offset: Vector = Vector((-20., 0., 0.))

        tiles: list[Tile] = [Tile(1, 2, random(), random(), i * .1)
                             for i in range(25)]

        for tile in tiles:
            tile.visual.set_x(tile.visual.get_x() + tile_offset.get_x())
            tile.visual.set_y(tile.visual.get_y() + tile_offset.get_y())
            self.play(GrowFromCenter(tile.visual, run_time=.1))

        self.move_camera(phi=0, theta=-90 * DEGREES)
        slide_number: Text = Text("1/10").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(FadeIn(slide_number))

        self.next_section()

        self.play(Circumscribe(board))

        self.next_section()

        tile_bounds: Rectangle = Rectangle(4, 4).move_to((
            max(tiles, key=lambda x: abs(x.x)).x + tile_offset.get_x(),
            max(tiles, key=lambda x: abs(x.y)).y + tile_offset.get_y(),
            0.
        ))

        self.move_camera(
            phi=75 * DEGREES, theta=-60 * DEGREES, zoom=1., frame_center=tile_bounds)

        self.play(Circumscribe(tile_bounds))

        self.move_camera(phi=0, theta=-90 * DEGREES,
                         frame_center=(0., 0., 0.), zoom=.5)

        self.next_section()

        seq: list = []
        for i in range(len(tiles) - 1):
            seq.append(FadeOut(tiles[i].visual))
        self.play(*seq)
        seq = []

        self.play(FadeOut(board, run_time=.3))

        selected_tile: Tile = tiles[-1]
        og_pos: Vector = selected_tile.get_pos()
        self.play(selected_tile.visual.animate.move_to((0, 0, og_pos.get_z())))

        self.wait(2)

        for i in range(len(tiles) - 1):
            seq.append(FadeIn(tiles[i].visual, run_time=.1))
        self.play(*seq)
        seq = []

        self.play(
            selected_tile.visual.animate.move_to(
                (
                    og_pos.get_x() + tile_offset.get_x(),
                    og_pos.get_y() + tile_offset.get_y(),
                    og_pos.get_z()
                )
            )
        )
        self.play(FadeIn(board, run_time=.3))

        self.next_slide()
        t_slide_number: Text = Text("2/10").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(ReplacementTransform(slide_number, t_slide_number))
        slide_number = t_slide_number

        self.play(tiles[-1].visual.animate.move_to((.5, 0, 0)))
        self.play(tiles[-2].visual.animate.move_to((-.5, 0, 0)))

        t_board = Rectangle(
            width=2, height=3, grid_xstep=1.0, grid_ystep=1.0).set_style(stroke_width=2, stroke_color=BLUE_D).set_z_index(99)
        self.play(
            ReplacementTransform(board, t_board),
            tiles[-1].visual.animate.move_to((.5, .5, 0.)),
            tiles[-2].visual.animate.move_to((-.5, .5, 0.)),
        )
        board = t_board

        selected_tile = tiles[-3]
        self.play(selected_tile.visual.animate.move_to((-3., 1.5, 0.)))

        for i in range(len(tiles) - 3):
            seq.append(FadeOut(tiles[i].visual))
        self.play(*seq)
        seq = []

        self.next_section()

        self.play(selected_tile.visual.animate.move_to((-.5, -1.5, 0.)))
        self.play(selected_tile.visual.animate.move_to((.5, -1.5, 0.)))

        self.play(
            Circumscribe(
                Rectangle(height=1, width=2).move_to((0., -1., 0.))
            ),
            Blink(Cross(Square(1).move_to((-.5, -1., 0.))
                        ).scale(.5), blinks=5, hide_at_end=True),
            Blink(Cross(Square(1).move_to((.5, -1., 0.))).scale(.5),
                  blinks=5, hide_at_end=True),
            selected_tile.visual.animate.move_to((-3., 1.5, 0.))
        )

        self.next_section()

        self.play(Rotate(selected_tile.visual, 90 * DEGREES))

        self.wait(2)

        self.play(Rotate(selected_tile.visual, 90 * DEGREES))
        self.wait(1)
        self.play(Rotate(selected_tile.visual, 90 * DEGREES))
        self.wait(1)
        self.play(Rotate(selected_tile.visual, 90 * DEGREES))

        self.next_section()

        self.play(Rotate(selected_tile.visual, 90 * DEGREES))
        self.play(selected_tile.visual.animate.move_to((-0., -1., 0.)))

        t_board = Rectangle(
            width=3, height=2, grid_xstep=1.0, grid_ystep=1.0).set_style(stroke_width=2, stroke_color=BLUE_D).set_z_index(99)
        self.play(
            ReplacementTransform(board, t_board),
            tiles[-1].visual.animate.move_to((0., 0., 0.)),
            tiles[-2].visual.animate.move_to((-1., 0., 0.)),
            FadeOut(tiles[-3].visual),
        )
        board = t_board

        self.reset_tile(tiles[-3], tile_offset)
        self.play(FadeIn(tiles[-3].visual))

        self.next_section()

        self.play(tiles[-3].visual.animate.move_to((1., 0., 0.)))

        t_board = Rectangle(
            width=3, height=3, grid_xstep=1.0, grid_ystep=1.0).set_style(stroke_width=2, stroke_color=BLUE_D).set_z_index(99)
        self.play(
            tiles[-1].visual.animate.move_to((0., .5, 0.)),
            tiles[-2].visual.animate.move_to((-1., .5, 0.)),
            tiles[-3].visual.animate.move_to((1., .5, 0.)),
            ReplacementTransform(board, t_board),
        )
        board = t_board

        selected_tile = tiles[-4]
        self.play(FadeIn(selected_tile.visual))

        self.next_section()

        self.play(Rotate(selected_tile.visual, 90 * DEGREES))
        self.play(selected_tile.visual.animate.move_to((-.5, -1., 0.)))

        self.next_section()

        t_board = Rectangle(
            width=3, height=4, grid_xstep=1.0, grid_ystep=1.0).set_style(stroke_width=2, stroke_color=BLUE_D).set_z_index(99)
        self.play(
            tiles[-1].visual.animate.move_to((0., 1., 0.)),
            tiles[-2].visual.animate.move_to((-1., 1., 0.)),
            tiles[-3].visual.animate.move_to((1., 1., 0.)),
            tiles[-4].visual.animate.move_to((-.5, -.5, 0.)),
            ReplacementTransform(board, t_board),
        )
        board = t_board

        self.play(FadeIn(tiles[-5].visual, run_time=.3))
        self.play(FadeIn(tiles[-6].visual, run_time=.3))

        self.next_section()

        self.play(Rotate(tiles[-5].visual, 90 * DEGREES))
        self.play(
            tiles[-5].visual.animate.move_to((-.5, -1.5, 0.)),
            tiles[-6].visual.animate.move_to((1., -1., 0.))
        )

        t_board = Rectangle(
            width=4, height=4, grid_xstep=1.0, grid_ystep=1.0).set_style(stroke_width=2, stroke_color=BLUE_D).set_z_index(99)
        self.play(
            tiles[-1].visual.animate.move_to((-.5, 1., 0.)),
            tiles[-2].visual.animate.move_to((-1.5, 1., 0.)),
            tiles[-3].visual.animate.move_to((.5, 1., 0.)),
            tiles[-4].visual.animate.move_to((-1., -.5, 0.)),
            tiles[-5].visual.animate.move_to((-1., -1.5, 0.)),
            tiles[-6].visual.animate.move_to((.5, -1., 0.)),
            ReplacementTransform(board, t_board),
        )
        board = t_board

        self.play(FadeIn(tiles[-7].visual, run_time=.3))
        self.play(FadeIn(tiles[-8].visual, run_time=.3))

        self.next_section()

        self.play(
            tiles[-7].visual.animate.move_to((1.5, 1., 0.)),
            tiles[-8].visual.animate.move_to((1.5, -1., 0.))
        )

        t_board = Rectangle(
            width=4, height=5, grid_xstep=1.0, grid_ystep=1.0).set_style(stroke_width=2, stroke_color=BLUE_D).set_z_index(99)
        self.play(
            tiles[-1].visual.animate.move_to((-.5, 1.5, 0.)),
            tiles[-2].visual.animate.move_to((-1.5, 1.5, 0.)),
            tiles[-3].visual.animate.move_to((.5, 1.5, 0.)),
            tiles[-4].visual.animate.move_to((-1., 0., 0.)),
            tiles[-5].visual.animate.move_to((-1., -1., 0.)),
            tiles[-6].visual.animate.move_to((.5, -.5, 0.)),
            tiles[-7].visual.animate.move_to((1.5, 1.5, 0.)),
            tiles[-8].visual.animate.move_to((1.5, -.5, 0.)),
            ReplacementTransform(board, t_board),
        )
        board = t_board

        self.play(FadeIn(tiles[-9].visual, run_time=.3))
        self.play(FadeIn(tiles[-10].visual, run_time=.3))

        self.next_section()

        self.play(
            Rotate(tiles[-9].visual, 90 * DEGREES),
            Rotate(tiles[-10].visual, 90 * DEGREES),
        )

        self.play(
            tiles[-9].visual.animate.move_to((-1., -2., 0.)),
            tiles[-10].visual.animate.move_to((1, -2., 0.))
        )

        t_board = Rectangle(
            width=5, height=4, grid_xstep=1.0, grid_ystep=1.0).set_style(stroke_width=2, stroke_color=BLUE_D).set_z_index(99)
        self.play(
            tiles[-1].visual.animate.move_to((-1, 1., 0.)),
            tiles[-2].visual.animate.move_to((-2., 1., 0.)),
            tiles[-3].visual.animate.move_to((0., 1., 0.)),
            tiles[-4].visual.animate.move_to((-1.5, -.5, 0.)),
            tiles[-5].visual.animate.move_to((-1.5, -1.5, 0.)),
            tiles[-6].visual.animate.move_to((0., -1., 0.)),
            tiles[-7].visual.animate.move_to((1., 1., 0.)),
            tiles[-8].visual.animate.move_to((1., -1., 0.)),
            FadeOut(tiles[-9].visual),
            FadeOut(tiles[-10].visual),
            ReplacementTransform(board, t_board),
        )
        board = t_board

        self.reset_tile(tiles[-9], tile_offset)
        self.reset_tile(tiles[-10], tile_offset)
        self.play(FadeIn(tiles[-9].visual, run_time=.3))
        self.play(FadeIn(tiles[-10].visual, run_time=.3))

        self.next_section()

        self.play(
            tiles[-9].visual.animate.move_to((2., 1., 0.)),
            tiles[-10].visual.animate.move_to((2., -1., 0.))
        )

        t_board = Rectangle(
            width=5, height=5, grid_xstep=1.0, grid_ystep=1.0).set_style(stroke_width=2, stroke_color=BLUE_D).set_z_index(99)
        self.play(
            tiles[-1].visual.animate.move_to((-1, 1.5, 0.)),
            tiles[-2].visual.animate.move_to((-2., 1.5, 0.)),
            tiles[-3].visual.animate.move_to((0., 1.5, 0.)),
            tiles[-4].visual.animate.move_to((-1.5, 0., 0.)),
            tiles[-5].visual.animate.move_to((-1.5, -1., 0.)),
            tiles[-6].visual.animate.move_to((0., -.5, 0.)),
            tiles[-7].visual.animate.move_to((1., 1.5, 0.)),
            tiles[-8].visual.animate.move_to((1., -.5, 0.)),
            tiles[-9].visual.animate.move_to((2., 1.5, 0.)),
            tiles[-10].visual.animate.move_to((2., -.5, 0.)),
            ReplacementTransform(board, t_board),
        )
        board = t_board

        self.play(FadeIn(tiles[-11].visual, run_time=.3))
        self.play(FadeIn(tiles[-12].visual, run_time=.3))

        self.next_section()

        self.play(
            Rotate(tiles[-11].visual, 90 * DEGREES),
            Rotate(tiles[-12].visual, 90 * DEGREES),
        )

        self.play(
            tiles[-11].visual.animate.move_to((-1.5, -2, 0.)),
            tiles[-12].visual.animate.move_to((0.5, -2, 0.))
        )

        im: ImageMobject = ImageMobject(
            "./assets/adress_me.jpg")
        im.height = 1.
        im.width = 1.
        im.move_to((2.4, -2.4, 0.))
        self.wait(1)
        self.move_camera(frame_center=(2., -2., 0.))
        _, _, _, _, zoom = self.camera.get_value_trackers()
        self.play(
            AnimationGroup((zoom.animate.set_value(5.),),
                           run_time=5, rate_func=rate_functions.ease_in_out_circ
                           )
        )
        self.play(FadeIn(im))

        self.wait(3)

        self.play(
            FadeOut(*(tiles[i].visual for i in range(-1, -13, -1))),
            FadeOut(board),
            FadeOut(im),
        )

        self.move_camera(zoom=1., frame_center=(0., 0., 0.))

        self.wait()

    def reset_tile(self, tile: Tile, offest: Vector, rotate: bool = True) -> None:
        tile.reset_pos()
        og_pos = tile.get_pos()

        if rotate:
            tile.visual.rotate(90 * DEGREES)

        tile.visual.move_to(
            (
                og_pos.get_x() + offest.get_x(),
                og_pos.get_y() + offest.get_y(),
                og_pos.get_z()
            )
        )
