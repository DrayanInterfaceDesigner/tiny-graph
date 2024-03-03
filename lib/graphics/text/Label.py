from lib.graphics.shapes import Object
from lib.maths.Vector2 import Vector2, VEC_ZERO 
import cairo

class Label(Object):
    def __init__(self, manager, options):
        options['layer'] = options.get('layer', 1)
        super().__init__(manager, options)

        self.label:str = options.get("label", "")
        self.font:str = options.get("font", "Arial")
        self.font_size:int = options.get("font_size", 12)
        self.font_weight:int = options.get("font_weight", cairo.FONT_WEIGHT_BOLD)
        self.font_color: tuple = options.get("font_color", (255, 255, 255))
        self.font_offset: Vector2 = options.get("font_offset", VEC_ZERO)
        self.background_padding: tuple = options.get("background_padding", (0,0))
        self.label_background: tuple = options.get("label_background", None)
        self.label_background_color: tuple = options.get("label_background_color", (255, 255, 255))

    def draw_background(self, ctx):
        characters_size_factor: int = len(self.label) * self.font_size
        if self.label_background is not None:
            ctx.set_source_rgb(
                self.label_background_color[0]/255, 
                self.label_background_color[1]/255, 
                self.label_background_color[2]/255
            )
            ctx.rectangle(self.position.x - characters_size_factor / 4, 
                          self.position.y - self.font_size, 
                          characters_size_factor + (self.background_padding[0] * 2), 
                          self.font_size + (self.background_padding[1] * 2)
                        )
            ctx.fill()

    def draw(self, ctx):
        self.draw_background(ctx)
        ctx.set_source_rgb(self.font_color[0]/255, self.font_color[1]/255, self.font_color[2]/255)
        ctx.select_font_face(self.font, cairo.FONT_SLANT_NORMAL, self.font_weight)
        ctx.set_font_size(self.font_size)
        ctx.move_to(self.position.x + self.font_offset.x, self.position.y + self.font_offset.y)
        ctx.show_text(self.label)

    def update(self, dt):
        pass