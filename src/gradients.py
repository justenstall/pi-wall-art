import itertools
import random
from PIL import Image
from matrix import Matrix
import time
import sys
import numpy as np
from typing import List

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
        color_i = tuple(int(start_color[j] + (float(i)/float(stops-1)) * (end_color[j]-start_color[j])) for j in range(3))
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

def infinite_random_gradient(m: Matrix):
    '''
        Gradient scrolling

        color1 --> color2 --> color3

        gradient1 [ color1 --> color2 ] --> gradient2 [ color2 --> color3 ]
    '''
    random.seed()
    color1 = random_color()
    color2 = random_color()
    color3 = random_color()
    gradient1 = [list(c) for c in linear_gradient(color1, color2)]
    gradient2 = [list(c) for c in linear_gradient(color2, color3)]
    while True:
        # print("gradient1:", gradient1)
        imarray = np.empty([64, 64, 3], dtype=np.uint8)
        for offset in range(64):
            for i in range(0, offset):
                imarray[i, :] = gradient1[(64-offset)+i]
            for i in range(offset, 64):
                imarray[i, :] = gradient2[i-offset]
            grim = Image.fromarray(imarray, mode='RGB')
            m.matrix.SetImage(grim)
            time.sleep(.005)
        color3 = color2
        color2 = color1
        color1 = random_color()
        gradient2 = gradient1
        gradient1 = [list(c) for c in linear_gradient(color1, color2)]

def infinite_random_size_gradient(m: Matrix):
    def rand_gradient_length():
        return random.randrange(10, 200)
    '''
        Gradient scrolling

        color1 --> color2 --> color3

        gradient1 [ color1 --> color2 ] --> gradient2 [ color2 --> color3 ]
    '''
    color1 = random_color()
    color2 = random_color()
    color3 = random_color()
    length1 = rand_gradient_length()
    length2 = rand_gradient_length()
    gradient1 = [list(c) for c in linear_gradient(color1, color2, stops=length1)]
    gradient2 = [list(c) for c in linear_gradient(color2, color3, stops=length2)]
    while True:
        # Make RGB Matrix-sized array 
        imarray = np.empty([length1+length2, 64, 3], dtype=np.uint8)

        # Loop through the length of both gradients to transition to the next gradient
        for offset in range(length1+length2):
            for i in range(0, min(offset, 64)):
                imarray[i, :] = gradient1[(len(gradient1)-offset)+i]
            for i in range(offset, 64):
                imarray[i, :] = gradient2[i-offset]
            grim = Image.fromarray(imarray, mode='RGB')
            m.matrix.SetImage(grim)
            time.sleep(.01)

        # Iterate colors and create the next color
        color3 = color2
        color2 = color1
        color1 = random_color()

        # Set random length for next gradient
        length2 = length1
        length1 = rand_gradient_length()

        # Create next gradient
        gradient2 = gradient1
        gradient1 = [list(c) for c in linear_gradient(color1, color2, stops=length1)]

from gpiozero import MCP3008

def gradient_speed_control(m: Matrix):
    '''
        Gradient scrolling

        color1 --> color2 --> color3

        gradient1 [ color1 --> color2 ] --> gradient2 [ color2 --> color3 ]
    '''
    random.seed()
    pot = MCP3008(7)
    color1 = random_color()
    color2 = random_color()
    color3 = random_color()
    gradient1 = [list(c) for c in linear_gradient(color1, color2)]
    gradient2 = [list(c) for c in linear_gradient(color2, color3)]
    while True:
        print(pot.value)
        # print("gradient1:", gradient1)
        imarray = np.empty([64, 64, 3], dtype=np.uint8)
        for offset in range(64):
            for i in range(0, offset):
                imarray[i, :] = gradient1[(64-offset)+i]
            for i in range(offset, 64):
                imarray[i, :] = gradient2[i-offset]
            grim = Image.fromarray(imarray, mode='RGB')
            m.matrix.SetImage(grim)
            time.sleep(.005)
        color3 = color2
        color2 = color1
        color1 = random_color()
        gradient2 = gradient1
        gradient1 = [list(c) for c in linear_gradient(color1, color2)]

def random_color():
    return (random.randrange(255), random.randrange(255), random.randrange(255))


