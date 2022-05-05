
from util import *
import objects

#Bounding box classes
#BVH_node: a node within bounding hierachy tree
#BB: The actual bounding box which can be queried for collision

class BVH_node():
    def __init__(self, bb, left, right):
        self.left = left
        self.right = right
        self.bb = bb

    def hit(self, ray, t_min, t_max, obj_list):
        if self.bb.hit(ray, t_min, t_max):
            if self.left is not None:
                if isinstance(self.left, BVH_node):
                    self.left.hit(ray, t_min, t_max, obj_list)
                elif isinstance(self.left, objects.Object):
                    obj_list.append(self.left)

            if self.right is not None:
                if isinstance(self.right, BVH_node):
                    self.right.hit(ray, t_min, t_max, obj_list)
                elif isinstance(self.right, objects.Object):
                    obj_list.append(self.right)

    def __str__(self):
        return f"BVH_node: {self.bb} , \n \tleft {self.left} \n\tright {self.right}"

class BB():
    def __init__(self, minv, maxv):
        self.minv = minv
        self.maxv = maxv

    def hit(self, ray, t_min, t_max):
        for a in range(0,3):
            t0 = min(
                (self.minv.unwrap()[a] - ray.origin.unwrap()[a]) / ray.direction.unwrap()[a],
                (self.maxv.unwrap()[a] - ray.origin.unwrap()[a]) / ray.direction.unwrap()[a])
            t1 = max(
                (self.minv.unwrap()[a] - ray.origin.unwrap()[a]) / ray.direction.unwrap()[a],
                (self.maxv.unwrap()[a] - ray.origin.unwrap()[a]) / ray.direction.unwrap()[a])
            t_min = max(t0, t_min)
            t_max = min(t1, t_max)

            if t_max <= t_min:
                return False
        return True

    def __str__(self):
        return f"BB: {self.minv} , {self.maxv}"