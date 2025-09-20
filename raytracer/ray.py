from dataclasses import dataclass
from raytracer import Vec3, Point3


@dataclass(frozen=True, eq=False, slots=True)
class Ray:
    origin: Point3
    direction: Vec3

    def at(self, t: float) -> Point3:
        return self.origin + t * self.direction
