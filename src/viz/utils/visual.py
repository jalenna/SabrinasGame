from random import random
from manim_slides.slide import Slide
from manim import DR, FadeIn, FadeOut, Rectangle, Text, Vector, RandomColorGenerator


def reset_slide(slide: Slide) -> None:
    fade_all_out(slide)
    slide.move_camera(zoom=1., frame_center=(0., 0., 0.))


def fade_all_out(slide: Slide, run_time: float = .2) -> None:
    mobs_to_fade = [
        mob for mob in slide.mobjects
        if mob is not getattr(slide, 'current_slide_number', None)
    ]

    if mobs_to_fade:
        slide.play(
            *[FadeOut(mob, run_time=run_time) for mob in mobs_to_fade]
        )
    # slide.play(
    #     *[FadeOut(mob, run_time=run_time) for mob in slide.mobjects]
    # )


def show_slide_number(slide: Slide, update: bool = True) -> None:
    if update:
        slide.play(FadeOut(slide.current_slide_number))

    new_slide_number = Text(
        str(slide.slide_tracker.current), font_size=32).to_edge(DR)
    slide.add_fixed_in_frame_mobjects(new_slide_number)
    slide.current_slide_number = new_slide_number

    slide.play(FadeIn(slide.current_slide_number))


def create_tiles(count: int, offset: Vector, color_gen: RandomColorGenerator, show_grid_lines: bool = True, fill: float = 1.) -> list[Rectangle]:
    return [create_tile(color_gen, offset, show_grid_lines, fill).set_z(i * .2) for i in range(count)]


def create_tile(color_gen: RandomColorGenerator, offset: Vector, show_grid_lines: bool = True, fill: float = 1.) -> Rectangle:
    tile: Rectangle = Rectangle(fill_color=color_gen.next(), fill_opacity=fill, height=2, width=1, grid_xstep=1.0 if show_grid_lines else None,
                                grid_ystep=1.0 if show_grid_lines else None)
    tile.set_x(tile.get_x() + offset.get_x() + random())
    tile.set_y(tile.get_y() + offset.get_y() + random())
    tile.save_state()
    return tile
