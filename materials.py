

from abc import ABC, abstractmethod
from util import Vec3, Ray
import math

class Material(ABC):
    def reflect(self, v, n):
        return v - 2*Vec3.dot(v,n)*n

    def refract(self, uv, n, refact_ratio):
        cos_theta = min(Vec3.dot(-1*uv, n), 1.0)
        r_out_perp = refact_ratio * (uv + (cos_theta*n))
        r_out_parallel = -1*math.sqrt(abs(1.0 - r_out_perp.len_squared())) * n

        return r_out_perp + r_out_parallel
    
    def random_unit_sphere(self):
        while (True):
            p = Vec3.random(-1,1)
            if (p.len_squared() >= 1):
                continue
            return p
            
    @abstractmethod
    def scatter(self, inc_ray, normal, point, front_face):
        pass

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, inc_ray, normal, point, front_face):
        rand_dir = self.random_unit_sphere()
        scatter_direction = normal + rand_dir

        if scatter_direction.len_squared() < 0.001:
            scatter_direction = normal
        scattered = Ray(point, scatter_direction)

        return (scattered, self.albedo)

class Metal(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, inc_ray, normal, point, front_face):
        scatter_direction = self.reflect(inc_ray.unit_direction(), normal)
        if scatter_direction.len_squared() < 0.001:
            scatter_direction = normal
        scattered = Ray(point, scatter_direction)
        return (scattered, self.albedo)

class Dielectric(Material):
    def __init__(self, index_of_refract):
        self.index_of_refract = index_of_refract
    
    def scatter(self, inc_ray, normal, point, front_face):
        attenuation = Vec3(1,1,1)
        if front_face:
            refraction_ratio = 1 / self.index_of_refract
        else:
            refraction_ratio = self.index_of_refract

        unit_direction = inc_ray.unit_direction()
        cos_theta = min(Vec3.dot(-1*unit_direction, normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0
        if (cannot_refract):
            refract_direction = self.reflect(inc_ray.unit_direction(), normal)
        else:
            refract_direction = self.refract(inc_ray.unit_direction(), normal, refraction_ratio)

        scattered = Ray(point, refract_direction)
        return (scattered, attenuation)