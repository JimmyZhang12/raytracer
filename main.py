from re import T
from readline import redisplay
from site import removeduppaths
from PIL import Image
import numpy as np
from util import *
from camera import *
import math

class Sphere():
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def hit(self, ray, t_min, t_max):
        oc = ray.origin - self.center
        a = ray.direction.len_squared()
        half_b = Vec3.dot(oc, ray.direction)
        c = oc.len_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c
        if (discriminant < 0):
            return False
        sqrtd = math.sqrt(discriminant);

        # Find the nearest root that lies in the acceptable range.
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False

        t = root
        p = ray.at(t)
        normal = (p - self.center) / self.radius
        return [t, p, normal]
        

class World():
    hittables = []
    def add_object(self, object):
        self.hittables.append(object)
    def hit(self, ray, t_min):
        ret = False
        closest_so_far = 99999

        for obj in self.hittables:
            tryhit = obj.hit(ray, t_min, closest_so_far)
            if tryhit:
                [t, p, normal] = tryhit
                ret = [t, p, normal]
                closest_so_far = t
        return ret
                


def print_image(data):
    data.astype(int)
    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    img.show()

if __name__ == "__main__":
    #image 
    aspect_ratio = 16.0/9.0
    image_width = 400
    image_height = int((image_width / aspect_ratio))
    img = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    #camera
    camera = Camera(aspect_ratio)

    world = World()
    world.add_object(Sphere(Vec3.from_val(0,0,-1), 0.5))
    world.add_object(Sphere(Vec3.from_val(0,-100.5,-1), 100))

    print(f"Generating image {image_height} tall and {image_width} wide")
    for j in range(image_height-1, -1, -1):
        print(f"row {j}")
        for i in range(image_width-1, -1, -1):
            v = j / (image_height-1)
            u = i / (image_width-1)
            ray = camera.get_ray(u, v)

            pt = world.hit(ray,0)
            if pt:
                [t, p, N] = pt
                color = 0.5*(N + 1)

            else:
                ray_dir = ray.unit_direction()
                t = 0.5*(ray_dir.y + 1.0)
                color = Vec3.from_val(1, 1, 1)*(1.0-t) + Vec3.from_val(0.5, 0.7, 1.0)*t

            color *= 255
            # print(f" u {u} v {v}, j {j} v {i}| t {t}")
            img[-j+(image_height-1),i] = color.unwrap()

            # input()
        print_image(img)

