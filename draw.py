__author__ = 'Alex'

from PIL import Image
import math


def get_step(_from, _to):
    if _from < _to:
        return lambda x, step_size=1: x + step_size
    return lambda x, step_size=1: x - step_size


class SImage(object):

    def __init__(self, mode, size, color, scale=1):
        self.image = Image.new(mode, size, color)
        self.size = size
        self.color = color
        self.scale = scale
        self.mode = mode
        self.pseudo_size = self.get_pseudo_size()

    def show(self):
        self.image.show()

    def get_scale(self):
        return self.scale

    def get_pseudo_size(self):
        self.pseudo_size = (int(self.size[0] / self.scale), int(self.size[1] / self.scale))
        return self.pseudo_size

    def put_pseudo_pixel(self, pseudo_cord, color, gradient=1):
        for real_x in range(int((pseudo_cord[0] - 1) * self.scale), int(pseudo_cord[0] * self.scale + 1)):
            for real_y in range(int((pseudo_cord[1] - 1) * self.scale), int(pseudo_cord[1] * self.scale + 1)):
                self.image.putpixel((real_x, real_y),
                                    (int(color[0]*gradient), int(color[1]*gradient), int(color[2]*gradient)))

    def flip_vertically(self):
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

    def br_line(self, a, b, color):
        dx = abs(b[0] - a[0])
        dy = abs(b[1] - a[1])
        x_step = get_step(a[0], b[0])
        y_step = get_step(a[1], b[1])
        pdx, pdy = 0, 0

        if dx > dy:
            pdx = x_step(0)
            es = dy
            el = dx
        else:
            pdy = y_step(0)
            es = dx
            el = dy

        current_x = a[0]
        current_y = a[1]
        err = el / 2

        self.put_pseudo_pixel((current_x, current_y), color)

        for _ in range(0, el):
            err -= es
            if err < 0:
                err += el
                current_x = x_step(current_x)
                current_y = y_step(current_y)
            else:
                current_x += pdx
                current_y += pdy
            self.put_pseudo_pixel((current_x, current_y), color)

    def br_circle(self, center, radius, color):
        x = 0
        y = radius
        delta = 1 - 2 * radius
        while y >= 0:
            self.put_pseudo_pixel((center[0] + x, center[1] + y), color)
            self.put_pseudo_pixel((center[0] + x, center[1] - y), color)
            self.put_pseudo_pixel((center[0] - x, center[1] + y), color)
            self.put_pseudo_pixel((center[0] - x, center[1] - y), color)
            error = 2 * (delta + y) - 1
            if delta < 0 and error <= 0:
                x += 1
                delta += 2 * x + 1
                continue
            error = 2 * (delta - x) - 1
            if delta > 0 and error > 0:
                y -= 1
                delta += 1 - 2 * y
                continue
            x += 1
            delta += 2 * (x - y)
            y -= 1

    def br_ellipse(self, center, width, height, color):
        h_2 = height * height
        w_2 = width * width
        prevSR = 0
        for i in range(1, int(2 * width + 1)):
            sqrRoot = math.sqrt(h_2 - (((h_2 * (width - i)) * (width - i)) / w_2))
            self.br_line((int(center[0] + i - 1 - width), int(center[1] + prevSR)),
                         (int(center[0] + i - width), int(center[1] + sqrRoot)),
                         color)
            self.br_line((int(center[0] + i - 1 - width), int(center[1] - prevSR)),
                         (int(center[0] + i - width), int(center[1] - sqrRoot)),
                         color)
            prevSR = sqrRoot


    def wu_line(self, a, b, color):
        if b[0] < a[0]:
            a_swaped = (b[0], b[1])
            b_swaped = (a[0], a[1])
        else:
            a_swaped = (a[0], a[1])
            b_swaped = (b[0], b[1])

        dx = b_swaped[0] - a_swaped[0]
        dy = b_swaped[1] - a_swaped[1]
        gradient = dy / dx

        # обработать начальную точку
        xend = round(a_swaped[0])
        yend = a_swaped[1] + gradient * (xend - a_swaped[0])
        xgap = 1 - math.modf(a_swaped[0] + 0.5)[0]
        x_a = xend  # будет использоваться в основном цикле
        y_a = int(yend)
        self.put_pseudo_pixel((x_a, y_a), color, 1 - math.modf(yend)[0] * xgap)
        self.put_pseudo_pixel((x_a, y_a + 1), color, math.modf(yend)[0] * xgap)
        intery = yend + gradient  # первое y-пересечение для цикла

        # обработать конечную точку
        xend = round(b_swaped[0])
        yend = b_swaped[1] + gradient * (xend - b_swaped[0])
        xgap = math.modf(b_swaped[0] + 0.5)[0]
        x_b = xend  # будет использоваться в основном цикле
        y_b = int(yend)
        self.put_pseudo_pixel((x_b, y_b), color, 1 - math.modf(yend)[0] * xgap)
        self.put_pseudo_pixel((x_b, y_b + 1), color, math.modf(yend)[0] * xgap)

        # основной цикл
        for x in range(x_a + 1, x_b):
            self.put_pseudo_pixel((x, int(intery)), color, 1 - math.modf(intery)[0])
            self.put_pseudo_pixel((x, int(intery) + 1), color, math.modf(intery)[0])
            intery = intery + gradient


