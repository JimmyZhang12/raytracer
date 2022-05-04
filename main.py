from readline import redisplay
from PIL import Image
import numpy as np

class Vec3:
    def __init__(self, arr):
        assert(arr.shape == (3,))
        self.coor = arr

    @classmethod
    def from_val(cls, x,y,z):
        arr = np.array([x,y,z])
        return Vec3(arr)

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
    def dot(cls, vec1, vec2):
        return np.dot(vec1.coor, vec2.coor)

    def unwrap(self):
        return self.coor

    def __add__(self, other):
        return Vec3(self.coor + other.coor)

    def __mul__(self, other):
        return Vec3(self.coor * other)
    def __rmul__(self, other):
        return self.__mul__(other)


    def __truediv__(self, other):
        return Vec3(self.coor / other)

    def __sub__(self, other):
        return Vec3(self.coor - other.coor)        

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
        maxv = np.abs(self._direction.coor).max()
        return self._direction / maxv

    def shoot(self, t):
        return Vec3(self._origin + t*self._direction)




def hit_sphere(center, radius, ray):
    oc = ray.origin - center
    a = Vec3.dot(ray.direction, ray.direction)
    b = 2.0 * Vec3.dot(oc, ray.direction)
    c = Vec3.dot(oc, oc) - radius*radius
    discriminant = b*b - 4*a*c
    return (discriminant > 0)

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
    print(img.shape)
    # data[0:256, 0:256] = [255, 0, 0] # red patch in upper left

    #camera
    viewport_height = 2
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1
    origin = Vec3.from_val(0,0,0)
    horizontal = Vec3.from_val(viewport_width,0,0)
    vertical = Vec3.from_val(0, viewport_height,0)
    lower_left_corner = origin - horizontal/2 - vertical/2 - Vec3.from_val(0,0,focal_length)

    print(lower_left_corner)

    for j in range(image_height-1, -1, -1):
        print(f"row {j}")
        for i in range(image_width-1, -1, -1):
            v = j / (image_height-1)
            u = i / (image_width-1)
            direction = lower_left_corner + u*horizontal + v*vertical - origin

            ray = Ray(origin, direction)
            center = Vec3.from_val(0,0,-1)
            if hit_sphere(Vec3.from_val(0,0,-1), 0.5, ray):
                color = Vec3.from_val(0,0,0)

            else:
                ray_dir = ray.unit_direction()
                t = 0.5*(ray_dir.y + 1.0)
                color = Vec3.from_val(1, 1, 1)*(1.0-t) + Vec3.from_val(0.5, 0.7, 1.0)*t

            color *= 255
            img[j,i] = color.unwrap()

            # print(f" u {u} v {v}| color {color}")

        print_image(img)

