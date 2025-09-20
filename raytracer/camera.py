import sys
from random import random
from raytracer import (Point3, Vec3, HittableList, Color,
                       Ray, Hittable, HitRecord, Interval)


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


    def render(self, world: HittableList) -> None:
        print("P3")  # PPM file is in ascii format.
        print(self.image_width, self.image_height)
        print(255)  # Max pixel color value.

        for j in range(self.image_height):
            print(f"\rScanlines remaining: {self.image_height - j:3d}",
                  file=sys.stderr, end="", flush=True)
            for i in range(self.image_width):
                pixel_color: Color = Color(0, 0, 0)  # Black.
                for _ in range(self.samples_per_pixel):
                    ray: Ray = self.get_ray(i, j)
                    pixel_color += self.ray_color(ray, world)
                (self.pixel_samples_scale * pixel_color).write()

        print(f"\r{'Done':24s}", file=sys.stderr)

    @staticmethod
    def ray_color(ray: Ray, world: Hittable) -> Color:
        record: None | HitRecord = world.hit(ray, Interval(0, float("inf")))
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

    def get_ray(self, i: int, j: int) -> Ray:
        """Construct a camera ray originating from the origin and directed
        at randomly sampled point around the pixel location i, j."""
        offset: Vec3 = self.sample_square()
        pixel_sample: Vec3 = (
            self.pixel00_loc
            + (i + offset.x) * self.pixel_delta_u
            + (j + offset.y) * self.pixel_delta_v
        )
        ray_origin: Point3 = self.center
        ray_direction: Vec3 = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    @staticmethod
    def sample_square() -> Vec3:
        """Returns the vector to a random point in the [-.5, -.5] x [+.5, +.5]
        unit square."""
        return Vec3(random() - 0.5, random() - 0.5, 0)
