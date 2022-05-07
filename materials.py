
'''
Contains classes describing materials and colors
materials are attributes to objects
colors are attributes to materials
'''


from abc import ABC, abstractmethod
from util import Vec3, Ray
import math
from typing import Tuple
from PIL import Image
import numpy as np
import random


#Abstract class representing a material color
#Textures are sampled using u,v coordinates
class Color(ABC):
    @property
    @abstractmethod
    def value(self, u, v) -> Vec3:
        pass

#Uniform color
class SolidColor(Color):
    def __init__(self, color):
        self.color = color
    def value(self, collision):
        return self.color

#A dark green and white checkerboard color
class CheckerColor(Color):
    def value(self, collision):

        if int(collision.v / 0.03)%2 == 0:
            if int(collision.u / 0.03)%2 == 0:
                return Vec3(0.3,0.3,0.3)
            else:
                return Vec3(0.9,0.9,0.3)
        else:
            if int(collision.u / 0.03)%2 == 1:
                return Vec3(0.3,0.3,0.3)
            else:
                return Vec3(0.9,0.9,0.3)

#A textture, loads from an image file
class Texture(Color):
    def __init__(self, fname):
        print(f"Loading Texture from: {fname}")
        image = Image.open(fname)
        self.img = np.asarray(image).astype(float)
        self.img /= 255
        self.height = self.img.shape[0]
        self.width = self.img.shape[1]
        print(f"Done!")

    def value(self, collision):
        h = int(collision.v*self.height)
        w = int(collision.u*self.width)
        return Vec3.from_array(self.img[h][w])
    pass


#Parents class for materials
#Used to get a ray bounce and color based on the material properties
#Child classes must implement the ray bounce calculation
class Material(ABC):
    albedo = None

    def reflect(self, v, n) -> Vec3:
        return v - 2*Vec3.dot(v,n)*n 

    def refract(self, uv, n, refact_ratio) -> Vec3:
        cos_theta = min(Vec3.dot(-1*uv, n), 1.0)
        r_out_perp = refact_ratio * (uv + (cos_theta*n))
        r_out_parallel = -1*math.sqrt(abs(1.0 - r_out_perp.len_squared())) * n

        return r_out_perp + r_out_parallel
    
    def random_unit_sphere(self) -> Vec3:
        while (True):
            p = Vec3.random(-1,1)
            if (p.len_squared() >= 1):
                continue
            return p

    def scatter(self, inc_ray, collision) -> Tuple[Ray, Vec3]:
        new_ray = self.bounce_ray(inc_ray, collision)
        color = self.albedo.value(collision)
        return (new_ray, color)

    @property
    @abstractmethod
    def bounce_ray(self, inc_ray, collision) -> Ray:
        pass


class Lambertian(Material):
    def __init__(self, albedo:Color = None):
        if albedo == None:
            self.albedo=SolidColor(
                Vec3(random.uniform(0.3,1),random.uniform(0.3,1),random.uniform(0.3,1)))
        else:
            self.albedo = albedo

    def bounce_ray(self, inc_ray, collision):
        rand_dir = self.random_unit_sphere().unit_length()
        scatter_direction = collision.normal + rand_dir

        if scatter_direction.len_squared() < 0.001:
            scatter_direction = collision.normal
        scattered = Ray(collision.p, scatter_direction)

        return scattered

class Metal(Material):
    def __init__(self, albedo=None):
        if albedo == None:
            self.albedo=SolidColor(
                Vec3(random.uniform(0.3,1),random.uniform(0.3,1),random.uniform(0.3,1)))
        else:
            self.albedo = albedo

    def bounce_ray(self, inc_ray, collision):
        scatter_direction = self.reflect(inc_ray.unit_direction(), collision.normal)
        if scatter_direction.len_squared() < 0.001:
            scatter_direction = collision.normal
        scattered = Ray(collision.p, scatter_direction)

        return scattered

class Dielectric(Material):
    def __init__(self, index_of_refract=1.5):
        self.index_of_refract = index_of_refract
        self.albedo = SolidColor(Vec3(1,1,1))
        
    def bounce_ray(self, inc_ray, collision):
        if collision.front_face:
            refraction_ratio = 1 / self.index_of_refract
        else:
            refraction_ratio = self.index_of_refract

        unit_direction = inc_ray.unit_direction()
        cos_theta = min(Vec3.dot(-1*unit_direction, collision.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0
        if (cannot_refract):
            refract_direction = self.reflect(inc_ray.unit_direction(), collision.normal)
        else:
            refract_direction = self.refract(inc_ray.unit_direction(), collision.normal, refraction_ratio)

        scattered = Ray(collision.p, refract_direction)
        return scattered