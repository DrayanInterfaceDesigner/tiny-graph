from lib.maths.Vector2 import Vector2, VEC_ZERO 
from lib.graphics.objects import Manager
class Object:

    DEFAULT: dict = {
        "position": VEC_ZERO,
        "velocity": VEC_ZERO,
        "speed": 0,
        "acceleration": 0,
        "friction": 0.01
    }

    def __init__(self, manager: Manager, params:dict = DEFAULT) -> None:
        self.marked_for_removal: bool = False
        self.position: Vector2 = params.get("position", VEC_ZERO)
        self.velocity: Vector2 = params.get("velocity", VEC_ZERO)
        self.speed: float = params.get("speed", 0)
        self.acceleration: float = params.get("acceleration", 0)
        self.friction: float = params.get("friction", 0.01)
        self.manager: Manager = manager
        self.layer: int = params.get("layer", 0)
        manager.add(self)

    def update(self, dt):
        pass

    def draw(self, ctx):
        pass