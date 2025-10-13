from __future__ import annotations
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING, cast
import math
import numpy as np
import numpy.typing as npt

if TYPE_CHECKING:
    from raytracer.color import Color


@dataclass(frozen=False, eq=False, slots=True)
class Vec3:
    x: float
    y: float
    z: float

    def __mul__(self, other: Any) -> Vec3:
        if isinstance(other, (float, int)):
            return Vec3(self.x * other,
                        self.y * other,
                        self.z * other)
        return NotImplemented

    def __rmul__(self, other: Any) -> Vec3:
        if isinstance(other, (float, int)):
            return self * other
        return NotImplemented

    def __add__[T: (Vec3, Color)](self, other: T) -> T:
        from raytracer.color import Color  # Avoid circular import.
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x,
                        self.y + other.y,
                        self.z + other.z)
        if isinstance(other, Color):
            return Color(self.x + other.r,
                         self.y + other.g,
                         self.z + other.b)
        return NotImplemented

    def __truediv__(self, other: Any) -> Vec3:
        if isinstance(other, (float, int)):
            return self * (1.0 / other)
        return NotImplemented

    def __sub__(self, other: Any) -> Any:
        if isinstance(other, Vec3):
            return self + (- other)
        return NotImplemented

    def __neg__(self) -> Vec3:
        return -1.0 * self

    def __matmul__(self, other: Any) -> float:
        if isinstance(other, Vec3):
            return (self.x * other.x
                    + self.y * other.y
                    + self.z * other.z)
        return NotImplemented

    def length_squared(self) -> float:
        return self @ self

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def unit_vector(self) -> Vec3:
        return self / self.length()

    def to_array(self) -> npt.NDArray[np.float64]:
        return np.array([self.x, self.y, self.z])

Point3 = Vec3  # Class Alias
