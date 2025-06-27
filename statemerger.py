import re, os

class State:
    def __init__(self):
        self.mp = 0
        self.provinces = []

        self.aluminium = 0
        self.chromium = 0
        self.oil = 0
        self.rubber = 0
        self.steel = 0
        self.tungsten = 0

        self.vps = []
        self.navalBases = []

    def compile(self, newid):
        out = ""
        out += "state={\n"
        out += f'id={newid}\n'
        out += f'name="STATE_{newid}"\n'
        out += f'manpower={self.mp}\n\n'

        out += f'state_category = town\n'
        out += "resources = {\n"
        out += f'aluminium = {self.aluminium}\n'
        out += f'chromium = {self.chromium}\n'
        out += f'oil = {self.oil}\n'
        out += f'rubber = {self.rubber}\n'
        out += f'steel = {self.steel}\n'
        out += f'tungsten = {self.tungsten}\n'
        out += "}\n\n"

        out += "history = {\n"
        for v in self.vps:
            out += "victory_points = {" + v + "}\n"
        out += "owner = AAA\nadd_core_of = AAA\n"
        out += """
buildings = {
    infrastructure = 3
    arms_factory = 1
    industrial_complex = 1
"""
        for n in self.navalBases:
            out += str(n)+" = {naval_base = 1}\n"
        out += "}\n}\n\n"

        out += "provinces = {" + " ".join(self.provinces) + "}\n"
        out += "local_supplies = 1.0\n"
        out += "}"

        return out

def getValueFromLine(s:str):
    x = s.strip()[s.strip().index("=")+1:].strip() # I hate Python
    if x.isnumeric():
        x = int(x)
    return x

def merge(ids:list, newid):
    newState = State()
    for i in ids:
        with open(f"./history/states/{i}.txt") as statefile:
            for line in statefile:
                # match list of provinces
                if re.match(r"^\s*(\d* )+$", line, re.M):
                    newState.provinces.extend(line.strip().split())

                # victorypoints
                elif "victory_points" in line:
                    point = getValueFromLine(line)[1:-1]
                    newState.vps.append(point)

                # naval bases
                elif re.match(r"^\s*\d+ = {$", line, re.M):
                    base = line.replace("= {", "").strip()
                    newState.navalBases.append(base)

                elif "manpower" in line:
                    newState.mp = getValueFromLine(line)
                elif "aluminum" in line:
                    newState.aluminum = getValueFromLine(line)
                elif "chromium" in line:
                    newState.chromium = getValueFromLine(line)
                elif "oil" in line:
                    newState.oil = getValueFromLine(line)
                elif "rubber" in line:
                    newState.rubber = getValueFromLine(line)
                elif "steel" in line:
                    newState.steel = getValueFromLine(line)
                elif "tungsten" in line:
                    newState.tungsten = getValueFromLine(line)
        os.remove(f"./history/states/{i}.txt")

    with open(f"./history/states/{newid}.txt", "w") as f:
        f.write(newState.compile(newid))
    with open("statemerger/states.txt", "a") as sl:
        for i in ids:
            sl.write(f"{i}\n")


STATES = input("state ids: (use spaces to seperate) ").split()
NEW = input("new id: ")
merge(STATES, NEW)