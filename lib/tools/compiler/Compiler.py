from lib.graphics.shapes.Edge import Edge
from lib.graphics.shapes.Vertice import Vertice
from lib.graphics.objects.Manager import Manager
from lib.maths.Vector2 import Vector2
from lib.tools.parser.Parser import Parser
from lib.graphics.artistic.colors import *

class Compiler:
    def __init__(self, options:dict={}) -> None:
        self.net:list = []
        self.built_singletons_counter: int = 0
        self.max_expected_singletons: int = None
        self.color_steps:list = options.get("color_steps", [(0,0, 255), (255,0,0)])
        self.colors_length: int = len(self.color_steps)
        
    def all_singleton_appearances(self, singleton:str, expressions:list) -> Vertice:
        found:list = []
        for expression in expressions:
            if singleton in expression["connections"]:
                found.append(expression)
        return found
    
    def last_singleton_appearance(self, singleton:str, expressions:list) -> Vertice:
        appearances:list = self.all_singleton_appearances(singleton, expressions)
        return appearances[-1] if appearances else None
    
    def find_singleton(self, singleton:str) -> Vertice:
        for s in self.net:
            if s.tag == singleton:
                return s
        return None
    
    def build_singleton(self, manager: Manager, singleton:str, expressions:list) -> Vertice:
        last_singleton: dict = self.last_singleton_appearance(singleton, expressions)
        last_singleton_index: int = last_singleton["connections"].index(singleton)
        last_singleton_position: Vector2 = Vector2(
            last_singleton["coords"][last_singleton_index][0],
            last_singleton["coords"][last_singleton_index][1]
        )

        vertice: Vertice = Vertice(manager, {
            "tag": singleton,
            "position": last_singleton_position, 
            "radius": 20, 
            "color": (
                lerp_colors(self.color_steps, self.built_singletons_counter/self.max_expected_singletons)
            ), 
            "font_size": 12, 
            "label": singleton
        })
        self.built_singletons_counter += 1

        self.net.append(vertice)

        return vertice

    def connect_singleton(self, singleton:str, expressions: list) -> None:
        all_appearances: list = self.all_singleton_appearances(singleton, expressions)
        _singleton: Vertice = self.find_singleton(singleton)
        for appearance in all_appearances:
            if len(appearance['connections']) <= 1: continue
            other_singleton:str = appearance["connections"][0] if appearance["connections"][0] != singleton else appearance["connections"][1]
            other_singleton_instance: Vertice = self.find_singleton(other_singleton)

            _singleton.connect(other_singleton_instance, {
                "color": (66,66,66),
                "direction": appearance["signal"],
            })

    def compile(self, manager: Manager, code: str) -> list:
        parser:Parser = Parser()
        parsed_code:dict = parser.parse(code)
        self.max_expected_singletons = len(parsed_code["singletons"])

        for singleton in parsed_code["singletons"]:
            self.build_singleton(manager, singleton, parsed_code["expressions"])
        
        for singleton in parsed_code["singletons"]:
            self.connect_singleton(singleton, parsed_code["expressions"])
        
        print(self.net)
        return self.net