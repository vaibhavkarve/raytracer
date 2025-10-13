from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=False, eq=False, slots=True)
class Interval:
    min_: float
    max_: float

    def size(self) -> float:
        return self.max_ - self.min_

    def __contains__(self, x: float) -> bool:
        return self.min_ <= x <= self.max_

    def surrounds(self, x: float) -> bool:
        return self.min_ < x < self.max_

    @staticmethod
    def empty() -> Interval:
        return Interval(min_=float("inf"), max_=-float("inf"))

    @staticmethod
    def universe() -> Interval:
        return Interval(min_=-float("inf"), max_=float("inf"))

    def clamp(self, x: float) -> float:
        if x < self.min_:
            return self.min_
        if x > self.max_:
            return self.max_
        return x
