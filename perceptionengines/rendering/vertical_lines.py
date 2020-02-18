import sys
import math
from PIL import Image, ImageDraw
import numpy as np
import csv
import random

last_x = -1
last_y = -1
last_r = -1
last_g = -1
last_b = -1
last_a = -1

def grouped(iterable, n):
  "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
  return zip(*[iter(iterable)]*n)

# canonical interpolation function, like https://p5js.org/reference/#/p5/map
def map_number(n, start1, stop1, start2, stop2):
  return ((n-start1)/(stop1-start1))*(stop2-start2)+start2;

def clamp_range(n, min, max):
  if n < min:
    return min
  if n > max:
    return max
  return n

def line_normal_sampling(density, x1, y1, x2, y2, size):
    points = []
    slope = (y2 - y1) / (x2 - x1)
    constant = y1 - (slope*x1)

    n = int(density * (((x2-x1)**2 + (y2-y1)**2)**(0.5)))
    x_inc = (x2-x1)/n
    x_n1 = x1
    dir_vec = (x2-x1, y2-y1)
    dir_vec /= (dir_vec[0]**2 + dir_vec[1]**2)**(0.5)
    
    normal_dir_vec = (dir_vec[1], -dir_vec[0])
    normal_dir_vec /= (normal_dir_vec[0]**2 + normal_dir_vec[1]**2)**(0.5)

    for i in range(0, n):
        curr_size = random.randint(4, size)
        x_n1 += x_inc
        y_n1 = x_n1*slope + constant
        x_n2 = normal_dir_vec[0]*curr_size + x_n1
        y_n2 = normal_dir_vec[1]*curr_size + y_n1
        x_n3 = -normal_dir_vec[0]*curr_size + x_n1
        y_n3 = -normal_dir_vec[1]*curr_size + y_n1
        normal_line_up = (x_n1, y_n1, x_n2, y_n2)
        normal_line_down = (x_n1, y_n1, x_n3, y_n3)
        points.append(normal_line_up)
        points.append(normal_line_down)

    return points

# input: array of real vectors, length 8, each component normalized 0-1
def render(a, size):
    global last_x
    global last_y
    global last_r
    global last_g
    global last_b
    global last_a

    # split input array into header and rest
    header_length = 2
    head = a[:header_length]
    rest = a[header_length:]

    # determine background color from header
    R = int(map_number(head[0][0], 0, 1, 0, 255))
    G = int(map_number(head[0][1], 0, 1, 0, 255))
    B = int(map_number(head[0][2], 0, 1, 0, 255))
    A = int(map_number(head[0][3], 0.1, 1, 0, 255))

    # create the image and drawing context
    im = Image.new('RGB', (size, size), (R, G, B))
    draw = ImageDraw.Draw(im, 'RGBA')

    # now draw lines
    min_width = 0.004 * size
    max_width = 0.004 * size
    min_dist = 0.04 * size
    max_dist = 0.05 * size
    max_color_dist = 40
    min_rad = 0.04 * size
    max_rad = 0.06 * size
    margin = 0.02 * size
    for e in rest:
        if (last_x is -1):
            last_x = int(size / 2)
            last_y = int(size / 2)
        """
        w2 = int(map_number(e[4], 0, 1, min_width, max_width))
        # line width
        w = 2 * w2 + 2
        # line position
        x1 = map_number(e[0], 0, 1, w2, size-w2)
        y1 = map_number(e[1], 0, 1, w2, size-w2)
        x2 = map_number(e[2], 0, 1, w2, size-w2)
        y2 = map_number(e[3], 0, 1, w2, size-w2)

        # determine foreground color from header
        R = int(map_number(e[4], 0, 1, 0, 255))
        G = int(map_number(e[5], 0, 1, 0, 255))
        B = int(map_number(e[6], 0, 1, 0, 255))

        # draw line with round line caps (circles at the end)
        draw.line((x1, y1, x2, y2), fill=(R, G, B), width=w)
        draw.ellipse((x1-w2, y1-w2, x1+w2, y1+w2), fill=(R, G, B))
        draw.ellipse((x2-w2, y2-w2, x2+w2, y2+w2), fill=(R, G, B))
        """
        w2 = int(map_number(e[4], 0, 1, min_width, max_width))
        # line width
        w = 2 * w2 + 2
        # line position
        x1 = map_number(e[0], 0, 1, min_dist, max_dist)
        y1 = map_number(e[1], 0, 1, min_dist, max_dist)
        x2 = map_number(e[2], 0, 1, w2, size-w2)
        y2 = map_number(e[3], 0, 1, w2, size-w2)
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
        A = 0
        if (last_r is -1):
            R = int(map_number(e[4], 0, 1, 0, 255))
            G = int(map_number(e[5], 0, 1, 0, 255))
            B = int(map_number(e[6], 0, 1, 0, 255))
            A = int(map_number(e[7], 0, 1, 0, 255))
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
            A = int(clamp_range(\
                last_b + map_number(e[7], 0, 1, -max_color_dist, max_color_dist),\
                0,\
                255)\
            )
            
        last_r = R
        last_g = G
        last_b = B
        last_a = A

        density = 0.05
        points = line_normal_sampling(density, x1, y1, x2, y2, 20)
        for first, second in grouped(points, 2):
          _width=random.randint(1, 5)
          draw.line(first, fill=(R, G, B), width=_width)
          draw.line(second, fill=(R, G, B), width=_width)
        draw.ellipse((x1-w2, y1-w2, x1+w2, y1+w2), fill=(R, G, B, A))
        draw.ellipse((x2-w2, y2-w2, x2+w2, y2+w2), fill=(R, G, B, A))


    return im.resize((1200, 1200), Image.ANTIALIAS)
