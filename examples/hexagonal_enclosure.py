# examples/hexagonal_enclosure.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "server"))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

def create_hex():
    python_python = find_freecad_python()
    
    # Hexagonal prism logic
    code = """
import FreeCAD, Part, math
def make_hex(radius, height, name):
    points = []
    for i in range(7):
        angle = math.radians(i * 60)
        points.append(FreeCAD.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))
    
    wire = Part.makePolygon(points)
    face = Part.Face(wire)
    extrude = face.extrude(FreeCAD.Vector(0,0,height))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = extrude
    return obj

make_hex(100, 200, "HexBody")
"""
    print("Executing raw FreeCAD Python for hexagonal enclosure...")
    result = run_freecad_script(code, python_python)
    if result["success"]:
        print("Success! HexBody created in session.")
    else:
        print("Error:", result.get("stderr"))

if __name__ == "__main__":
    create_hex()
