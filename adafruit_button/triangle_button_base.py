# SPDX-FileCopyrightText: 2024 Channing Ramos
#
# SPDX-License-Identifier: MIT

"""
`adafruit_button.triangle_button`
================================================================================

Base Class for Triangular UI Buttons for displayio


* Author(s): Channing Ramos

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

    TODO:
        DONE! --Rebase to a base button class
        DONE! --determine if changes need to be made to label positioning
        DONE! --hit detection
        DONE! --implement properties
        review type annotations
        check if functions or variables can be set to private with a leading _
        documentation



"""

import terminalio
from adafruit_display_text.bitmap_label import Label
from adafruit_button.button_base import _check_color
from displayio import Group

try:
    from typing import Optional, Union, Tuple, Any, List
    from fontio import FontProtocol
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Display_Button.git"

def _calc_area(x0: int, y0: int, x1: int, y1: int, x2: int, y2: int):
    area = abs((x0 * (y1 - y2) + x1 * (y2 - y0) + x2 * (y0 - y1)) / 2.0)
    return area

class TriangleButtonBase(Group):
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
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        name: Optional[str] = None,
        label: Optional[str] = None,
        label_font: Optional[FontProtocol] = None,
        label_color: Optional[Union[int, Tuple[int, int, int]]] = 0x0,
        selected_label: Optional[Union[int, Tuple[int, int, int]]] = None,
        label_x_offset: Optional[int] = 0,
        label_y_offset: Optional[int] = 0,
        label_scale: Optional[int] = 1
    ) -> None:

        super().__init__(x=x, y=y)

        #Find the height and width based off the provided points.
        #The Triangle class in adafruit_display_shapes has no height/width attributes
        self._width = max(x0, x1, x2) - min(x0, x1, x2)
        self._height = max(y0, y1, y2) - min(y0, y1, y2)

        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        self._selected = False
        self.label_x_offset = label_x_offset
        self.label_y_offset = label_y_offset
        self._name = name
        self._label = label
        self._label_font = label_font
        self._label_color = _check_color(label_color)
        self._selected_label = _check_color(selected_label)
        self._label_scale = label_scale


    def _subclass_selected_behavior(self, value):
        pass

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        if value == self._selected:
            return
        self._selected = value

        if self._selected:
            new_label = self.selected_label
        else:
            new_label = self._label_color
        if self._label is not None:
            self._label.color = new_label

        self._subclass_selected_behavior(value)

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
        #If offsets were provided this is where they get applied.
        x_point = ((self._x0 + self._x1 + self._x2) // 3) + self.label_x_offset
        y_point = ((self._y0 + self._y1 + self._y2) // 3) + self.label_y_offset
        self._label.anchored_position = (x_point, y_point)

        self._label.color = self._label_color if not self.selected else self._selected_label
        self.append(self._label)

        if (self.selected_label is None) and (self._label_color is not None):
            self.selected_label = (~_check_color(self._label_color)) & 0xFFFFFF

    @property
    def selected_label(self) -> int:
        return self._selected_label

    @selected_label.setter
    def selected_label(self, new_color: Union[int, Tuple[int, int, int]]) -> None:
        self._selected_label = _check_color(new_color)

    @property
    def label_color(self) -> int:
        return self._label_color

    @label_color.setter
    def label_color(self, new_color: Union[int, Tuple[int, int, int]]):
        self._label_color = _check_color(new_color)
        self._label.color = self._label_color

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def points(self) -> List[int, int, int, int, int, int]:
        return [self._x0, self._y0, self._x1, self._y1, self._x2, self._y2]

    def contains(self, point: Union[Tuple[int, int], List[int], List[Dict[str, int]]]) -> bool:

        if isinstance(point, tuple) or (isinstance(point, list) and isinstance(point[0], int)):
            point_x = point[0]
            point_y = point[1]

            area = _calc_area(self._x0, self._y0, self._x1, self._y1, self._x2, self._y2)
            area_pbc = _calc_area(point_x, point_y, self._x1, self._y1, self._x2, self._y2)
            area_apc = _calc_area(self._x0, self._y0, point_x, point_y, self._x2, self._y2)
            area_abp = _calc_area(self._x0, self._y0, self._x1, self._y1, point_x, point_y)

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

                    area = _calc_area(self._x0, self._y0, self._x1, self._y1, self._x2, self._y2)
                    area_pbc = _calc_area(point_x, point_y, self._x1, self._y1, self._x2, self._y2)
                    area_apc = _calc_area(self._x0, self._y0, point_x, point_y, self._x2, self._y2)
                    area_abp = _calc_area(self._x0, self._y0, self._x1, self._y1, point_x, point_y)

                    if area == area_pbc + area_apc + area_abp:
                        return True

        return False