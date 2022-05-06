
from PIL import Image
import numpy as np
from util import *
from camera import *
from objects import *
import random
import threading


class RayTracer():
    samples_per_pixel = 500
    aspect_ratio = 16.0/9.0
    image_width = 400
    ray_depth = 50
    image_height = int((image_width / aspect_ratio))
    use_BVH = True

    def __init__(self):
        self.camera = Camera(
            lookfrom = Vec3(0,2,3),
            lookat = Vec3(0,0,0),
            vup = Vec3(0,1,0),
            fov = 90,
            aspect_ratio = self.aspect_ratio)

        self.world = World(BVH_ON = True)

        self.img = np.zeros((self.image_height, self.image_width, 3), dtype=np.uint8)


    def finalize(self):
        if self.use_BVH:
            self.world.create_BoundingHierarchy()

    def add_object(self, obj:Object):
        self.world.add_object(obj)

    def run(self):
        print(f"Generating image {self.image_height} tall and {self.image_width} wide")
        for j in range(0, self.image_height, 1):
            if j%10 == 0:
                print(f"{100*(j/self.image_height):.2f}% done... \
    Average intersections per ray : {(self.world.count / self.world.ray_count):.2f}")
            for i in range(self.image_width-1, -1, -1):
                
                color = Vec3(0,0,0)
                for _ in range(self.samples_per_pixel):

                    v = (j + random.uniform(0,1)) / (self.image_height-1)
                    u = (i + random.uniform(0,1)) / (self.image_width-1)
                    ray = self.camera.get_ray(u, v)
                    color += self.ray_color(ray, self.world, self.ray_depth)
                self.write_color(j, i , color)



    #writes a color to the output image
    def write_color(self, j, i , color):
        def clamp (x, min, max):
            if (x < min): return min
            if (x > max): return max
            return x
        color /= self.samples_per_pixel
        color = color.sqrt()
        final_color = Vec3(
            int(256 * clamp(color.x, 0.0, 0.999)),
            int(256 * clamp(color.y, 0.0, 0.999)),
            int(256 * clamp(color.z, 0.0, 0.999)),
        )
        self.img[-j+(self.image_height-1),i] = final_color.unwrap()

    #save the image to a file
    def print_image(self,fname):
        pic = Image.fromarray(self.img, 'RGB')
        pic.save(fname)
        pic.show()


    #return the color of a ray shot into the world
    def ray_color(self, ray, world, depth):
        collision = CollisionPacket()

        if depth <= 0:
            return Vec3(0,0,0)

        obj = world.hit(ray,0, collision)
        if obj:
            bounced_ray, attenutation = obj.material.scatter(ray, collision)
            if any(v == 0 for v in bounced_ray.direction.unwrap()):
                return Vec3(0,0,0)
            return attenutation * self.ray_color(bounced_ray, world, depth-1)
            
        ray_dir = ray.unit_direction()
        t = 0.5*(ray_dir.y + 1.0)
        return Vec3(1, 1, 1)*(1.0-t) + Vec3(0.5, 0.7, 1.0)*t


#main driver
def main():

    rt = RayTracer()
    rt.add_object(Sphere( Vec3(0.0,   1.0, 0.0), 1, Dielectric(1.5) ))
    rt.add_object(Sphere( Vec3(-4.0,  1.0, 0.0), 1, Lambertian( SolidColor(Vec3(0.7,0.3,0.3)) ) ))
    rt.add_object(Sphere( Vec3(4.0,   1.0, 0.0), 1, Metal(SolidColor(Vec3(0.8,0.6,0.2))) ))
    rt.add_object(RectFlat(-10,10,-10,10,0, Lambertian( CheckerColor()) ))
    rt.finalize()

    rt.run()
    rt.print_image("scene.png")

if __name__ == "__main__":
    main()
