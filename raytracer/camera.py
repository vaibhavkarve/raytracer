import sys
from random import random
from raytracer import (Point3, Vec3, HittableList, Color,
                       Ray, Hittable, HitRecord, Interval)
from line_profiler import profile
import numpy as np
import numpy.typing as npt
import itertools as it


class Camera:
    def __init__(
            self,
            aspect_ratio: float = 16/9,
            image_width: int = 400,
            samples_per_pixel: int = 10
    ) -> None:
        """Initialize a camera, a viewport and an image.

        Note that the code uses the aspect ratio as a guide but the final
        image height and width can only approximate the aspect ratio.

        """
        self.aspect_ratio: float = aspect_ratio
        self.image_width: int = image_width
        self.samples_per_pixel: int = samples_per_pixel  # For antialiasing.

        # All the other values are derived or constants.
        self.image_height: int = max(1, int(self.image_width / self.aspect_ratio))
        self.center: Point3 = Point3(0, 0, 0)  # Camera center.
        self.pixel_samples_scale: float = 1 / self.samples_per_pixel

        # Determine viewport dimensions.
        self.focal_length: float = 1
        self.viewport_height: float = 2
        self.viewport_width: float = self.viewport_height * (self.image_width / self.image_height)

        # Calculate the vectors across the horizontal and down the vertical
        # viewport edges.
        self.viewport_u: Vec3 = Vec3(self.viewport_width, 0, 0)
        self.viewport_v: Vec3 = Vec3(0, -self.viewport_height, 0)

        # Calculate the horizontal and vertical delta vectors from pixel to
        # pixel.
        self.pixel_delta_u: Vec3 = self.viewport_u / self.image_width
        self.pixel_delta_v: Vec3 = self.viewport_v / self.image_height

        # Calculate the location of the upper left pixel.
        self.viewport_upper_left: Point3 = (
            self.center
            - Vec3(0, 0, self.focal_length)
            - self.viewport_u / 2
            - self.viewport_v / 2
        )
        self.pixel00_loc: Point3 = (
            self.viewport_upper_left
            + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)
        )

    @profile  # type: ignore[misc]
    def render(self, world: HittableList, rng: np.random.Generator) -> None:
        print("P3")  # PPM file is in ascii format.
        print(self.image_width, self.image_height)
        print(255)  # Max pixel color value.

        for j in range(self.image_height):
            print(f"\rScanlines remaining: {self.image_height - j:3d}",
                  file=sys.stderr, end="", flush=True)
            for i in range(self.image_width):
                pixel_color: Color = Color(0, 0, 0)  # Black.
                ray_origins, ray_directions = self.get_rays(rng, i, j)
                for origin, direction in zip(ray_origins, ray_directions):
                    ray: Ray = Ray(origin, direction)
                    pixel_color += self.ray_color(ray, world)
                (self.pixel_samples_scale * pixel_color).write()

        print(f"\r{'Done':24s}", file=sys.stderr)

    @staticmethod
    def ray_color(ray: Ray, world: Hittable) -> Color:
        record: None | HitRecord = world.hit(
            ray, Interval(0, float("inf")))
        if record is not None:
            # We hit something.
            return 0.5 * (record.normal + Color(1, 1, 1))

        # Nothing was hit => background.
        unit_direction: Vec3 = ray.direction.unit_vector()
        a: float = 0.5 * (unit_direction.y + 1)
        return (
            (1 - a) * Color(1, 1, 1)
            + a * Color(0.5, 0.7, 1)
        )

    def get_rays(self, rng: np.random.Generator, i: int, j: int) \
            -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """Construct all camera rays originating from the origin and directed
        at randomly sampled points around the pixel location i, j."""
        offsets: npt.NDArray[np.float64] \
            = rng.uniform(low=-0.5, high=0.5, size=self.samples_per_pixel * 2).reshape(self.samples_per_pixel, 2)

        pixel_sample_xs: npt.NDArray[np.float64] = self.pixel00_loc.x + (i + offsets[:, 0]) * self.pixel_delta_u.x
        pixel_sample_ys: npt.NDArray[np.float64] = self.pixel00_loc.y + (j + offsets[:, 1]) * self.pixel_delta_v.y
        pixel_sample_zs: npt.NDArray[np.float64] = np.repeat(self.pixel00_loc.z, self.samples_per_pixel)
        pixel_samples: npt.NDArray[Vec3] = np.array(list(it.starmap(Vec3, zip(pixel_sample_xs, pixel_sample_ys, pixel_sample_zs))))

        ray_origins: npt.NDArray[Vec3] = np.repeat(self.center, self.samples_per_pixel)
        ray_directions: npt.NDArray[Vec3] = pixel_samples - ray_origins

        return ray_origins, ray_directions

    @staticmethod
    def sample_square() -> Vec3:
        """Returns the vector to a random point in the [-.5, -.5] x [+.5, +.5]
        unit square."""
        return Vec3(random() - 0.5, random() - 0.5, 0)
