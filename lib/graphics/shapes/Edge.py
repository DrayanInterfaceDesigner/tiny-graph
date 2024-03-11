from lib.graphics.shapes import Object
from lib.graphics.objects import Manager
from lib.graphics.shapes import Vertice
from lib.maths.Vector2 import Vector2
import math 
import random

class Edge(Object):

    DRAW_SIGNIFICANTLY_CHANGES_ONLY = True

    def __init__(self, manager: Manager, options: dict = {}, consts:dict = {}) -> None:
        options['layer'] = options.get('layer', -1)
        super().__init__(manager, options)
        self.vertice_a: Vertice = options.get("vertice_a", None)
        self.vertice_b: Vertice = options.get("vertice_b", None)
        self.vertices: list = [self.vertice_a, self.vertice_b]
        
        self.color: tuple = options.get("color", (255, 255, 255))
        self.stroke_thickness: int = options.get("stroke_thickness", 1)
        self.direction: int = options.get("direction", 1)
        self.weight: int = options.get("weight", 1)
        self.radius: int = options.get("radius", 20)
        self.self_connection_rotation: float = 3.14 * random.uniform(0, 2)
        self.draw_significantly_changes_only = consts.get("draw_significantly_changes_only", False)
        if self.draw_significantly_changes_only:
            self.vertices_cache:dict = {
            "v_a_origin": self.vertice_a.original_position.copy(),
            "v_b_origin": self.vertice_b.original_position.copy()
        }
        self.draw_method: list = []
        self.infer_direction()
    
    def DRAW_METHOD_SELF_CONNECTION(self, ctx):
        ctx.save()
        ctx.translate(self.vertice_a.position.x, self.vertice_a.position.y)
        ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
        ctx.set_line_width(self.stroke_thickness + self.stroke_thickness * (1 + self.weight))
        ctx.rotate(self.self_connection_rotation)
        ctx.arc(0, -self.vertice_a.radius, self.vertice_a.radius, 0, 2 * 3.14)
        ctx.stroke() 
        ctx.restore()
    
    def DRAW_METHOD_DIRECTIONAL(self, ctx):
        ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
        ctx.move_to(self.vertice_a.position.x, self.vertice_a.position.y)
        ctx.line_to(self.vertice_b.position.x, self.vertice_b.position.y)
        ctx.set_line_width(self.stroke_thickness)
        ctx.stroke()
        self.directional_triangle(ctx)

    def DRAW_METHOD_BIDIRECTIONAL(self, ctx):
        ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
        ctx.move_to(self.vertice_a.position.x, self.vertice_a.position.y)
        ctx.line_to(self.vertice_b.position.x, self.vertice_b.position.y)
        ctx.set_line_width(self.stroke_thickness)
        ctx.stroke()
        self.prisma(ctx)
        
    def DRAW_METHOD_FLAT(self, ctx):
        ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
        ctx.move_to(self.vertice_a.position.x, self.vertice_a.position.y)
        ctx.line_to(self.vertice_b.position.x, self.vertice_b.position.y)
        ctx.set_line_width(self.stroke_thickness)
        ctx.stroke()
    
    def infer_direction(self):
        # print(self.direction)
        if self.vertice_a == self.vertice_b:
            self.draw_method.append(self.DRAW_METHOD_SELF_CONNECTION)
        
        if self.direction == 1:
            self.draw_method.append(self.DRAW_METHOD_FLAT)
        elif self.direction == 2:
            self.draw_method.append(self.DRAW_METHOD_DIRECTIONAL)
        elif self.direction == 3:
            self.draw_method.append(self.DRAW_METHOD_BIDIRECTIONAL)
        else:
            is_reciprocal = len([connection['vertice'] == self.vertice_a for connection in self.vertice_b.connections]) > 0
            if is_reciprocal:
                self.draw_method.append(self.DRAW_METHOD_BIDIRECTIONAL)
            else:
                self.draw_method.append(self.DRAW_METHOD_DIRECTIONAL)
        
    

        # # they connect to each other
        # if any(connection['vertice'] == self.vertice_a for connection in self.vertice_b.connections):
        #     conn = next((connection for connection in self.vertice_b.connections if connection['vertice'] == self.vertice_a), None)
        #     if self.weight == conn['weight']:
        #         self.draw_method.append(self.DRAW_METHOD_DIRECTIONAL)
                
        #     else:
        #         self.draw_method.append(self.DRAW_METHOD_BIDIRECTIONAL)
        #         return 2
        # else:
        #     self.draw_method.append(self.DRAW_METHOD_FLAT)
            
    def is_connected_with(self, vertice: Vertice):
        return vertice in self.vertices
    
    def origin_positions_changed(self) -> bool:
        if self.vertices_cache["v_a_origin"] != self.vertice_a.original_position:
            self.vertices_cache["v_a_origin"] = self.vertice_a.original_position
            return True
        elif self.vertices_cache["v_b_origin"] != self.vertice_b.original_position:
            self.vertices_cache["v_b_origin"] = self.vertice_b.original_position
            return True
        return False
        
    def directional_triangle(self, ctx, origin:Vertice = None, target:Vertice=None):
        origin = self.vertice_a if origin is None else origin
        target = self.vertice_b if target is None else target
        
        mid_x = (self.vertice_a.position.x + self.vertice_b.position.x) / 2
        mid_y = (self.vertice_a.position.y + self.vertice_b.position.y) / 2

        ctx.save()
        ctx.translate(mid_x, mid_y)
        ctx.rotate((origin.position.point_to(target.position) + 3.14/2))
        ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
        ctx.move_to(0, -10) 
        ctx.line_to(10, 10)
        ctx.line_to(-10, 10) 
        ctx.close_path()

        ctx.fill()
        ctx.restore()
        
    def prisma(self, ctx):
        mid_x = (self.vertice_a.position.x + self.vertice_b.position.x) / 2
        mid_y = (self.vertice_a.position.y + self.vertice_b.position.y) / 2

        ctx.save()
        ctx.translate(mid_x, mid_y)
        ctx.rotate(self.vertice_a.position.point_to(self.vertice_b.position))
        ctx.set_source_rgb(self.color[0]/255, self.color[1]/255, self.color[2]/255)
        ctx.move_to(-10, 0)
        ctx.line_to(0, -10)
        ctx.line_to(10, 0)
        ctx.line_to(0, 10)
        ctx.close_path()
        ctx.fill()

        ctx.restore()


    def draw(self, ctx):
        for draw_method in self.draw_method:
            draw_method(ctx)
    
    def update(self, dt):
        pass