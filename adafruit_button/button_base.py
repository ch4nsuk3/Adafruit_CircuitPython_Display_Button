# SPDX-FileCopyrightText: 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_button.button`
================================================================================

UI Buttons for displayio


* Author(s): Limor Fried

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""
from adafruit_display_text.bitmap_label import Label
from displayio import Group
import terminalio
try:
    from typing import Optional, Union, List, Tuple, Any
    from fontio import FontProtocol
except ImportError:
    pass


def _check_color(color: Optional[Union[int, tuple[int, int, int]]]) -> Optional[int]:
    # if a tuple is supplied, convert it to a RGB number
    if isinstance(color, tuple):
        r, g, b = color
        return int((r << 16) + (g << 8) + (b & 0xFF))
    return color


class ButtonBase(Group):
    # pylint: disable=too-many-instance-attributes
    """Superclass for creating UI buttons for ``displayio``.

    :param int x: The x position of the button.
    :param int y: The y position of the button.
    :param int width: The width of the button in tiles.
    :param int height: The height of the button in tiles.
    :param str name: A name, or miscellaneous string that is stored on the button.
    :param str label: The text that appears inside the button. Defaults to not displaying the label.
    :param FontProtocol label_font: The button label font.
    :param int label_color: The color of the button label text. Defaults to 0x0.
    :param selected_label: The color of button label text when the button is selected.
    """

    def __init__(
        self,
        *,
        x: int,
        y: int,
        width: int,
        height: int,
        name: Optional[str] = None,
        label: Optional[str] = None,
        label_font: Optional[FontProtocol] = None,
        label_color: Optional[int] = 0x0,
        selected_label: Optional[Union[int, tuple[int, int, int]]] = None,
        label_scale: Optional[int] = 1,
    ) -> None:
        super().__init__(x=x, y=y)
        self.x = x
        self.y = y
        self._width = width
        self._height = height
        self._font = label_font
        self._selected = False
        self.name = name
        self._label = label
        self._label_color = label_color
        self._label_font = label_font
        self._selected_label = _check_color(selected_label)
        self._label_scale = label_scale

    @property
    def label(self) -> Optional[Tuple[str, str]]:
        """The text label of the button"""
        return getattr(self._label, "text", None)

    @label.setter
    def label(self, newtext: str) -> None:
        if self._label and self and (self[-1] == self._label):
            self.pop()

        self._label = None
        if not newtext or (self._label_color is None):  # no new text
            return  # nothing to do!

        if not self._label_font:
            self._label_font = terminalio.FONT
        self._label = Label(self._label_font, text=newtext, scale=self._label_scale)
        dims = list(self._label.bounding_box)
        dims[2] *= self._label.scale
        dims[3] *= self._label.scale
        if dims[2] >= self.width or dims[3] >= self.height:
            while len(self._label.text) > 1 and (
                dims[2] >= self.width or dims[3] >= self.height
            ):
                self._label.text = "{}.".format(self._label.text[:-2])
                dims = list(self._label.bounding_box)
                dims[2] *= self._label.scale
                dims[3] *= self._label.scale
            if len(self._label.text) <= 1:
                raise RuntimeError("Button not large enough for label")
        self._label.x = (self.width - dims[2]) // 2
        self._label.y = self.height // 2
        self._label.color = (
            self._label_color if not self.selected else self._selected_label
        )
        self.append(self._label)

        if (self.selected_label is None) and (self._label_color is not None):
            self.selected_label = (~self._label_color) & 0xFFFFFF

    def _subclass_selected_behavior(self, value: Optional[Any]) -> None:
        # Subclasses should override this!
        pass

    @property
    def selected(self) -> bool:
        """Selected inverts the colors."""
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        if value == self._selected:
            return  # bail now, nothing more to do
        self._selected = value

        if self._selected:
            new_label = self.selected_label
        else:
            new_label = self._label_color
        if self._label is not None:
            self._label.color = new_label

        self._subclass_selected_behavior(value)

    @property
    def selected_label(self) -> int:
        """The font color of the button when selected"""
        return self._selected_label

    @selected_label.setter
    def selected_label(self, new_color: int) -> None:
        self._selected_label = _check_color(new_color)

    @property
    def label_color(self) -> int:
        """The font color of the button"""
        return self._label_color

    @label_color.setter
    def label_color(self, new_color: int) -> None:
        self._label_color = _check_color(new_color)
        self._label.color = self._label_color
