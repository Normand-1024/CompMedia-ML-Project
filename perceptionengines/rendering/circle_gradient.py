import sys
import math
from PIL import Image, ImageDraw
import numpy as np
import csv

last_x = -1
last_y = -1
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
    global last_x
    global last_y
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

    # now draw lines
    min_dist = 0.04 * size
    max_dist = 0.05 * size
    max_color_dist = 40
    min_rad = 0.04 * size
    max_rad = 0.06 * size
    margin = 0.02 * size
    for e in rest:
        # line position and raidus
        if (last_x is -1):
          last_x = int(size / 2)
          last_y = int(size / 2)
          
        x1 = map_number(e[0], 0, 1, min_dist, max_dist)
        y1 = map_number(e[1], 0, 1, min_dist, max_dist)
        if (e[2] < 0.5):
          x1 = x1 * -1
        if (e[3] < 0.5):
          y1 = y1 * -1
          
        x1 = clamp_range(last_x + x1, 0, size)
        y1 = clamp_range(last_y + y1, 0, size)
        last_x = x1
        last_y = y1

        r = map_number(e[7], 0, 1, min_rad, max_rad)

        # determine foreground color from header
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

        # draw line with round line caps (circles at the end)
        draw.ellipse((x1-r, y1-r, x1+r, y1+r), fill=(R, G, B))

    # Reinitialize global vars
    last_x = -1
    last_y = -1
    last_r = -1
    last_g = -1
    last_b = -1

    return im
