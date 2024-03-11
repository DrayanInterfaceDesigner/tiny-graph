import re

code = """
    P1(0,0) <-> P2(0,10) 
    P2(0,0) <-> P3(0,10) 
    P2(0,0) <-> P4(0,10) 
    P4(0,0) <-> P3(0,10) 
"""

class Parser:
    def __init__(self) -> None:
        pass

    def extract_signal(self, code: str) -> list:
        matches = "".join(re.findall(r'(?:<->|<-|<|-|>|->)', code))
        return matches

    def extract_variables(self, code: str) -> list:
        return re.findall(r'P\d+', code)
        
    def extract_coords(self, code: str) -> list:
        return re.findall(r'\(.*?\)', code)

    def extract_lines(self, code: str) -> list:
        regex: str = r'^\s*P\d+\([-+]?\d+,\s*[-+]?\d+\)(?:\s*(?:<->|->|<-|-)\s*P\d+\([-+]?\d+,\s*[-+]?\d+\))?\s*$'
        matches = re.findall(regex, code, re.MULTILINE)

        res: str = []
        for match in matches:
            res.append(match.strip())

        return res

    def map_signal(self, signal: str) -> int:
        if signal == "-": return 1
        elif signal == "<-" or signal == "->": return 2
        else: return 3

    def parse(self, code: str) -> dict:
        lines: list = self.extract_lines(code)
        res: dict = {'singletons': [], 'expressions': []}

        for line in lines:
            signal:str = self.extract_signal(line)
            variables: list = self.extract_variables(line)
            coords: list = self.extract_coords(line)
            mapped_signal: int = self.map_signal(signal)
            print(line, signal, mapped_signal)

            if not signal and len(variables) == 2: continue
            if not variables: continue
            # if len(variables) != 2: continue
            if not coords: continue
            if len(coords) != 2 and len(variables) == 2: continue

            tuple_coords: list = [tuple(x.replace('(', "").replace(')', "").split(',')) for x in coords]
            coords = [tuple(map(float, x)) for x in tuple_coords]
            res['expressions'].append({
                "signal": mapped_signal,
                "connections": variables,
                "coords": coords
            })

        for expression in res['expressions']:
            for variable in expression['connections']:
                if variable not in res['singletons']:
                    res['singletons'].append(variable)
        return res

# p = Parser()
# print(p.parse(code))
    

# pattern = r'^\s*P\d+\([-+]?\d+,\s*[-+]?\d+\)(?:\s*(?:<->|->|<-|-)\s*P\d+\([-+]?\d+,\s*[-+]?\d+\))?\s*$'

# lines = """
#     P1(-40,-40) -> P2(40,-40)
#     P2(40,-40)  <- P3(-40,40)
#     P3(-40,40)  <-> P4(40, 40)
#     P5(0,0) - P6(0, 10)
#     P7(0, 10)
# """

# matches = re.findall(pattern, lines, re.MULTILINE)
# for match in matches:
#     print(match.strip())