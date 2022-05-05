
from PIL import Image
import numpy as np
from util import *
from camera import *
from objects import *
import random
import cProfile
import threading

def write_color(image_height, j, i , color, img, num_samples):
    def clamp (x, min, max):
        if (x < min): return min
        if (x > max): return max
        return x
    color /= num_samples
    color = color.sqrt()
    final_color = Vec3(
        int(256 * clamp(color.x, 0.0, 0.999)),
        int(256 * clamp(color.y, 0.0, 0.999)),
        int(256 * clamp(color.z, 0.0, 0.999)),
    )
    img[-j+(image_height-1),i] = final_color.unwrap()

def print_image(data):
    data.astype(int)
    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    img.show()


def random_unit_sphere():
    while (True):
        p = Vec3.random(-1,1)
        if (p.len_squared() >= 1):
            continue
        return p


def ray_color(ray, world, depth):

    if depth <= 0:
        return Vec3(0,0,0)

    pt = world.hit(ray,0)
    if pt:
        [t, p, N, front_face, obj] = pt
        bounced_ray, attenutation = obj.material.scatter(ray, N, p, front_face)

        return attenutation * ray_color(bounced_ray, world, depth-1)
    ray_dir = ray.unit_direction()
    t = 0.5*(ray_dir.y + 1.0)
    return Vec3(1, 1, 1)*(1.0-t) + Vec3(0.5, 0.7, 1.0)*t

def run():
    #INITIALIZATION
    samples_per_pixel = 50
    aspect_ratio = 16.0/9.0
    image_width = 200
    ray_depth = 8
    image_height = int((image_width / aspect_ratio))

    #CAMERA
    camera = Camera(
        lookfrom = Vec3(0,0,0),
        lookat = Vec3(0,0,-1),
        vup = Vec3(0,1,0),
        fov = 90,
        aspect_ratio = aspect_ratio)

    world = World()
    world.add_object(Sphere(Vec3( 0.0, -100.5, -1.0), 100.0, Lambertian(Vec3(0.8,0.8,0))))
    world.add_object(Sphere(Vec3( 0.0,    0.0, -1.0),   0.5, Lambertian(Vec3(0.7,0.3,0.3))))
    world.add_object(Sphere(Vec3(-1.0,    0.0, -1.0),   0.5, Dielectric(2)))
    world.add_object(Sphere(Vec3( 1.0,    0.0, -1.0),   0.5, Metal(Vec3(0.8,0.6,0.2))))


    print(f"Generating image {image_height} tall and {image_width} wide")
    img = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    for j in range(image_height-1, -1, -1):
        print(f"row {j}")
        for i in range(image_width-1, -1, -1):

            color = Vec3(0,0,0)
            for _ in range(samples_per_pixel):

                v = (j + random.uniform(0,1)) / (image_height-1)
                u = (i + random.uniform(0,1)) / (image_width-1)

                ray = camera.get_ray(u, v)
                color += ray_color(ray, world, ray_depth)

            write_color(image_height, j, i , color, img, samples_per_pixel)

    print_image(img)

if __name__ == "__main__":
    run()
