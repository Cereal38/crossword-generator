from PIL import Image, ImageDraw, ImageFont


def generate_crossword_png(grid, file_path="crossword.png"):
    # Calculate the grid size
    rows = grid.rows()
    cols = grid.columns()

    cell_size = 128

    # Define the font size
    font_size = 64

    # Create a font object with the desired size
    font = ImageFont.truetype("assets/fonts/HedvigLetters.ttf", font_size)
    
    # Calculate image size
    image_width = cols * cell_size
    image_height = rows * cell_size

    # Create a transparent image
    img = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # # Draw grid lines
    # for i in range(rows + 1):
    #     draw.line([(0, i * cell_size), (image_width, i * cell_size)], fill="black", width=line_width)

    # for j in range(cols + 1):
    #     draw.line([(j * cell_size, 0), (j * cell_size, image_height)], fill="black", width=line_width)

    # Draw crossword cells
    for i in range(rows):
        for j in range(cols):
            if grid.get_cell(i, j).get_letter() is not None:
                draw.rectangle(
                    [
                        (j * cell_size, i * cell_size),
                        ((j + 1) * cell_size, (i + 1) * cell_size),
                    ],
                    fill="white",
                    outline="black",
                )
                _, _, w, h = draw.textbbox(
                    (0, 0),
                    grid.get_cell(i, j).get_letter().upper(),
                    font=font,
                )
                draw.text(
                    (
                        j * cell_size + (cell_size - w) / 2,
                        i * cell_size + (cell_size - h) / 2,
                    ),
                    grid.get_cell(i, j).get_letter().upper(),
                    fill="black",
                    font=font,
                )

    # Save the image
    img.save(file_path)

