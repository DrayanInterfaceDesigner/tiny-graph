
from lib.maths.Vector2 import Vector2

class BoundingBox:
    def __init__(self, screen_size: Vector2, size: dict) -> None:
        self.boundings: list = []
        self.position: Vector2 = Vector2(0, 0)
        self.real_position: Vector2 = Vector2(0, 0)
        self.screen_size: Vector2 = screen_size
        self.size: dict = size
        self.calc_boundings()



    def calc_offset(self):
        self.real_position = self.position - self.screen_size / 2
    
    def update(self, dt):
        self.calc_offset()




