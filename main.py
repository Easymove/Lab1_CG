__author__ = 'Alex'

from draw import SImage
import random


def test():
    img = SImage("RGB", (1600, 900), "black", 3)
    img.br_line((50, 5), (50, 50), (0, 255, 0))
    img.br_circle((100, 100), 25, (255, 0, 0))
    img.wu_line((180, 50), (50, 150), (0, 0, 255))
    img.br_ellipse((220, 220), 40, 70, (150, 150, 50))
    img.show()


def signature_br():
    img = SImage("RGB", (1600, 900), "black", 7)
    color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    color2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    color3 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #Е
    img.br_line((5, 5), (5, 85), color1)
    img.br_line((5, 5), (40, 5), color1)
    img.br_line((5, 45), (40, 45), color1)
    img.br_line((5, 85), (40, 85), color1)
    #А
    img.br_line((85, 85), (65, 5), color2)
    img.br_line((85, 85), (105, 5), color2)
    img.br_line((75, 40), (95, 40), color2)
    #Г
    img.br_line((120, 85), (121, 5), color3)
    img.br_line((120, 85), (160, 85), color3)
    img.flip_vertically()
    img.show()


test()
signature_br()
