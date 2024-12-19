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

    TODO:
        DONE! --implement _create_body: TRI
        NOPE! --implement _create_body: TRISHADOW
        create subclass for equilateral triangles
            implement _create_body: EQTRI
            NOPE! --implement _create_body: EQTRISHADOW
            implement easy option to make a button point north, south, east, or west
        DONE! --determine if changes need to be made to label positioning
        DONE! --hit detection
        DONE! --implement properties
        review type annotations
        check if functions or variables can be set to private with a leading _
        documentation



"""

import terminalio
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_text.bitmap_label import Label
from adafruit_button.button_base import _check_color
from adafruit_button.triangle_button_base import TriangleButtonBase

try:
    from typing import Optional, Union, Tuple, Any, List
    from fontio import FontProtocol
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Display_Button.git"

class TriangleButton(TriangleButtonBase):
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

    def __init__(
        self,
        *,
        x: int,
        y: int,
        x0: Optional[int],
        y0: Optional[int],
        x1: Optional[int],
        y1: Optional[int],
        x2: Optional[int],
        y2: Optional[int],
        name: Optional[str] = None,
        fill_color: Optional[Union[int, Tuple[int, int, int]]] = 0xFFFFFF,
        outline_color: Optional[Union[int, Tuple[int, int, int]]] = 0x0,
        label: Optional[str] = None,
        label_font: Optional[FontProtocol] = None,
        label_color: Optional[Union[int, Tuple[int, int, int]]] = 0x0,
        selected_fill: Optional[Union[int, Tuple[int, int, int]]] = None,
        selected_outline: Optional[Union[int, Tuple[int, int, int]]] = None,
        selected_label: Optional[Union[int, Tuple[int, int, int]]] = None,
        label_x_offset: Optional[int] = 0,
        label_y_offset: Optional[int] = 0,
        label_scale: Optional[int] = 1
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            name=name,
            label=label,
            fill_color=fill_color,
            outline_color=outline_color,
            label_font=label_font,
            label_color=label_color,
            selected_fill=selected_fill,
            selected_outline=selected_outline,
            selected_label=selected_label,
            label_x_offset=label_x_offset,
            label_y_offset=label_y_offset,
            label_scale=label_scale,
        )

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

class TriangleButtonBH(TriangleButtonBase):

    #Constants to hold the directions the arrow can face
    NORTH = const(0)
    EAST = const(1)
    SOUTH = const(2)
    WEST = const(3)
    
    def _calculate_points(self, base, height) -> List:
        points = []
        if self.style == TriangleButtonBH.NORTH:
            #Calculate the top vertex
            x0 = base // 2
            y0 = 0
            #Lower right vertex
            x1 = base
            y1 = height
            #Lower left vertex
            x2 = 0



    def __init__(
        self,
        *,
        x: int,
        y: int,
        base: int,
        height: int,
        direction=NORTH,
        name: Optional[str] = None,
        fill_color: Optional[Union[int, Tuple[int, int, int]]] = 0xFFFFFF,
        outline_color: Optional[Union[int, Tuple[int, int, int]]] = 0x0,
        label: Optional[str] = None,
        label_font: Optional[FontProtocol] = None,
        label_color: Optional[Union[int, Tuple[int, int, int]]] = 0x0,
        selected_fill: Optional[Union[int, Tuple[int, int, int]]] = None,
        selected_outline: Optional[Union[int, Tuple[int, int, int]]] = None,
        selected_label: Optional[Union[int, Tuple[int, int, int]]] = None,
        label_x_offset: Optional[int] = 0,
        label_y_offset: Optional[int] = 0,
        label_scale: Optional[int] = 1
    ) -> None:

        self._base = base
        self._height = height
