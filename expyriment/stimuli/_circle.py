#!/usr/bin/env python

"""
A circle stimulus.

This module contains a class implementing a circle stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import math

from . import defaults
from ._ellipse import Ellipse


class Circle(Ellipse):
    """A class implementing a basic 2D circle."""

    def __init__(self, radius, colour=None, line_width=None, position=None,
                 anti_aliasing=None):
        """Create a circle.

        Parameters
        ----------
        radius : int
            radius of the circle
        colour : (int,int,int), optional
            colour of the circle
        line_width : int, optional
            line width in pixels betwee >= 0 and < radius,
            0 will result in a filled circle
        position : (int, int), optional
            position of the stimulus
        anti_aliasing : int, optional
            anti aliasing parameter (good anti_aliasing with 10)

        """

        self._radius = radius
        if position is None:
            position = defaults.circle_position
        if colour is None:
            colour = defaults.circle_colour
        if line_width is None:
            line_width = defaults.circle_line_width
        elif line_width < 0 or line_width >= self._radius:
            raise AttributeError("line_width must be >= 0 and < radius!")
        if anti_aliasing is not None:
            self._anti_aliasing = anti_aliasing
        else:
            self._anti_aliasing = defaults.circle_anti_aliasing
        Ellipse.__init__(self, [radius, radius], colour, line_width,
                         position, anti_aliasing)

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def radius(self):
        """Getter for radius."""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter for radius."""

        if self.has_surface:
            raise AttributeError(Circle._getter_exception_message.format(
                "radius"))
        else:
            self._radius = value

    def get_polar_coordiantes(self):
        """"OBSOLETE METHOD: Please use 'polar_coordinate'."""

        raise DeprecationWarning("get_polar_coordiantes is obsolete. " +
                                 "Please use the property polar_coordinate")

    def set_polar_coordinates(self, radial, angle_in_degrees):
        """"OBSOLETE METHOD: Please use 'set_polar_coordinates'."""

        raise DeprecationWarning("set_polar_coordinates is obsolete. " +
                                 "Please use the property polar_coordinate")

    def overlapping_with_circle(self, other, minimal_gap=0):
        """Return True if touching or overlapping with another circle.

        Parameters
        ----------
        other : expyriment.stimuli.Circle object
            other circle
        minimal_gap : int, optional
            minimum gap between two circle, small gaps will be treated as
            overlapping (default=0)

        Returns
        -------
        is_inside : bool

        """

        d = self.distance(other)
        return (d - minimal_gap <= other._radius + self._radius)

    def center_inside_circle(self, other):
        """Return True if the center is inside another circle.

        Parameters
        ----------
        other : expyriment.stimuli.Circle object
            other circle

        Returns
        -------
        is_inside : bool

        """

        d = self.distance(other)
        return (d <= other._radius)

    def inside_circle(self, other):
        """Return True if the whole circle is inside another circle.

        Parameters
        ----------
        other : expyriment.stimuli.Circle object
            other circle

        Returns
        -------
        is_inside : bool

        """

        d = self.distance(other)
        return (d <= other._radius - self._radius)

if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    dot = Circle(radius=100, anti_aliasing=10)
    dot.present()
    exp.clock.wait(1000)
