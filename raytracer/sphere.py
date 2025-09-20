from typing import override
from raytracer import Hittable, Point3, HitRecord, Interval, Ray, Vec3, sqrt


class Sphere(Hittable):
    def __init__(self, center: Point3, radius: float) -> None:
        self.center: Point3 = center
        self.radius: float = max(0, radius)

    @override
    def hit(self, ray: Ray, ray_t: Interval) -> None | HitRecord:
        oc: Vec3 = self.center - ray.origin
        a: float = ray.direction.length_squared()
        h: float = ray.direction @ oc
        c: float = oc.length_squared() - self.radius**2
        discriminant: float = h**2 - a*c

        if discriminant < 0:
            return None

        sqrtd: float = sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root: float = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return None

        return HitRecord.from_outward_normal(
            point=ray.at(root),
            t=root,
            ray=ray,
            outward_normal=(ray.at(root) - self.center) / self.radius)
