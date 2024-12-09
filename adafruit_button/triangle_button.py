# SPDX-FileCopyrightText: 2024 Channing Ramos
#
# SPDX-License-Identifier: MIT

"""
`adafruit_button.triangle_button`
================================================================================

Triangular UI Buttons for displayio


* Author(s): Channing Ramos

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

from micropython import const
from adafruit_display_shapes.triangle import Triangle
from adafruit_button.button_base import ButtonBase, _check_color

try:
    from typing import Optional, Union, Tuple, Any, List
    from fontio import FontProtocol
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Display_Button.git"


class TriangleButton(ButtonBase):
    # pylint: disable=too-many-instance-attributes, too-many-locals
    """Helper class for creating UI buttons for ``displayio``. Provides the following
    buttons:

    :param int x: The x position of the button.
    :param int y: The y position of the button.
    :param int x0: The width of the button in pixels.
    :param int y0: The height of the button in pixels.
    :param int x1: The height of the button in pixels.
    :param int y1: The height of the button in pixels.
    :param int x2: The height of the button in pixels.
    :param int y2: The height of the button in pixels.
    :param Optional[str] name: The name of the button.
    :param Optional[Union[int, Tuple[int, int, int]]] fill_color: The color to fill the button.
     Accepts an int or a tuple of 3 integers representing RGB values. Defaults to 0xFFFFFF.
    :param Optional[Union[int, Tuple[int, int, int]]] outline_color: The color of the outline of
     the button. Accepts an int or a tuple of 3 integers representing RGB values. Defaults to 0x0.
    :param Optional[str] label: The text that appears inside the button.
    :param Optional[FontProtocol] label_font: The button label font. Defaults to
     ''terminalio.FONT''
    :param Optional[Union[int, Tuple[int, int, int]]] label_color: The color of the button label
     text. Accepts an int or a tuple of 3 integers representing RGB values. Defaults to 0x0.
    :param Optional[Union[int, Tuple[int, int, int]]] selected_fill: The fill color when the
     button is selected. Accepts an int or a tuple of 3 integers representing RGB values.
     Defaults to the inverse of the fill_color.
    :param Optional[Union[int, Tuple[int, int, int]]] selected_outline: The outline color when the
     button is selected. Accepts an int or a tuple of 3 integers representing RGB values.
     Defaults to the inverse of outline_color.
    :param Optional[Union[int, Tuple[int, int, int]]] selected_label: The label color when the
     button is selected. Accepts an int or a tuple of 3 integers representing RGB values.
     Defaults to inverting the label_color.
    :param Optional[int] label_scale: The scale factor used for the label. Defaults to 1.
    """

    def _empty_self_group(self) -> None:
        while len(self) > 0:
            self.pop()

    def _create_body(self) -> None:
        if (self.outline_color is not None) or (self.fill_color is not None):
            if self.style == TriangleButton.TRI:
                self.body = Triangle(
                    self.x0,
                    self.y0,
                    self.x1,
                    self.y1,
                    self.x2,
                    self.y2,
                    fill=self.fill_color,
                    outline=self.outline_color
                )

    TRI = const(0)
    SHADOWTRI = const(1)

    def __init__(
        self,
        x,
        y,
        x0,
        y0,
        x1,
        y1,
        x2,
        y2,
        name,
        style,
        fill_color,
        outline_color,
        label,
        label_font,
        label_color,
        selected_fill,
        selected_outline,
        selected_label,
        label_scale):

        #Find the height and width based off the provided points.
        #The Triangle class in adafruit_display_shapes has no height/width attributes
        width = max[x0, x1, x2] - min[x0, x1, x2]
        height = max[y0, y1, y2] - min[y0, y1, y2]

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            name=name,
            label=label,
            label_font=label_font,
            label_color=label_color,
            selected_label=selected_label,
            label_scale=label_scale,
        )

        self.body = self.fill = self.shadow = None
        self.style = style

        self._fill_color = _check_color(fill_color)
        self._outline_color = _check_color(outline_color)

        self._selected_fill = _check_color(selected_fill)
        self._selected_outline = _check_color(selected_outline)

        if self.selected_fill is None and fill_color is not None:
            self.selected_fill = (~_check_color(self._fill_color)) & 0xFFFFFF
        if self.selected_outline is None and outline_color is not None:
            self.selected_outline = (~_check_color(self._outline_color)) & 0xFFFFFF

        self._create_body()
        if self.body:
            self.append(self.body)

        self.label = label

    def _subclass_selected_behavior(self, value):
        if self._selected:
            new_fill = self.selected_fill
            new_out = self.selected_outline
        else:
            new_fill = self._fill_color
            new_out = self._outline_color
        #Update and apply colors
        if self.body is not None:
            self.body.fill = new_fill
            self.body.outline = new_out
