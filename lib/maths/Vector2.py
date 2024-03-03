import math

class Vector2:
    def __init__(self, x, y) -> None:
        self.x: float = x
        self.y: float = y
    
    def __add__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return Vector2(self.x + other, self.y + other)
    
    def __sub__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return Vector2(self.x - other, self.y - other)
    
    def __mul__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not (self == other)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    
    def lerp(self, other, t):
        return Vector2(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t
        )
    
    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    
    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5
    
    def normalize(self):
        return self / self.magnitude()
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def angle(self, other):
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))
    
    def rotate(self, angle):
        return Vector2(
            self.x * math.cos(angle) - self.y * math.sin(angle),
            self.x * math.sin(angle) + self.y * math.cos(angle)
        )
    
    def copy(self):
        return Vector2(self.x, self.y)
    
    def to_tuple(self):
        return (self.x, self.y)
    
    def to_list(self):
        return [self.x, self.y]
    
    def to_int(self):
        return Vector2(int(self.x), int(self.y))
    
    def point_to(self, other):
        return math.atan2(other.y - self.y, other.x - self.x)

VEC_ZERO = Vector2(0,0)