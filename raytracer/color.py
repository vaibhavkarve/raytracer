from __future__ import annotations
import sys
from dataclasses import dataclass
from typing import IO, Any
from raytracer import Interval, Vec3


@dataclass(frozen=True, eq=False, slots=True)
class Color:
    r: float
    g: float
    b: float

    def __mul__(self, other: Any) -> Color:
        if isinstance(other, (float, int)):
            return Color(self.r * other,
                        self.g * other,
                        self.b * other)
        return NotImplemented

    def __rmul__(self, other: Any) -> Color:
        if isinstance(other, (float, int)):
            return self * other
        return NotImplemented

    def __add__(self, other: Any) -> Color:
        if isinstance(other, Color):
            return Color(self.r + other.r,
                         self.g + other.g,
                         self.b + other.b)
        if isinstance(other, Vec3):
            return Color(self.r + other.x,
                         self.g + other.y,
                         self.b + other.z)
        return NotImplemented

    def write(self, out: IO[str] = sys.stdout) -> None:

        # Translate the [0, 1] component values to the byte range [0, 255].
        intensity: Interval = Interval(0, 0.999)
        rbyte: int = int(256 * intensity.clamp(self.r))
        gbyte: int = int(256 * intensity.clamp(self.g))
        bbyte: int = int(256 * intensity.clamp(self.b))
        print(rbyte, gbyte, bbyte, file=out)
