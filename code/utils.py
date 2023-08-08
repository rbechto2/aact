import pygame
import math


def drawRegularPolygon(surf, color, x, y, radius):
    pts = []
    for i in range(6):
        x = x + radius * math.cos(math.pi/2 + math.pi * 2 * i / 6)
        y = y + radius * math.sin(math.pi/2 + math.pi * 2 * i / 6)
        pts.append([int(x), int(y)])
    pygame.draw.polygon(surf, color, pts)
