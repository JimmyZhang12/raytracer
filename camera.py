from util import *

#A moveable camera class
#The camera generates ray that are shot into the world

class Camera():
    def __init__(self, lookfrom, lookat, vup, fov, aspect_ratio):
        self.aspect_ratio = aspect_ratio 
        self.fov = fov
        #camera
        theta = math.radians(fov)
        h = math.tan(theta/2)
        viewport_height = 2.0*h
        viewport_width = self.aspect_ratio * viewport_height

        w = (lookfrom - lookat).unit_length()
        u = Vec3.cross(vup, w).unit_length()
        v = Vec3.cross(w, u)

        self.origin = lookfrom
        self.horizontal = viewport_width * u
        self.vertical = viewport_height * v
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - w

        # self.focal_length = 1.0
        # self.origin = Vec3(0,0,0)
        # self.horizontal = Vec3(self.viewport_width,0,0)
        # self.vertical = Vec3(0, self.viewport_height,0)
        # self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - Vec3(0,0,self.focal_length)

    def get_ray(self, u, v):
        direction = (self.lower_left_corner + self.horizontal*u + self.vertical*v) - self.origin
        return Ray(self.origin, direction)
