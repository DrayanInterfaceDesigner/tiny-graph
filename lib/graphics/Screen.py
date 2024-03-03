import pyglet
import cairo
from lib.graphics.objects import Manager
from lib.maths import Vector2

class Screen:
    def __init__(self, manager: Manager, options:dict = {}) -> None:
        self.options = options
        self.window_size = self.options.get("window_size", (400, 300))
        self.window = pyglet.window.Window(
            width=self.window_size[0], height=self.window_size[1])
        self.manager: Manager = manager
        self.scale = 1
        self.allow_zoom = False
        self.mouse_pos = (0, 0)
        self.dragging = False
        self.translation = (0, 0)
        self.last_translation = (0, 0)
        self.window.push_handlers(self.on_draw)
        self.window.push_handlers(self.on_mouse_scroll)
        self.window.push_handlers(self.on_mouse_press)
        self.window.push_handlers(self.on_mouse_drag)
        self.window.push_handlers(self.on_mouse_release)


    def surface(self):
        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, 
            self.window_size[0], 
            self.window_size[1]
        )
        ctx = cairo.Context(surface)
        return ctx
    
    def update(self, dt):
        self.manager.update(dt)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        scale:float = (scroll_y * 0.1)

        _ = self.scale + scale
        self.scale = max(0.2, min(_, 6))

        if self.scale > .2 and self.scale < 3:
            self.allow_zoom = True
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT: 
            self.dragging = True
            self.mouse_pos = (x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging:
            self.translation = (self.translation[0] + dx, self.translation[1] + dy)
            self.mouse_pos = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.dragging = False
    
    def on_draw(self):

        self.window.clear()
        ctx = self.surface()
        
        tx = self.window_size[0]/2 + self.translation[0] 
        ty = self.window_size[1]/2 + -self.translation[1]
        ctx.translate(tx, ty)

        ctx.save()

        if self.allow_zoom:
            ctx.scale(self.scale, self.scale)

        self.manager.draw(ctx)
        ctx.restore()

        img = pyglet.image.ImageData(
            self.window_size[0], 
            self.window_size[1], 
            'RGBA', 
            ctx.get_target().get_data(), 
            pitch=-self.window_size[0]*4
        )
        img.blit(0, 0)

    def start(self):
        pyglet.clock.schedule_interval(self.update, 1/60) 
        pyglet.app.run()
    