import sys
import math
from PIL import Image, ImageDraw
import numpy as np
import csv

# canonical interpolation function, like https://p5js.org/reference/#/p5/map
def map_number(n, start1, stop1, start2, stop2):
  return ((n-start1)/(stop1-start1))*(stop2-start2)+start2

# input: array of real vectors, length 8, each component normalized 0-1
def render(a, size):

    # determine background color from header
    R = int(map_number(a[0][0], 0, 1, 0, 255))
    G = int(map_number(a[0][1], 0, 1, 0, 255))
    B = int(map_number(a[0][2], 0, 1, 0, 255))

    # create the image and drawing context
    im = Image.new('RGB', (size, size), (R, G, B))
    draw = ImageDraw.Draw(im, 'RGB')

    # now draw lines
    min_width = 0.007 * size
    max_width = 0.007 * size

    flipper = Image.open("assets/goldfish/flipper.png")
    eyeball = Image.open("assets/goldfish/eyeball.png")

    for i in range(1, len(a)):
        if(i==1):
            x1 = map_number(a[i][0], 0, 1, 0, size)
            y1 = map_number(a[i][1], 0, 1, 0, size)
            x2 = map_number(a[i][2], 0, 1, 0, size)
            y2 = map_number(a[i][3], 0, 1, 0, size)
            R2 = int(map_number(a[i][4], 0, 1, 0, 255))
            G2 = int(map_number(a[i][5], 0, 1, 0, 255))
            B2 = int(map_number(a[i][6], 0, 1, 0, 255))
            draw.ellipse((x1, y1, x2, y2), fill=(R2, G2, B2))
        elif (i < 4):
            flipperTemp = flipper
            # flip
            if (a[i][5] > 0.5):
                flipperTemp = flipperTemp.transpose(Image.FLIP_LEFT_RIGHT)
            # rotate
            px, py = int(map_number(a[i][3], 0, 1, 0, size)), int(map_number(a[i][4], 0, 1, 0, size))
            sx, sy = flipperTemp.size
            flipperTemp = flipperTemp.rotate(map_number(a[i][1], 0, 1, 0, 364), expand=1)

            im.paste(flipperTemp, (px, py), flipperTemp)
        elif (i < 6):
            flipperTemp = eyeball
            # flip
            if (a[i][0] > 0.5):
                flipperTemp = flipperTemp.transpose(Image.FLIP_LEFT_RIGHT)
            # rotate
            px, py = int(map_number(a[i][3], 0, 1, 0, size)), int(map_number(a[i][4], 0, 1, 0, size))
            sx, sy = flipperTemp.size
            flipperTemp = flipperTemp.rotate(map_number(a[i][1], 0, 1, 0, 364), expand=1)

            im.paste(flipperTemp, (px, py), flipperTemp)

        # w2 = int(map_number(a[i][4], 0, 1, min_width, max_width))
        # # line width
        # w = 2 * w2 + 2
        # # line position
        # x1 = map_number(a[i][0], 0, 1, w2, size - w2)
        # y1 = map_number(a[i][1], 0, 1, w2, size - w2)
        # # x2 = map_number(e[2], 0, 1, w2, size-w2)
        # # y2 = map_number(e[3], 0, 1, w2, size-w2)
        #
        # # determine foreground color from header
        # R = int(map_number(a[i][4], 0, 1, 0, 255))
        # G = int(map_number(a[i][5], 0, 1, 0, 255))
        # B = int(map_number(a[i][6], 0, 1, 0, 255))
        #
        # # circle
        # if (i < 15):
        #     draw.ellipse((x1 - w2, y1 - w2, x1 + w2, y1 + w2), fill=(R, G, B))
        # # square
        # elif (i < 30):
        #     draw.rect((x1 - w2, y1 - w2, x1 + w2, y1 + w2), fill=(R, G, B))
        # # triangle
        # elif (i <= 45):
        #     draw.polygon((x1 - w2, y1 - w2, x1 + w2, y1 + w2), fill=(R, G, B))

    return im
