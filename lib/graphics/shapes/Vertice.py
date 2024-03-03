from lib.graphics.objects.Manager import Manager
from lib.graphics.shapes import Object
from lib.graphics.shapes.Edge import Edge
from lib.maths.Vector2 import VEC_ZERO, Vector2
import random
import cairo

class Vertice(Object):
    def __init__(self, manager: Manager, params: dict = ...) -> None:
        super().__init__(manager, params)
        self.tag: str = params.get("tag", len(manager.objects))
        self.radius: float = params.get("radius", 10)
        self.color: tuple = params.get("color", (255, 255, 255))
        self.value: float = params.get("value", 0)
        self.selected: bool = False
        self.dragging: bool = False
        self.connections:list = []
        self.original_position: Vector2 = self.position.copy()
    
    def update(self, dt):
        random_direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        displacement = random_direction * 0.3

        self.position += displacement

        self.position = self.position.lerp(self.original_position, 0.1 * dt)

    # def draw_label(self, ctx):
    #     ctx.set_source_rgb(self.font_color[0]/255, self.font_color[1]/255, self.font_color[2]/255)
    #     ctx.select_font_face(self.font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    #     ctx.set_font_size(self.font_size)
    #     ctx.move_to(self.position.x + self.font_offset.x, self.position.y + self.font_offset.y)
    #     ctx.show_text(self.label)

    def draw(self, ctx):
        
        ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
        ctx.arc(self.position.x, self.position.y, self.radius, 0, 2 * 3.14)
        ctx.fill()

    def connect(self, vertice, options:dict = {}):
        
        if options.get("edge") is not None:
            edge: Edge = options.get("edge")
        else: 
            options.update({
                "vertice_a": self, 
                "vertice_b": vertice, 
                "weight": options.get("weight", 1),
                "direction": options.get("direction", -1)
            })
            
            edge: Edge = Edge(self.manager, options)
        
        self.connections.append({
            "vertice": vertice, 
            "weight": options.get("weight", 1), # 1 = "adjacent", 2 = "one-way", 3 = "bi-directional"
            "edge": edge
        })

        vertice.connections.append({
            "vertice": self, 
            "weight": options.get("weight", 1), # 1 = "adjacent", 2 = "one-way", 3 = "bi-directional"
            "edge": edge
        })

    
    def disconnect(self, vertice):
        for connection in self.connections:
            if connection["vertice"] == vertice:
                self.connections.remove(connection)
    
    def __repr__(self):
        return f"""
        [
            Vertice({self.position.x}, {self.position.y}, {self.value}),
            {len(self.connections)} connections.
        ]"""
    
    