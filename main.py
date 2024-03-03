import pyglet
import cairo
from lib.graphics import Screen, Screen_GPU_ACCEL_EXPERIMENTAL
from lib.graphics.objects import Manager
from lib.graphics.shapes import Vertice
from lib.maths.Vector2 import Vector2
from lib.graphics.text import Label
import random
from lib.tools.compiler import Compiler
from lib.tools.parser import Parser

manager: Manager = Manager()
compiler: Compiler = Compiler({"color_steps": [(0,0, 255),(255,0,0)]})
# screen: Screen = Screen(manager, {"window_size": (1380, 720)})
gpu_screen: Screen = Screen_GPU_ACCEL_EXPERIMENTAL(manager, {"window_size": (1380, 720)})

net:list = compiler.compile(manager, """
     P1(-40,-40) -> P2(40,-40)
     P2(40,-40)  <- P3(-40,40)
     P3(-40,40)  <-> P4(40, 40)
     P5(-190,0) - P5(-190,0)
     P5(-190,0) - P6(-40, 160)
     P7(0, -180)
""")

gpu_screen.start()
# screen.start()










# vertices: list = []
# for x in range(0, 100):
#      vertice = Vertice(manager, { "radius": 13, "position": Vector2(
#      (random.randrange(-20, 90)  * x),
#      (random.randrange(-20, 90)  * x)
#      ), "color": (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))})
#      vertices.append(vertice)

# for vertice in vertices:
#     for other_vertice in vertices[1:]:
#         vertice.connect(other_vertice, {"color": (66,66,66)})