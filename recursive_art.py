""" TODO: Put your header comment here """

import random
from math import pi, sin, cos
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

        Returns a nested list representation of a nested function call by using
        recursion and a pseudo-random number generator to pick the function.
    """
    depth = random.randint(min_depth, max_depth)
    return _build_random_function(depth)

def _build_random_function(depth):
    """ A helper function for build_random_function above. Uses a pseudo-random number
        to pick which function comprehension to add to the nested list.

        Functions to choose from:
        prod(a, b) = ab
        avg(a,b) = 0.5*(a+b)
        cos_pi(a) = cos(pi*a)
        sin_pi(a) = sin(pi*a)
        mod_sum(a, b) = -1 + (a + b) % 2 -- sums A and B % 2, places in range [-1, 1]
        quot(a, b) = a/b -- divides A by B
    """
    # End case: picks either x or y to return if depth == 1
    if depth == 1:
        c = random.choice([0, 1])
        if c == 0:
            return ["x"]
        else:
            return ["y"]
    else:
    #otherwise pick another function to add into the nested list
        psrn = random.randrange(6)
        if psrn == 0:
            return ["prod", _build_random_function(depth-1), _build_random_function(depth-1)]
        elif psrn == 1:
            return ["avg", _build_random_function(depth-1), _build_random_function(depth-1)]
        elif psrn == 2:
            return ["cos_pi", _build_random_function(depth-1)]
        elif psrn == 3:
            return ["sin_pi", _build_random_function(depth-1)]
        elif psrn == 4:
            return ["sum", _build_random_function(depth-1), _build_random_function(depth-1)]
        else: #psrn == 5
            return ["pow", _build_random_function(depth-1), _build_random_function(depth-1)]


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["prod",["x"],["y"]],0.5,0.1)
        0.05
        >>> evaluate_random_function(["avg",["x"],["y"]],0.6,0.4)
        0.5
        >>> evaluate_random_function(["sin_pi",["x"]],0.5,0.1)
        1.0

        ***Rounding errors make this not work
         > evaluate_random_function(["cos_pi",["x"]],0.5,0.1)
        0.0

        This next one is weird. It takes the absolute value of the sum and
        centers it around zero.

        >>> evaluate_random_function(["sum",["x"],["y"]],0.5,0.5)
        0.0

        This one also centers around zero, which is odd but it works
        >>> evaluate_random_function(["pow",["x"],["y"]],1,0.5)
        0.0
    """
    if f[0] == "prod":
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    if f[0] == "avg":
        return 0.5 * (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))
    if f[0] == "cos_pi":
        return cos(pi * evaluate_random_function(f[1], x, y))
    if f[0] == "sin_pi":
        return sin(pi * evaluate_random_function(f[1], x, y))
    if f[0] == "sum":
        return -1 + abs(evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))
    if f[0] == "pow": #should be in the right range.
        return abs(evaluate_random_function(f[1], x, y)) ** abs(evaluate_random_function(f[2], x, y)) - 1
    if f[0] == "x":
        return x
    if f[0] == "y":
        return y

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # multiply value relative to interval by scaling factor, add to output interval start.
    factor = (output_interval_end - output_interval_start) * 1.0 /(input_interval_end-input_interval_start)
    return output_interval_start + (val - input_interval_start) * factor


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("test1.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
