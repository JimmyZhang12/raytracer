
from PIL import Image
import numpy as np
from util import *
from camera import *
from objects import *
import random
import cProfile
import threading


#writes a color to the output image
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

#save the image to a jpeg in the current pwd
def print_image(data):
    data.astype(int)
    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    img.show()

            

#return the color of a ray shot into the world
def ray_color(ray, world, depth):
    if depth <= 0:
        return Vec3(0,0,0)

    pt = world.hit(ray,0)
    if pt:
        [t, p, N, front_face, obj] = pt
        bounced_ray, attenutation = obj.material.scatter(ray, N, p, front_face)
        if any(v == 0 for v in bounced_ray.direction.unwrap()):
            return Vec3(0,0,0)

        return attenutation * ray_color(bounced_ray, world, depth-1)
        
    ray_dir = ray.unit_direction()
    t = 0.5*(ray_dir.y + 1.0)
    return Vec3(1, 1, 1)*(1.0-t) + Vec3(0.5, 0.7, 1.0)*t

class 

#main driver
def run():
    #PARAMETERS
    samples_per_pixel = 50
    aspect_ratio = 16.0/9.0
    image_width = 100
    ray_depth = 50
    image_height = int((image_width / aspect_ratio))

    #CAMERA
    camera = Camera(
        lookfrom = Vec3(0,2,3),
        lookat = Vec3(0,0,0),
        vup = Vec3(0,1,0),
        fov = 90,
        aspect_ratio = aspect_ratio)

    #insert objects into world
    world = World()
    # world.add_object(Sphere(
    #     Vec3(0,-1000,0), 1000, Lambertian(0.5)
    #     ))
    world.add_object(Sphere(Vec3(0.0,   1.0, 0.0),   1, Dielectric(1.5)))
    world.add_object(Sphere(Vec3(-4.0,  1.0, 0.0),   1, Lambertian(Vec3(0.7,0.3,0.3))))
    world.add_object(Sphere(Vec3(4.0,   1.0, 0.0),    1, Metal(Vec3(0.8,0.6,0.2))))
    world.add_object(RectFlat(-10,10,-10,10,0, Lambertian(0.5)))

    #create the bounding hierachy
    world.create_BoundingHierarchy()

    print(f"Generating image {image_height} tall and {image_width} wide")
    img = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    for j in range(0, image_height, 1):
        if j%10 == 0:
            print(f"{100*(j/image_height):.2f}% done... \
    Average intersections per ray : {(world.count / world.ray_count):.2f}")
        for i in range(image_width-1, -1, -1):
            
            color = Vec3(0,0,0)
            for _ in range(samples_per_pixel):

                v = (j + random.uniform(0,1)) / (image_height-1)
                u = (i + random.uniform(0,1)) / (image_width-1)
                ray = camera.get_ray(u, v)
                color += ray_color(ray, world, ray_depth)
            # print(f"v {v} u {u} color {255*(color/samples_per_pixel).sqrt()}")
            write_color(image_height, j, i , color, img, samples_per_pixel)
    print_image(img)

if __name__ == "__main__":
    run()
