import sys
from time import time
from raytracer import HittableList, Sphere, Point3, Camera



def main() -> int:
    time0: float = time()

    world: HittableList = HittableList(objects = [
        Sphere(Point3(0, 0, -1), 0.5),
        Sphere(Point3(0, -100.5, -1), 100),
    ])

    cam: Camera = Camera(
        aspect_ratio = 16 / 9,
        image_width = 400,
        samples_per_pixel = 1,  # Currently set to 1 because antialiasing is slow.
    )
    cam.render(world)

    print(f"Time taken: {time() - time0:.2f}s", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
