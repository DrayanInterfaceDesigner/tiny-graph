import pyglet
import cairo
from pyglet.gl import *
import numpy as np
from lib.graphics.objects import Manager
from lib.maths.Vector2 import Vector2
from lib.graphics.shapes import Vertice
import ctypes
from lib.graphics.shapes import Edge

class Screen(pyglet.window.Window):
    def __init__(self, manager: Manager, options: dict = {}) -> None:
        self.options = options
        self.window_size = self.options.get("window_size", (400, 300))
        super().__init__(width=self.window_size[0], height=self.window_size[1])
        self.manager: Manager = manager
        self.scale:int = 1
        self.allow_zoom:bool = False
        self.mouse_pos:tuple = (0, 0)
        self.dragging:bool = False
        self.translation:tuple = (0, 0)
        self.last_translation:tuple = (0, 0)
        self.update_interval:float = 1 / 60
        self.set_handlers()

    def set_handlers(self):
        self.event_handlers = {
            "on_draw": self.on_draw,
            "on_mouse_scroll": self.on_mouse_scroll,
            "on_mouse_press": self.on_mouse_press,
            "on_mouse_drag": self.on_mouse_drag,
            "on_mouse_release": self.on_mouse_release
        }
        # for event, handler in self.event_handlers.items():
        #     self.push_handlers(getattr(self, event))

    def surface(self):
        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self.width,
            self.height
        )
        ctx = cairo.Context(surface)
        return ctx

    def update(self, dt):
        self.manager.update(dt)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        scale = scroll_y * 0.1
        new_scale = self.scale + scale
        self.scale = max(0.05, min(new_scale, 6))
        if 0.2 < self.scale < 3:
            self.allow_zoom = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.MIDDLE:
            self.dragging = True
            self.mouse_pos = (x, y)
        if button == pyglet.window.mouse.LEFT:
            mouse_pos:Vector2 = Vector2(((x - self.window_size[0] / 2) / self.scale) , ((y - self.window_size[1] / 2) * -1) / self.scale)
            print(mouse_pos)
            for obj in self.manager.objects:
                if isinstance(obj, Vertice):
                    if obj.position.distance(mouse_pos) < obj.radius:
                        connections: list = [connection['edge'] for connection in obj.connections]
                        print(obj.tag)
                        for connection in connections:
                            for vertice in connection.vertices:
                                vertice.disconnect(obj)
                            self.manager.remove(connection)
                        self.manager.remove(obj)
                        break
        if button == pyglet.window.mouse.RIGHT:
            print("RIGGT CLICK")

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging:
            self.translation = (self.translation[0] + dx, self.translation[1] + dy)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.MIDDLE:
            self.dragging = False

    def on_draw(self):
        self.clear()
        ctx = self.surface()
        tx = self.width / 2 + self.translation[0]
        ty = self.height / 2 - self.translation[1]
        ctx.translate(tx, ty)
        ctx.save()
        if self.allow_zoom:
            ctx.scale(self.scale, self.scale)
        self.manager.draw(ctx)
        ctx.restore()
        
        img = pyglet.image.ImageData(
            self.width,
            self.height,
            'RGBA',
            ctx.get_target().get_data(),
            pitch=-self.width * 4
        )
        img.blit(0, 0)

    def start(self):
        pyglet.clock.schedule_interval(self.update, self.update_interval)
        pyglet.app.run()


class Screen_GPU_ACCEL_EXPERIMENTAL(pyglet.window.Window):
    def __init__(self, manager: Manager, options: dict = {}) -> None:
        """WARNING: This class is experimental and may not work as expected.
        And most important, before accusing us, YES this class had a lot of
        help from Generative Models. We're just having fun here, please
        don't get overreact. We're just trying to make the world a better place.

        """
        
        self.options = options
        self.window_size = self.options.get("window_size", (400, 300))
        super().__init__(width=self.window_size[0], height=self.window_size[1])
        self.manager: Manager = manager
        self.scale:int = 1
        self.allow_zoom:bool = False
        self.mouse_pos:tuple = (0, 0)
        self.dragging:bool = False
        self.translation:tuple = (0, 0)
        self.last_translation:tuple = (0, 0)
        self.update_interval:float = 1 / 60
        self.set_handlers()
        self.setup_opengl()

    def set_handlers(self):
        self.event_handlers = {
            "on_draw": self.on_draw,
            "on_mouse_scroll": self.on_mouse_scroll,
            "on_mouse_press": self.on_mouse_press,
            "on_mouse_drag": self.on_mouse_drag,
            "on_mouse_release": self.on_mouse_release
        }
        # for event, handler in self.event_handlers.items():
        #     self.push_handlers(getattr(self, event))

    def setup_opengl(self):
        glClearColor(0, 0, 0, 1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # compiling the shaders
        self.shader_program = self.compile_shaders()

        # vertex to simple quads
        self.vertices = np.array([-1, -1, 1, -1, 1, 1, -1, 1], dtype=np.float32)
        self.tex_coords = np.array([0, 1, 1, 1, 1, 0, 0, 0], dtype=np.float32)

        # self.vertices and self.tex_coords to ctypes arrays
        vertices_array = (ctypes.c_float * len(self.vertices))(*self.vertices)
        tex_coords_array = (ctypes.c_float * len(self.tex_coords))(*self.tex_coords)

        # vertex buffer objects vbos and vao
        self.vbo_vertices = GLuint()
        glGenBuffers(1, self.vbo_vertices)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_vertices)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(vertices_array), vertices_array, GL_STATIC_DRAW)

        self.vbo_tex_coords = GLuint()
        glGenBuffers(1, self.vbo_tex_coords)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_tex_coords)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(tex_coords_array), tex_coords_array, GL_STATIC_DRAW)

        self.vao = GLuint()
        glGenVertexArrays(1, self.vao)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_vertices)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_tex_coords)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def compile_shaders(self):
        vertex_shader_source = """
        #version 330 core
        layout(location = 0) in vec2 position;
        layout(location = 1) in vec2 tex_coord;
        out vec2 v_tex_coord;
        void main()
        {
            gl_Position = vec4(position, 0.0, 1.0);
            v_tex_coord = tex_coord;
        }
        """
        fragment_shader_source = """
        #version 330 core
        in vec2 v_tex_coord;
        out vec4 frag_color;
        uniform sampler2D tex;
        void main()
        {
            frag_color = texture(tex, v_tex_coord);
        }
        """
        # compilign the vertex shader
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        
        # glShaderSource = _link_function('glShaderSource', None, [GLuint, GLsizei, POINTER(POINTER(GLchar)), POINTER(GLint)], requires='OpenGL 2.0')
        # source to c_char_p
        source = ctypes.c_char_p(vertex_shader_source.encode('utf-8'))
        length = ctypes.c_int(len(vertex_shader_source))

        # getting pointers
        source_array = (ctypes.POINTER(ctypes.c_char) * 1)()
        source_array[0] = ctypes.cast(source, ctypes.POINTER(ctypes.c_char))

        glShaderSource(vertex_shader, 1, source_array, ctypes.byref(length))
        glCompileShader(vertex_shader)

        # compiling fragment shader
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)

        # source code to ctypes c_char_p and get its length
        source = ctypes.c_char_p(fragment_shader_source.encode('utf-8'))
        length = ctypes.c_int(len(fragment_shader_source))

        # get pointers 
        source_array = (ctypes.POINTER(ctypes.c_char) * 1)()
        source_array[0] = ctypes.cast(source, ctypes.POINTER(ctypes.c_char))

        glShaderSource(fragment_shader, 1, source_array, ctypes.byref(length))
        glCompileShader(fragment_shader)

        # creating the program and linking the shaders
        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)

        # deleting the shaderes
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        return shader_program

    def update(self, dt):
        self.manager.update(dt)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        scale = scroll_y * 0.1
        new_scale = self.scale + scale
        self.scale = max(0.05, min(new_scale, 6))
        if 0.2 < self.scale < 3:
            self.allow_zoom = True

    def on_mouse_press(self, x, y, button, modifiers):
        mouse_pos:Vector2 = Vector2(
            ((x - self.window_size[0] / 2) / self.scale) - self.translation[0]/self.scale , 
            (((y - self.window_size[1] / 2) * -1) / self.scale) + self.translation[1]/self.scale
            )
        if button == pyglet.window.mouse.MIDDLE:
            self.dragging = True
            self.mouse_pos = (x, y)
        if button == pyglet.window.mouse.LEFT:
            print(mouse_pos)
            for obj in self.manager.objects:
                if isinstance(obj, Vertice):
                    if obj.position.distance(mouse_pos) < obj.radius:
                        connections: list = [connection['edge'] for connection in obj.connections]
                        print(obj.tag)
                        for connection in connections:
                            for vertice in connection.vertices:
                                vertice.disconnect(obj)
                            self.manager.remove(connection)
                        self.manager.remove(obj)
                        break
        if button == pyglet.window.mouse.RIGHT:
            for obj in self.manager.objects:
                if isinstance(obj, Vertice):
                    if obj.position.distance(mouse_pos) < obj.radius:
                        connections: list = [connection['edge'] for connection in obj.connections]
                        print(obj.tag)
                        for connection in connections:
                            connection.color = obj.color


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging:
            self.translation = (self.translation[0] + dx, self.translation[1] + dy)
            self.mouse_pos = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.dragging = False

    def surface(self):
        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self.width,
            self.height
        )
        ctx = cairo.Context(surface)
        return (surface, ctx)
    
    def on_draw(self):
        self.clear()
        glUseProgram(self.shader_program)
        glBindVertexArray(self.vao)

        surface, ctx = self.surface()

        # rendering process
        tx = self.width / 2 + self.translation[0]
        ty = self.height / 2 - self.translation[1]
        ctx.translate(tx, ty)
        ctx.save()
        if self.allow_zoom:
            ctx.scale(self.scale, self.scale)
        self.manager.draw(ctx)
        ctx.restore()
        
        # here we upload Cairo ctx data to OpenGL texture
        texture = GLuint()
        glGenTextures(1, ctypes.byref(texture))

        # ARGB to RGBA fuck cairo honestly
        img_data = surface.get_data()
        img_data_rgba = np.frombuffer(img_data, np.uint8).reshape((self.height, self.width, 4))
        img_data_rgba = img_data_rgba[..., [2, 1, 0, 3]].tobytes()

        # surface data to ctype
        data_arr = (ctypes.c_ubyte * len(img_data_rgba)).from_buffer_copy(img_data_rgba)

        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_BGRA, GL_UNSIGNED_BYTE, data_arr)

        glBindTexture(GL_TEXTURE_2D, texture)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

        glDeleteTextures(1, ctypes.byref(texture))

        glBindVertexArray(0)
        glUseProgram(0)

    def start(self):
        pyglet.clock.schedule_interval(self.update, self.update_interval)
        pyglet.app.run()
