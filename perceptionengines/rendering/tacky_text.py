import sys
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import csv

last_r = -1
last_g = -1
last_b = -1

# canonical interpolation function, like https://p5js.org/reference/#/p5/map
def map_number(n, start1, stop1, start2, stop2):
  return ((n-start1)/(stop1-start1))*(stop2-start2)+start2

def clamp_range(n, min, max):
  if n < min:
    return min
  if n > max:
    return max
  return n

# input: array of real vectors, length 8, each component normalized 0-1
def render(a, size):
    global last_r
    global last_g
    global last_b

    # split input array into header and rest
    header_length = 2
    head = a[:header_length]
    rest = a[header_length:]

    # determine background color from header
    R = int(map_number(head[0][0], 0, 1, 0, 255))
    G = int(map_number(head[0][1], 0, 1, 0, 255))
    B = int(map_number(head[0][2], 0, 1, 0, 255))

    # create the image and drawing context
    im = Image.new('RGB', (size, size), (R, G, B))
    draw = ImageDraw.Draw(im, 'RGB')
    text = 'chirp'
    font = "font/Montaseli Sans.otf"
    font20 = ImageFont.truetype(font, size=20)
    font35 = ImageFont.truetype(font, size=30)
    font50 = ImageFont.truetype(font, size=40)

    # now draw texts
    # [x1, y1, rotation, R, G, B]
    left_margin = 0.04 * size
    right_margin = 0.96 * size
    max_color_dist = 30
    for e in rest:
        # line position
        x1 = map_number(e[0], 0, 1, left_margin, right_margin)
        y1 = map_number(e[1], 0, 1, left_margin, right_margin)
        x2 = map_number(e[2], 0, 1, left_margin, right_margin)
        y2 = map_number(e[3], 0, 1, left_margin, right_margin)

        # determine foreground color
        R = 0
        G = 0
        B = 0
        if (last_r is -1):
          R = int(map_number(e[4], 0, 1, 0, 255))
          G = int(map_number(e[5], 0, 1, 0, 255))
          B = int(map_number(e[6], 0, 1, 0, 255))
        else:
          R = int(clamp_range(\
            last_r + map_number(e[4], 0, 1, -max_color_dist, max_color_dist),\
             0,\
             255)\
            )
          G = int(clamp_range(\
            last_g + map_number(e[5], 0, 1, -max_color_dist, max_color_dist),\
             0,\
             255)\
            )
          B = int(clamp_range(\
            last_b + map_number(e[6], 0, 1, -max_color_dist, max_color_dist),\
             0,\
             255)\
            )
        last_r = R
        last_g = G
        last_b = B

        # draw text
        draw.text((x1, y1), text, fill=(R,G,B), font=font20)
        draw.text((x1 + (x2 - x1) * 0.2, y1 + (y2 - y1) * 0.4), text, fill=(R,G,B), font=font35)
        draw.text((x1 + (x2 - x1) * 0.4, y1 + (y2 - y1) * 0.4), text, fill=(R,G,B), font=font35)
        draw.text((x1 + (x2 - x1) * 0.6, y1 + (y2 - y1) * 0.6), text, fill=(R,G,B), font=font35)
        draw.text((x1 + (x2 - x1) * 0.8, y1 + (y2 - y1) * 0.6), text, fill=(R,G,B), font=font35)
        draw.text((x1, y1), text, fill=(R,G,B), font=font20)

    last_r = -1
    last_g = -1
    last_b = -1

    return im
