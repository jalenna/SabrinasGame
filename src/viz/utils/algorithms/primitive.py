from typing import Generator, cast
from tiling_algorithms.utils.types import iVec2D
from manim import PI, UL, Animation, Mobject, Rectangle


class PrimitiveSolver:
    @staticmethod
    def solve(dims: iVec2D, viz_board: Mobject, tiles: list[Rectangle]) -> Generator[list[Animation], None, None]:
        w, h = dims
        tile_w, tile_h = 1, 2

        sequence: list[Animation] = []

        start_x = viz_board.get_corner(UL)[0] + (tile_w / 2)
        start_y = viz_board.get_corner(UL)[1] - (tile_h / 2)

        last_row: int = 0
        for i, tile in enumerate(tiles):
            row, col = i // w, i % w
            if last_row != row:
                yield sequence
                sequence = []
            last_row = row

            target_pos: tuple[float, float, float] = (
                start_x + col * tile_w,
                start_y - row * tile_h,
                0
            )

            animation: Animation = cast(
                Animation, tile.animate.restore().move_to(target_pos))

            if row >= h // 2:
                target_pos = (
                    start_x + .5 + col * tile_w * 2,
                    start_y + .5 - row * tile_h,
                    0
                )
                animation = cast(Animation, tile.animate.restore().move_to(
                    target_pos).rotate(PI / 2))

            sequence.append(animation)

        yield sequence
