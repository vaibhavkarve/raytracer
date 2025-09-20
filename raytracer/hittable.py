from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from raytracer import Vec3, Point3, Ray, isclose, Interval


@dataclass(frozen=True, eq=False, slots=True)
class HitRecord:
    point: Point3
    normal: Vec3
    t: float
    front_face: bool

    @staticmethod
    def from_outward_normal(point: Point3,
                            t: float,
                            ray: Ray,
                            outward_normal: Vec3) -> HitRecord:
        """Sets the normal vector using a ray and an outward normal"""
        assert isclose(outward_normal.length(), 1), f"{outward_normal.length() = }"

        front_face: bool = (ray.direction @ outward_normal) < 0
        return HitRecord(
            point=point,
            normal=outward_normal if front_face else -outward_normal,
            front_face=front_face,
            t=t
        )


class Hittable(ABC):
    @abstractmethod
    def hit(self, ray: Ray, ray_t: Interval) -> None | HitRecord:
        ...
