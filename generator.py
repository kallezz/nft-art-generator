import random
import numpy

from PIL import Image, ImageDraw
from blend_modes import blending_functions

size_px = 512
padding_px = 16


def generate_boxes():
    r = (255, 0, 0)
    g = (0, 255, 0)
    b = (0, 0, 255)
    boxes_b = Image.new("RGBA", size=(size_px, size_px), color=(0, 0, 0, 0))
    boxes_g = Image.new("RGBA", size=(size_px, size_px), color=(0, 0, 0, 0))
    boxes_r = Image.new("RGBA", size=(size_px, size_px), color=(0, 0, 0, 0))
    draw_blue = ImageDraw.Draw(boxes_b)
    draw_green = ImageDraw.Draw(boxes_g)
    draw_red = ImageDraw.Draw(boxes_r)
    y = size_px / 8
    for col in range(7):
        for row in range(7):
            width = random.randint(8, 32)
            offset = width / 4
            draw_blue.rectangle((
                (size_px / 8 * (row + 1) - width / 2 - offset, y - width / 2 - offset),
                (size_px / 8 * (row + 1) + width / 2 - offset, y + width / 2 - offset)
            ), fill=b)
            draw_green.rectangle((
                (size_px / 8 * (row + 1) - width / 2, y - width / 2),
                (size_px / 8 * (row + 1) + width / 2, y + width / 2)
            ), fill=g)
            draw_red.rectangle((
                (size_px / 8 * (row + 1) - width / 2 + offset, y - width / 2 + offset),
                (size_px / 8 * (row + 1) + width / 2 + offset, y + width / 2 + offset)
            ), fill=r)
        y += size_px / 8

    return [numpy.array(boxes_b).astype(float), numpy.array(boxes_g).astype(float), numpy.array(boxes_r).astype(float)]


def generate_art():
    bg_color = (15, 23, 42)

    image = Image.new("RGBA", size=(size_px, size_px), color=bg_color)
    n_image = numpy.array(image).astype(float)

    for i in range(1000):
        box_images = generate_boxes()

        l1 = blending_functions.addition(n_image, box_images[0], 1)
        l2 = blending_functions.addition(l1, box_images[1], 1)
        final = Image.fromarray(numpy.uint8(blending_functions.addition(l2, box_images[2], 1)))

        final.save("collection/nft_art_{}.png".format(str(i + 1).zfill(4)))


if __name__ == "__main__":
    generate_art()
