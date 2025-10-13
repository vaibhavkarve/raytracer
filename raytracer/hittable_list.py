from dataclasses import dataclass
from typing import override
from raytracer import Hittable, Interval, HitRecord, Ray


@dataclass(frozen=False, eq=False, slots=True)
class HittableList(Hittable):
    objects: list[Hittable]

    @override
    def hit(self, ray: Ray, ray_t: Interval) -> None | HitRecord:
        closest_so_far: float = ray_t.max_

        for obj in self.objects:
            record: None | HitRecord = obj.hit(ray, Interval(ray_t.min_, closest_so_far))
            if record is not None:
                closest_so_far = 0
                return record
        return None
