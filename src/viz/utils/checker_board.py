import os
from PIL import Image


def generate_chessboard_images(cell_size=100, output_dir="./data_out/checkers/"):
    """
    Generates a full chessboard, an image with only black cells, 
    and an image with only white cells using transparent backgrounds.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    board_size = 8 * cell_size

    full_board = Image.new("RGBA", (board_size, board_size), (0, 0, 0, 0))
    black_only = Image.new("RGBA", (board_size, board_size), (0, 0, 0, 0))
    white_only = Image.new("RGBA", (board_size, board_size), (0, 0, 0, 0))

    COLOR_A = (255, 0, 0, 255)
    COLOR_B = (0, 0, 0, 255)

    for row in range(8):
        for col in range(8):
            left = col * cell_size
            top = row * cell_size
            right = left + cell_size
            bottom = top + cell_size
            box = (left, top, right, bottom)

            if (row + col) % 2 == 0:
                cell_white = Image.new(
                    "RGBA", (cell_size, cell_size), COLOR_A)
                full_board.paste(cell_white, box)
                white_only.paste(cell_white, box)
            else:
                cell_black = Image.new(
                    "RGBA", (cell_size, cell_size), COLOR_B)
                full_board.paste(cell_black, box)
                black_only.paste(cell_black, box)

    full_board.save(os.path.join(output_dir, "full_board.png"))
    black_only.save(os.path.join(output_dir, "b_cells_only.png"))
    white_only.save(os.path.join(output_dir, "a_cells_only.png"))

    print(f"Successfully generated 3 images in the '{output_dir}' directory!")


if __name__ == "__main__":
    generate_chessboard_images(cell_size=100)
