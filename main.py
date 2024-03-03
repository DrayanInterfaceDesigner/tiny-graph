import pyglet
import cairo
from lib.graphics import Screen
from lib.graphics.objects import Manager
from lib.graphics.shapes import Vertice
from lib.maths.Vector2 import Vector2
from lib.graphics.text import Label
import random
from lib.tools.compiler import Compiler
from lib.tools.parser import Parser

manager: Manager = Manager()
compiler: Compiler = Compiler({"color_steps": [(0,0, 255),(255,0,0)]})
screen: Screen = Screen(manager, {"window_size": (1380, 720)})

net:list = compiler.compile(manager, """
     P1(-40,-40) -> P2(40,-40)
     P2(40,-40)  <- P3(-40,40)
     P3(-40,40)  <-> P4(40, 40)
     P5(-190,0) - P5(-190,0)
     P5(-190,0) - P6(-40, 160)
     P7(0, -180)
""")


screen.start()