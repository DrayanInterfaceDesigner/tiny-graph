from lib.graphics.shapes import Object
from lib.maths.Vector2 import Vector2, VEC_ZERO 
import cairo

class Label(Object):
    def __init__(self, manager, options):
        options['layer'] = options.get('layer', 1)
        super().__init__(manager, options)

        self.target: Object = options.get("target", VEC_ZERO)
        self.is_target_object: bool = isinstance(self.target, Object)
        self.position: Vector2 = self.target.position if self.is_target_object else self.target

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
        width:float = ((characters_size_factor / 1.66) * 2)
        height:float = (self.font_size)/1.33
        if self.label_background is not None:
            ctx.set_source_rgb(
                self.label_background_color[0]/255, 
                self.label_background_color[1]/255, 
                self.label_background_color[2]/255
            )
            ctx.rectangle((self.position.x) - width/4, 
                          (self.position.y) - height, 
                          width, 
                          height
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
        self.position = self.target.position if isinstance(self.target, Object) else self.target
        if self.is_target_object:
            if self.target.marked_for_removal:
                self.manager.remove(self)