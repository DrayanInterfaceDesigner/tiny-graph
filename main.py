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
from pyglet.gl import *

manager: Manager = Manager()
compiler: Compiler = Compiler({"color_steps": [(0,0, 255),(255,0,0)]})
# screen: Screen = Screen(manager, {"window_size": (1380, 720)})
gpu_screen: Screen = Screen_GPU_ACCEL_EXPERIMENTAL(manager, {"window_size": (1380, 720)})

net:list = compiler.compile(manager, """
     
     1 Neuronio camada 1 conectado a 4 neuronios camada 2
     P1(-200, -30) - P21(-100, -90)
     P1(-200, -30) - P22(-100, -30)
     P1(-200, -30) - P23(-100,  30)
     P1(-200, -30) - P24(-100,  90)
     P1(-200, -30) - P1(-200, -30)
     
     1 Neuronio camada 1 conectado a 4 neuronios camada 2                     
     P2(-200, 30) - P21(-100, -90)
     P2(-200, 30) - P22(-100, -30)
     P2(-200, 30) - P23(-100,  30)
     P2(-200, 30) - P24(-100,  90) 

     4 Neuronios camada 2 conectados a 4 neuronios camada 3
     P21(-100, -90) - P31(0, -90)
     P21(-100, -90) - P32(0, -90)
     P21(-100, -90) - P33(0, -90)
     P21(-100, -90) - P34(0, -90)

     P22(-100, -30) -> P32(0, -30)
     P23(-100,  30) -> P33(0,  30)
     P24(-100,  90) -> P34(0,  90)
                            
     P31(0, -90) -> P41(100, -90)
     P32(0, -30) -> P42(100, -30)
     P33(0,  30) -> P43(100,  30)
     P34(0,  90) -> P44(100,  90)
                            
     P41(100, -90) -> P5(200, 0)
     P42(100, -30) -> P5(200, 0)
     P43(100,  30) -> P5(200, 0)
     P44(100,  90) -> P5(200, 0)
""")


gpu_screen.start()
# screen.start()









# vertices: list = []
# for x in range(0, 100000):
#      vertice = Vertice(manager, { "radius": 13, "position": Vector2(
#      (random.randrange(-20, 90)  * x),
#      (random.randrange(-20, 90)  * x)
#      ), "color": (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))})
#      vertices.append(vertice)

# for vertice in vertices[1:]:
#      vertice.connect(vertices[0], {"color": (66,66,66)})
# print(vertices)

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