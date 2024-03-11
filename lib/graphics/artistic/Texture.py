from lib.graphics.shapes.Object import Object
from lib.graphics.shapes.Vertice import Vertice
from lib.maths.Vector2 import Vector2
from lib.graphics.objects.Manager import Manager

class Texture(Object):
    def __init__(self, manager: Manager, params: dict = ...):
        super().__init__(manager, params)
        self.tag: str = params.get("tag", len(manager.objects))
        self.texture_path: str = params.get("texture", "")
        self.original_position: Vector2 = self.position.copy()

    def load_texture(self):
        self.texture = self.manager.loader.load_texture(self.texture_path)

    def load_vertices(self, vertices: list):
        for vertex in vertices:
            self.vertices.append(Vertice(self.manager, vertex))

    def draw(self):
        self.texture.blit(0, 0)
        for vertex in self.vertices:
            vertex.draw()
        pass