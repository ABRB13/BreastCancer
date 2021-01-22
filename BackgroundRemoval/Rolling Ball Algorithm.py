import math
import numpy
def rolling_ball_background(array, radius, light_background=True, smoothing=True):
    ball = RollingBall(radius)
    float_array = array
    float_array = rolling_ball_float_background(float_array, radius, invert, smoothing, ball)
    background_pixels = float_array.flatten()
    pixels = numpy.int8(array.flatten())
    for p in range(len(pixels)):
        value = (pixels[p] & 0xff) - (background_pixels[p] + 255) + offset
        if value < 0:
            value = 0
        if value > 255:
            value = 255
        pixels[p] = numpy.int8(value)
    return numpy.reshape(pixels, array.shape)
def roll_ball(ball, array):
    height, width = array.shape
    pixels = numpy.float32(array.flatten())
    z_ball = ball.data
    ball_width = ball.width
    radius = ball_width / 2
    cache = numpy.zeros(width * ball_width)
    for y in range(-radius, height + radius):
        next_line_to_write_in_cache = (y + radius) % ball_width
        next_line_to_read = y + radius
        if next_line_to_read < height:
            src = next_line_to_read * width
            dest = next_line_to_write_in_cache * width
            cache[dest:dest + width] = pixels[src:src + width]
            p = next_line_to_read * width
            for x in range(width):
                pixels[p] =- float('inf')
                p += 1
        y_0 = y - radius
        if y_0 < 0:
            y_0 = 0
        y_ball_0 = y_0 - y + radius
        y_end = y + radius
        if y_end >= height:
            y_end = height - 1
        for x in range(-radius, width + radius):
            z = float('inf')
            x_0 = x - radius
            if x_0 < 0:
                x_0 = 0
            x_ball_0 = x_0 - x + radius
            x_end = x + radius
            if x_end >= width:
                x_end = width - 1
            y_ball = y_ball_0
            for yp in range(y_0, y_end + 1):
                cache_pointer = (yp % ball_width) * width + x_0
                bp = x_ball_0 + y_ball * ball_width
                for xp in range(x_0, x_end + 1):
                    z_reduced = cache[cache_pointer] - z_ball[bp]
                    if z > z_reduced:
                        z = z_reduced
                    cache_pointer += 1
                    bp += 1
                y_ball += 1
            y_ball = y_ball_0
            for yp in range(y_0, y_end + 1):
                p = x_0 + yp * width
                bp = x_ball_0 + y_ball * ball_width
                for xp in range(x_0, x_end + 1):
                    z_min = z + z_ball[bp]
                    if pixels[p] < z_min:
                        pixels[p] = z_min
                    p += 1
                    bp += 1
                y_ball += 1
    return numpy.reshape(pixels, array.shape)
class RollingBall(object):
    def __init__(self, radius):
        if radius <= 10:
            self.shrink_factor = 1
            arc_trim_per = 24
        self.build(radius, arc_trim_per)
    def build(self, ball_radius, arc_trim_per):
        small_ball_radius = ball_radius / self.shrink_factor
        if small_ball_radius < 1:
            small_ball_radius = 1
        rsquare = small_ball_radius * small_ball_radius
        xtrim = int(arc_trim_per * small_ball_radius) / 100
        half_width = int(round(small_ball_radius - xtrim))
        self.width = (2 * half_width) + 1
        self.data = [0.0] * (self.width * self.width)
        p = 0
        for y in range(self.width):
            for x in range(self.width):
                xval = x - half_width
                yval = y - half_width
                temp = rsquare - (xval * xval) - (yval * yval)

                if temp > 0:
                    self.data[p] = float(math.sqrt(temp))
                p += 1