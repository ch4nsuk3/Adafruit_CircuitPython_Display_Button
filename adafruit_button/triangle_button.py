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

    def _empty_self_group(self) -> None:
        while len(self) > 0:
            self.pop()

    def _create_body(self) -> None:
        if (self._outline_color is not None) or (self._fill_color is not None):
            self.body = Triangle(
                self._x0,
                self._y0,
                self._x1,
                self._y1,
                self._x2,
                self._y2,
                fill=self._fill_color,
                outline=self._outline_color
            )

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
            label_font=label_font,
            label_color=label_color,
            selected_label=selected_label,
            label_x_offset=label_x_offset,
            label_y_offset=label_y_offset,
            label_scale=label_scale,
        )

        self.body = self.fill = self.shadow = None

        self._fill_color = _check_color(fill_color)
        self._outline_color = _check_color(outline_color)

        # Selecting inverts the button colors!
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

    @property
    def fill_color(self) -> Optional[int]:
        return self._fill_color

    @fill_color.setter
    def fill_color(self, new_color: Union[int, Tuple[int, int, int]]) -> None:
        self._fill_color = _check_color(new_color)
        if not self.selected:
            self.body.fill = self._fill_color

    @property
    def outline_color(self) -> Optional[int]:
        return self._outline_color

    @outline_color.setter
    def outline_color(self, new_color: Union[int, Tuple[int, int, int]]) -> None:
        self._outline_color = _check_color(new_color)
        if not self.selected:
            self.body.outline = self._outline_color

    @property
    def selected_fill(self) -> Optional[int]:
        return self._selected_fill

    @selected_fill.setter
    def selected_fill(self, new_color: Union[int, Tuple[int, int, int]]) -> None:
        self._selected_fill = _check_color(new_color)
        if self.selected:
            self.body.fill = self._selected_fill

    @property
    def selected_outline(self) -> Optional[int]:
        return self._selected_outline

    @selected_outline.setter
    def selected_outline(self, new_color: Union[int, Tuple[int, int, int]]) -> None:
        self._selected_outline = _check_color(new_color)
        if self.selected:
            self.body.outline = self._selected_outline