#!/usr/bin/python
# -*- coding:Utf-8 -*-

from PIL import Image
import operator
import unittest
import subprocess
import os
import shutil

ERROR = 0.01
MAX_ITER = 30


class Polynomial:
    def __init__(self, x, repr='roots'):
        if repr == 'coefficients':
            self.coeff = x
            self.roots = []
        elif repr == 'roots':
            self.roots = x
            self.coeff = [1.0, -1*x[0]]
            # calculate the (x-x_0)*(x-x_1)*...*(x-x_n) polynomial's coefficients
            for i in xrange(1, len(x)):
                self.convolve([1, -1*x[i]])

    def evaluate(self, x_0):
        """
        evaluate polynomial with Horner's method
        """
        val = 0
        for coefficient in self.coeff:
            val = val*x_0+coefficient
        return val

    def derive(self):
        x = self.coeff
        y = []
        for i in xrange(0, len(x)-1):
            y.append(x[i]*(len(x)-i-1))
        return y

    def convolve(self, a):
        """
        convolve self and a, where "a" is a linear polynomial's coefficients
        e.g. self = x^3+2x-1 -> [1, 0, 2, -1], a = 3x+8 -> [3, 8]
        self.colvolve(a) -> (x^3+2x-1)*(3x+8) = (3x^4+8x^3+6x^2+13x-8) ->
            self.coeff = [3, 8, 6, 13, -8]
        """
        if len(a) != 2:
            raise Exception("Wrong usage of convolve, read comment")
        x = []
        x.append(a[0]*self.coeff[0])
        for i in xrange(1, len(self.coeff)):
            x.append(a[0]*self.coeff[i]+a[1]*self.coeff[i-1])
        x.append(a[1]*self.coeff[-1])
        self.coeff = x

    def newton(self, x, maxit):
        derivative = Polynomial(self.derive(), 'coefficients')
        k = 0
        x_prev = float("infinity")
        while abs(x-x_prev) > ERROR*abs(x) and k < maxit:
            x_prev = x
            px = self.evaluate(x_prev)
            pdx = derivative.evaluate(x_prev)
            try:
                x -= px/pdx
            except ZeroDivisionError:
                x = float("infinity")
            k += +1
        # it is a root, and it is not already in the list of roots:
        try:
            root_not_found_yet = min([abs(i-x) for i in self.roots]) > ERROR
        except ValueError:
            root_not_found_yet = True
        if abs(self.evaluate(x)) < ERROR and root_not_found_yet:
            self.roots.append(x)
        return x, k

    def draw_fractal(self, x, y, width, height, file_name):
        xa = x.real
        xb = y.real
        ya = x.imag
        yb = y.imag

        image = Image.new("RGB", (width, height))

        for y in xrange(0, height):
            zy = y * (yb - ya) / (height - 1) + ya
            for x in xrange(0, width):
                zx = x * (xb - xa) / (width - 1) + xa
                z = complex(zx, zy)
                root, iter = self.newton(z, MAX_ITER)
                try:
                    min_index, min_value = min(enumerate([abs(i-root) for i in self.roots]), key=operator.itemgetter(1))
                except ValueError:
                    min_value = ERROR+1
                if min_value < ERROR:
                    image.putpixel((x, height-1-y), color(len(self.coeff)-1, min_index, iter))
                else:
                    image.putpixel((x, height-1-y), (0, 0, 0))

        try:
            image.save("images/" + file_name + '.png', "PNG")
        except IOError:
            os.mkdir('images/')

    def animate_fractal(self, xa, ya, xb, yb, width, height, n, file_name):
        try:
            os.mkdir('images/')
            os.mkdir('images/temp/')
        except OSError:
            pass
        for i in xrange(0, n):
            x1 = ya.real-xa.real
            x2 = yb.real-xb.real
            y1 = ya.imag-xa.imag
            y2 = yb.imag-xb.imag
            xd = x1*((float(x2)/x1)**(1.0/(n-1)))**i
            yd = y1*((float(y2)/y1)**(1.0/(n-1)))**i

            if x1-x2 == 0:
                x = 1-float(i)/n
                y = 1-float(i)/n
            else:
                x = float(xd-x2)/(x1-x2)
                y = float(yd-y2)/(y1-y2)

            self.draw_fractal(xa*x+xb*(1-x), ya*y+yb*(1-y), width, height, "temp/"+str(i).zfill(3))
        subprocess.call("convert -delay 10 -loop 0 images/temp/*png images/" + file_name + ".gif", shell=True)
        shutil.rmtree('images/temp/')

    def __eq__(self, a):
        return self.coeff == a.coeff


def color(n, k, iter):
    """
    Pick the k-th of n separabile color (e.g. red, green, blue in case of n=3).
    the greater the iter, the darker the color
    """
    kth_color = k*1530/n
    rgb = []
    if kth_color/255 == 0:
        rgb = [255, 0, kth_color % 255]
    elif kth_color/255 == 1:
        rgb = [255-kth_color % 255, 0, 255]
    elif kth_color/255 == 2:
        rgb = [0, kth_color % 255, 255]
    elif kth_color/255 == 3:
        rgb = [0, 255, 255-kth_color % 255]
    elif kth_color/255 == 4:
        rgb = [kth_color % 255, 255, 0]
    elif kth_color/255 == 5:
        rgb = [255, 255-kth_color % 255, 0]
    rgb[0] = int(rgb[0]-iter*rgb[0]/MAX_ITER)
    rgb[1] = int(rgb[1]-iter*rgb[1]/MAX_ITER)
    rgb[2] = int(rgb[2]-iter*rgb[2]/MAX_ITER)
    return tuple(rgb)


class UnitTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(UnitTest, self).__init__(*args, **kwargs)

    def test_convolve(self):
        # (1x + 2)(1x^2 + 2x + 3) = 1x^3 + 4x^2 + 7x + 6
        p1 = Polynomial([1, 2, 3], "coefficients")
        p1.convolve([1, 2])
        self.assertListEqual(p1.coeff, [1, 4, 7, 6])
        # (1x + 2)(1x^3 + 4x^2 + 7x + 6) = 1x^4 + 6x^3 + 15x^2 + 20x + 12
        p2 = Polynomial([1, 4, 7, 6], "coefficients")
        p2.convolve([1, 2])
        self.assertListEqual(p2.coeff, [1, 6, 15, 20, 12])

    def test_newton_method(self):
        p1 = Polynomial([2, -4], "roots")
        self.assertAlmostEqual(p1.newton(-10, MAX_ITER)[0], -4, delta=ERROR)
        p2 = Polynomial([2, 0, 10], "coefficients")
        self.assertEqual(p2.newton(0, MAX_ITER)[0], float("infinity"))

    def test_derive(self):
        p = Polynomial([2, -4, 10+3j, 0j, 0], "coefficients")
        self.assertEqual(p.derive(), Polynomial(Polynomial([8, -12, 20+6j, 0j], "coefficients")))

    def test_evaluate(self):
        p = Polynomial([2, -4, 10+3j, 0j, 0], "coefficients")
        self.assertEqual(p.derive(), Polynomial(Polynomial([8, -12, 20+6j, 0j], "coefficients")))

    def test_color(self):
        self.assertEqual(color(2, 1, 0), (0, 255, 255))
        self.assertEqual(color(2, 1, MAX_ITER/6), (0, 213, 213))
        self.assertEqual(color(2, 0, 0), (255, 0, 0))
        self.assertEqual(color(2, 0, MAX_ITER/3), (170, 0, 0))
        self.assertEqual(color(3, 0, 0), (255, 0, 0))
        self.assertEqual(color(3, 1, MAX_ITER/3), (0, 0, 170))
        self.assertEqual(color(3, 2, MAX_ITER/3*2), (0, 85, 0))
        self.assertEqual(color(3, 2, MAX_ITER), (0, 0, 0))
