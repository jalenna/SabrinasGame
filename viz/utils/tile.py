from manim import *


class Tile:

    def __init__(self, w: int, h: int, x: float, y: float, z: float) -> None:
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.z = z
        self.color = RandomColorGenerator().next()

        self.visual: Rectangle = Rectangle(
            width=w, height=h, grid_xstep=1.0, grid_ystep=1.0).move_to((x, y, z)).set_style(stroke_width=2, fill_color=self.color, fill_opacity=1.).set_z_index(z)

    def reset_pos(self) -> None:
        self.visual.set_x(self.x)
        self.visual.set_y(self.y)
        self.visual.set_z(self.z)

    def get_pos(self) -> Vector:
        return Vector((self.x, self.y, self.z))


class Cell:

    def __init__(self, x: int, y: int, value=None) -> None:
        self.x = x
        self.y = y
        self.value = value
        self.neighbor_ids = []
