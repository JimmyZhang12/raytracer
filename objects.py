
'''
This file contains classes describing the physical objects within the world
Also contains the world class which contains all objects and performs ray intersections
'''

from re import U
from util import *
from camera import *
from boundingbox import *
import sys
import math
from abc import ABC, abstractmethod
from materials import *
from dataclasses import dataclass


#packet describing a ray intersection with an object
@dataclass
class CollisionPacket():
    t          : float = 0          #time to hit
    p          : Vec3 = Vec3(0,0,0) #hit point
    normal     : Vec3 = Vec3(0,0,0) #normal of the hit surface, always against the ray
    front_face : bool = False       #was the surface facing the ray?
    u          : float = 0          #horizontal texture coordinate
    v          : float = 0          #vertical texture coordinate

#Parent class for all objects
#Enforces a ray hit method, bounding box, and y position query
class Object(ABC):
    @property
    @abstractmethod
    def bb(self):
        pass

    @property
    @abstractmethod
    def hit(self, ray, t_min, t_max, collision_packet):
        pass

    @property
    @abstractmethod
    def get_y(self):
        pass

    def set_face_normal(self, ray, outward_normal):
        if Vec3.dot(ray.direction, outward_normal) > 0:
            normal = -1*outward_normal
            front_face = False
        else:
            normal = outward_normal
            front_face = True
        return [normal, front_face]


#Flat plane instance
class RectFlat(Object):
    bb = None
    def __init__(self, x0, x1, z0, z1, k, material:Material):
        self.x0 = x0
        self.x1 = x1
        self.z0 = z0
        self.z1 = z1
        self.k = k
        self.material = material
        self.bb = BB(Vec3(x0, k-0.001, z0), Vec3(x1, k+0.001, z1))

    def get_y(self):
        return self.k

    def hit(self, ray, t_min, t_max, collision_packet):
        if ray.direction.y >=0 and ray.origin.y >= self.k:
            return False

        t = (self.k - ray.origin.y) / ray.direction.y
        if t < t_min or t > t_max:
            return False

        x = ray.origin.x + t*ray.direction.x
        z = ray.origin.z + t*ray.direction.z

        if x<self.x0 or x>self.x1 or z<self.z0 or z>self.z1:
            return False

        outward_normal = Vec3(0,1,0)
        [normal, front_face] = self.set_face_normal(ray, outward_normal)
        p = ray.at(t)

        collision_packet.t = t
        collision_packet.p = p
        collision_packet.normal = normal
        collision_packet.front_face = front_face
        collision_packet.u = (p.x - self.x0) / (self.x1 - self.x0)
        collision_packet.v = (p.z - self.z0) / (self.z1 - self.z0)


        return True

#Physical sphere instance
class Sphere(Object):
    bb = None
    def __init__(self, center: Vec3, radius: Vec3, material: Material):
        self.center = center
        self.radius = radius
        self.material = material
        self.bb = BB(center - Vec3(radius, radius, radius),
            center + Vec3(radius, radius, radius))

    def get_y(self):
        return self.center.y

    def hit(self, ray, t_min, t_max, collision_packet):
        oc = ray.origin - self.center
        a = ray.direction.len_squared()
        half_b = Vec3.dot(oc, ray.direction)
        c = oc.len_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c
        if (discriminant < 0):
            return False
        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False

        t = root
        p = ray.at(t)
        outward_normal = (p - self.center) / self.radius

        norm_p = (p - self.center) / self.radius
        theta = math.acos(-norm_p.y)
        phi = math.atan2(-norm_p.z, norm_p.x) + math.pi
        u = phi / (2*math.pi)
        v = theta / math.pi

        #normal always points against ray
        [normal, front_face] = self.set_face_normal(ray, outward_normal)

        collision_packet.t = t
        collision_packet.p = p
        collision_packet.normal = normal
        collision_packet.front_face = front_face
        collision_packet.u = u
        collision_packet.v = v
        return True

    def __str__(self):
        return f"Sphere, center {self.center} radius {self.radius}"

        

class World():
    hittables = []
    count = 0
    ray_count = 1

    def __init__(self, BVH_ON=True):
        self.use_bb = BVH_ON

    def add_object(self, obj:Object):
        self.hittables.append(obj)

    #bottom up tree 
    def create_BoundingHierarchy(self):
        def combine_boxes(b0, b1):
            small = Vec3(
                min(b0.minv.x, b1.minv.x),
                min(b0.minv.y, b1.minv.y),
                min(b0.minv.z, b1.minv.z))
            big = Vec3(
                max(b0.maxv.x, b1.maxv.x),
                max(b0.maxv.y, b1.maxv.y),
                max(b0.maxv.z, b1.maxv.z))   
            return BB(small, big)

        #sort the object list based on y coordinate
        #this is to try to minimize the size of bounding boxes of the nodes in the BVH
        builder = [o for o in self.hittables]
        builder = sorted(builder, key=lambda x: x.get_y(), reverse=True)

        #if empty scene, BVH is just one trivial node
        if len(builder) == 0:
            self.bb_root = BVH_node(BB(Vec3(0,0,0), Vec3(0,0,0)), None, None)
            return

        #if generate BVH bottom up manner
        #each loop, remove two nodes or objects and attach to a new node with those objects as leaves
        #continue until a single node (the root) is left
        while True:
            temp = []
            while len(builder) > 0:

                if len(builder) >= 2:
                    left = builder.pop()
                    right = builder.pop()
                    combined_box = combine_boxes(left.bb, right.bb)
                else:
                    left = builder.pop()
                    right = None
                    combined_box = left.bb

                node = BVH_node(combined_box, left, right)
                temp.append(node)
            builder = temp 

            if len(builder) == 1:
                break

        #last remaining node is the root of the tree
        self.bb_root = builder[0]
    
    #send a ray into the world
    def hit(self, ray:Ray, t_min, collision_packet):

        ret = False
        closest_so_far = 99999

        if self.use_bb:
            ray_intersect_list = []
            self.bb_root.hit(ray, t_min, t_max=9999, obj_list=ray_intersect_list)
        else:
            ray_intersect_list = self.hittables
        

        self.count += len(ray_intersect_list)
        self.ray_count += 1  

        for obj in ray_intersect_list:
            if obj.hit(ray, t_min, closest_so_far, collision_packet):
                ret = obj
                closest_so_far = collision_packet.t
        return ret
                
