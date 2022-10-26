import itertools
import random
from PIL import Image, ImageDraw
from matrix import Matrix
import time
import sys
import numpy as np
from typing import List

class Gradient:
    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = cols
        self.gradient_root = [0, 0]
  #   sns.color_palette("magma", as_cmap=True)
        pass

    def gradient_looping(self):
        # end
        print('hi')


# def hex_to_RGB(hex):
#     ''' "#FFFFFF" -> [255,255,255] '''
#     # Pass 16 to the integer function for change of base
#     return [int(hex[i:i+2], 16) for i in range(1, 6, 2)]


# def RGB_to_hex(RGB):
#     ''' [255,255,255] -> "#FFFFFF" '''
#     # Components need to be integers for hex to make sense
#     RGB = [int(x) for x in RGB]
#     return "#"+"".join(["0{0:x}".format(v) if v < 16 else
#                         "{0:x}".format(v) for v in RGB])


def linear_gradient(start_color: tuple[int, int, int], end_color: tuple[int, int, int], stops: int = 64) -> List[tuple[int,int,int]]:
    ''' returns a gradient list of (n) colors between
                    two hex colors. start_hex and finish_hex
                    should be the full six-digit color string,
                    inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    #  s = hex_to_RGB(start_color)
    #  f = hex_to_RGB(end_color)
    # Initilize a list of the output colors with the starting color
    color_list = [start_color]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for i in range(1, stops):
        # Interpolate RGB vector for color at the current value of t
        color_i = tuple(
            int(start_color[j] + (float(i)/(stops-1))
                * (end_color[j]-start_color[j]))
            for j in range(3)
        )
        # Add it to our list of output colors
        color_list.append(color_i)

    return color_list

def polylinear_gradient(colors: List[tuple[int, int, int]], stops: int = 64):
    ''' returns a list of colors forming linear gradients between
        all sequential pairs of colors. "n" specifies the total
        number of desired output colors '''
    # The number of colors per individual linear gradient
    color_stops = int(float(stops) / (len(colors) - 1))
    # returns dictionary defined by color_dict()
    gradient_dict = linear_gradient(colors[0], colors[1], color_stops)

    if len(colors) > 1:
        for col in range(1, len(colors) - 1):
            next = linear_gradient(colors[col], colors[col+1], color_stops)
            for k in range(3):
                # Exclude first point to avoid duplicates
                gradient_dict[col] = next[col]

    return gradient_dict


def scrolling_linear_gradient(m: Matrix):
    half_gradient = linear_gradient((255, 100, 255), (50, 50, 250), stops=32)
    reverse_gradient = half_gradient.copy()
    reverse_gradient.reverse()
    gradient = half_gradient + reverse_gradient

    for offset in itertools.cycle(range(64)):
        imarray = np.empty([64, 64, 3], dtype=np.uint8)
        for i, color in enumerate(gradient):
            imarray[:, (i+offset) % 64] = list(color)
            # imarray[:, (63-offset)] = list(color)
        grim = Image.fromarray(imarray, mode='RGB')
        m.matrix.SetImage(grim)
        time.sleep(.05)

def scrolling_polylinear_gradient(m: Matrix):
    half_gradient = polylinear_gradient([(255, 100, 255), (50, 50, 250), (255, 0, 0)], stops=32)
    reverse_gradient = half_gradient.copy()
    reverse_gradient.reverse()
    gradient = half_gradient + reverse_gradient

    for offset in itertools.cycle(range(64)):
        imarray = np.empty([64, 64, 3], dtype=np.uint8)
        for i, color in enumerate(gradient):
            imarray[:, (i+offset) % 64] = list(color)
            # imarray[:, (63-offset)] = list(color)
        grim = Image.fromarray(imarray, mode='RGB')
        m.matrix.SetImage(grim)
        time.sleep(.05)

def infinite_random_gradient(m: Matrix):
    random.seed()
    color1 = (random.randrange(255), random.randrange(255), random.randrange(255))
    color2 = (random.randrange(255), random.randrange(255), random.randrange(255))
    while True:
        color3 = (random.randrange(255), random.randrange(255), random.randrange(255))
        gradient1 = [list(c) for c in linear_gradient(color1, color2)]
        # print("gradient1:", gradient1)
        gradient2 = [list(c) for c in linear_gradient(color2, color3)]
        # print("gradient2:", gradient2)
        for offset in itertools.cycle(range(len(gradient1))):
            imarray = np.empty([64, 64, 3], dtype=np.uint8)
            imarray[:, 0:offset] = gradient2[len(gradient2)-offset:len(gradient2)]
            imarray[:, offset:(len(imarray[0]))] = gradient1[0:len(gradient1)-offset]
            grim = Image.fromarray(imarray, mode='RGB')
            m.matrix.SetImage(grim)
            time.sleep(.05)
        color1 = color2
        color2 = color3

m = Matrix(brightness=60)
# scrolling_linear_gradient(m)
infinite_random_gradient(m)
