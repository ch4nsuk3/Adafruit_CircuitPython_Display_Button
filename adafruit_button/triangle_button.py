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
        determine if changes need to be made to label positioning
        DONE! --hit detection
        DONE! --implement properties
        review type annotations
        documentation



"""

import terminalio
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_text.bitmap_label import Label
from adafruit_button.button_base import ButtonBase, _check_color

try:
    from typing import Optional, Union, Tuple, Any, List
    from displayio import Group
    from fontio import FontProtocol
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Display_Button.git"

def _calc_area(x0: int, y0: int, x1: int, y1: int, x2: int, y2: int):
    area = abs((x0 * (y1 - y2) + x1 * (y2 - y0) + x2 * (y0 - y1)) / 2.0)
    return area

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
        if (self._outline_color is not None) or (self._fill_color is not None):
            self.body = Triangle(
                self.x0,
                self.y0,
                self.x1,
                self.y1,
                self.x2,
                self.y2,
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
        label_x_offset: Optional[int] = None,
        label_y_offset: Optional[int] = None,
        label_scale: Optional[int] = 1
    ) -> None:

        #Find the height and width based off the provided points.
        #The Triangle class in adafruit_display_shapes has no height/width attributes
        self.width = max(x0, x1, x2) - min(x0, x1, x2)
        self.height = max(y0, y1, y2) - min(y0, y1, y2)

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        super().__init__(
            x=x,
            y=y,
            width=self.width,
            height=self.height,
            name=name,
            label=label,
            label_font=label_font,
            label_color=label_color,
            selected_label=selected_label,
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

    @property
    def label(self) -> Optional[str]:
        return getattr(self._label, "text", None)

    @label.setter
    def label(self, newtext: str) -> None:
        if self._label and self and (self[-1] == self._label):
            self.pop()

        self._label = None
        if not newtext or (self._label_color is None):
            return

        if not self._label_font:
            self._label_font = terminalio.FONT
        self._label = Label(self._label_font, text=newtext, scale=self._label_scale, anchor_point=(0.5, 0.5))

        #Calculate the centroid of the triangle, then stick the label there.
        self._label.x = (self.x0 + self.x1 + self.x2) // 3
        self._label.y = (self.y0 + self.y1 + self.y2) // 3
        self._label.color = self._label_color if not self.selected else self._selected_label
        self.append(self._label)

        if (self.selected_label is None) and (self._label_color is not None):
            self.selected_label = (~_check_color(self._label_color)) & 0xFFFFFF

    def contains(self, point: Union[Tuple[int, int], List[int], List[Dict[str, int]]]) -> bool:

        if isinstance(point, tuple) or (isinstance(point, list) and isinstance(point[0], int)):
            point_x = point[0]
            point_y = point[1]

            area = _calc_area(self.x0, self.y0, self.x1, self.y1, self.x2, self.y2)
            area_pbc = _calc_area(point_x, point_y, self.x1, self.y1, self.x2, self.y2)
            area_apc = _calc_area(self.x0, self.y0, point_x, point_y, self.x2, self.y2)
            area_abp = _calc_area(self.x0, self.y0, self.x1, self.y1, point_x, point_y)

            if area == area_pbc + area_apc + area_abp:
                return True

        elif isinstance(point, list):
            touch_points = point
            if len(touch_points) == 0:
                return False
            for touch_point in touch_points:
                if (
                    isinstance(touch_point, dict)
                    and "x" in touch_point.keys()
                    and "y" in touch_point.keys()
                ):
                    point_x = touch_point["x"]
                    point_y = touch_point["y"]

                    area = _calc_area(self.x0, self.y0, self.x1, self.y1, self.x2, self.y2)
                    area_pbc = _calc_area(point_x, point_y, self.x1, self.y1, self.x2, self.y2)
                    area_apc = _calc_area(self.x0, self.y0, point_x, point_y, self.x2, self.y2)
                    area_abp = _calc_area(self.x0, self.y0, self.x1, self.y1, point_x, point_y)

                    if area == area_pbc + area_apc + area_abp:
                        return True

        return False
