from lib.graphics.shapes import Object
from lib.graphics.objects import Manager
from lib.graphics.shapes import Vertice
from lib.maths.Vector2 import Vector2
import math 
import random

class Edge(Object):
    def __init__(self, manager: Manager, options: dict = {}) -> None:
        options['layer'] = options.get('layer', -1)
        super().__init__(manager, options)
        self.vertice_a: Vertice = options.get("vertice_a", None)
        self.vertice_b: Vertice = options.get("vertice_b", None)
        self.color: tuple = options.get("color", (255, 255, 255))
        self.stroke_thickness: int = options.get("stroke_thickness", 1)
        self.direction: int = options.get("direction", 1)
        self.weight: int = options.get("weight", 1)
        self.radius: int = options.get("radius", 20)
        self.self_connection_rotation: float = 3.14 * random.uniform(0, 2)
        self.draw_method: list = []
        self.infer_direction()
    
    def infer_direction(self):

        if self.vertice_a == self.vertice_b:
            def draw(self, ctx):
                ctx.save()
                ctx.translate(self.vertice_a.position.x, self.vertice_a.position.y)
                ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
                ctx.set_line_width(self.stroke_thickness + self.stroke_thickness * (1 + self.weight))
                ctx.rotate(self.self_connection_rotation)
                ctx.arc(0, -self.vertice_a.radius, self.vertice_a.radius, 0, 2 * 3.14)
                ctx.stroke() 
                ctx.restore()
            self.draw_method.append(draw)

        # they connect to each other
        if any(connection['vertice'] == self.vertice_a for connection in self.vertice_b.connections):
            conn = next((connection for connection in self.vertice_b.connections if connection['vertice'] == self.vertice_a), None)
            if self.weight == conn['weight']:
                def draw(self, ctx):
                    ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
                    ctx.move_to(self.vertice_a.position.x, self.vertice_a.position.y)
                    ctx.line_to(self.vertice_b.position.x, self.vertice_b.position.y)
                    ctx.set_line_width(self.stroke_thickness)
                    ctx.stroke()
                    self.directional_triangle(ctx)
                self.draw_method.append(draw)
                
            else:
                # Create a new edge with an offset from the other edge.
                # if they have different weights and are connected
                return 2
        else:
            def draw(self, ctx):
                ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
                ctx.move_to(self.vertice_a.position.x, self.vertice_a.position.y)
                ctx.line_to(self.vertice_b.position.x, self.vertice_b.position.y)
                ctx.set_line_width(self.stroke_thickness)
                ctx.stroke()
            self.draw_method.append(draw)
            
    def directional_triangle(self, ctx):
        mid_x = (self.vertice_a.position.x + self.vertice_b.position.x) / 2
        mid_y = (self.vertice_a.position.y + self.vertice_b.position.y) / 2

        ctx.save()
        ctx.translate(mid_x, mid_y)
        ctx.rotate((self.vertice_a.position.point_to(self.vertice_b.position) + 3.14/2))
        ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
        ctx.move_to(0, -10) 
        ctx.line_to(10, 10)
        ctx.line_to(-10, 10) 
        ctx.close_path()

        ctx.fill()
        ctx.restore()
        

    def draw(self, ctx):
        
        for draw_method in self.draw_method:
            draw_method(self, ctx)
    
    def update(self, dt):
        pass