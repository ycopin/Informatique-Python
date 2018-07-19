#!/usr/bin/env python3

"""
Source: http://en.wikipedia.org/wiki/Hilbert_curve#Implementation
"""

from turtle import left, right, forward, exitonclick

size = 10


def hilbert(level, angle):
    if level == 0:
        return

    right(angle)
    hilbert(level - 1, -angle)
    forward(size)
    left(angle)
    hilbert(level - 1, angle)
    forward(size)
    hilbert(level - 1, angle)
    left(angle)
    forward(size)
    hilbert(level - 1, -angle)
    right(angle)

hilbert(4, 90)
exitonclick()
