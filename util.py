
import random
import math

#Helper classes and useful functions:
#A Vec3 class
#A ray class composed two two Vec3s

class Vec3:
    def __init__(self, x, y, z):
        self.coor = [x,y,z]


    @classmethod
    def from_array(cls, arr):
        return Vec3(arr[0], arr[1], arr[2])

    def unwrap(self):
        return self.coor

    @property
    def x(self):
        return self.coor[0]
    @property
    def y(self):
        return self.coor[1]
    @property
    def z(self):
        return self.coor[2]

    @classmethod
    def dot(cls, n1, n2):
        vec1 = n1.coor
        vec2 = n2.coor
        return vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2]

    @classmethod
    def cross(cls, n1, n2):
        v1 = n1.coor
        v2 = n2.coor
        return Vec3(v1[1]*v2[2] - v1[2]*v2[1],
                    v1[2]*v2[0] - v1[0]*v2[2],
                    v1[0]*v2[1] - v1[1]*v2[0])

    @classmethod
    def random(cls, lo, hi):
        return Vec3(random.uniform(lo, hi),
            random.uniform(lo, hi),
            random.uniform(lo, hi))  

    # def norm(self):
    #     maxv = abs(max(self.coor, key=abs))
    #     return Vec3(self.coor[0]/maxv, self.coor[1]/maxv, self.coor[2]/maxv)

    def unit_length(self):
        length = math.sqrt(self.len_squared())
        return Vec3(self.coor[0]/length, self.coor[1]/length, self.coor[2]/length)

    def sqrt(self):
        return Vec3(math.sqrt(self.coor[0]), math.sqrt(self.coor[1]), math.sqrt(self.coor[2]))

    def len_squared(self):
        return self.coor[0]*self.coor[0] + self.coor[1]*self.coor[1] + self.coor[2]*self.coor[2]


    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.coor[0] + other.coor[0],
                self.coor[1] + other.coor[1],
                self.coor[2] + other.coor[2])
        return Vec3(self.coor[0] + other,
            self.coor[1] + other,
            self.coor[2] + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.coor[0]*other.coor[0],
                self.coor[1]*other.coor[1],
                self.coor[2]*other.coor[2])
        return Vec3(self.coor[0]*other,
            self.coor[1]*other,
            self.coor[2]*other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Vec3(self.coor[0]/other,
            self.coor[1]/other,
            self.coor[2]/other)

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.coor[0] - other.coor[0],
                self.coor[1] - other.coor[1],
                self.coor[2] - other.coor[2])
        return Vec3(self.coor[0] - other,
            self.coor[1] - other,
            self.coor[2] - other)            

    def __getitem__(self, key):
        return self.coor[key]

    def __str__(self):
        return f"({self.coor})"

class Point3(Vec3):
    def __init__(self, x, y, z):
        Vec3.__init__(self, x, y, z)
    def __init__(self, arr):
        Vec3.__init__(arr)



class Ray:
    def __init__(self, origin, direction):
        assert(isinstance(origin, Vec3))
        assert(isinstance(direction, Vec3))

        self._origin = origin
        self._direction = direction

    @property
    def origin(self):
        return self._origin

    @property
    def direction(self):
        return self._direction

    def unit_direction(self):
        return self._direction.unit_length()

    def at(self, t):
        return self._origin + self._direction*t


