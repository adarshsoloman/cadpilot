# scripts/buoy_v2_step1.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python
from utils.session_manager import get_session_file, reset_session

# Start fresh for v2
reset_session(get_session_file())

python_path = find_freecad_python()

code = '''
import FreeCAD, Part, math

# Command 1: Main Industrial Hull
radius = 500
height = 400
points = []
for i in range(13):
    angle = math.radians(i * 30)
    points.append(FreeCAD.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))

wire = Part.makePolygon(points)
face = Part.Face(wire)
hull_shape = face.extrude(FreeCAD.Vector(0,0,height))
hull_obj = doc.addObject("Part::Feature", "MainHull_v2")
hull_obj.Shape = hull_shape

# Force Visibility and Color
try:
    hull_obj.ViewObject.ShapeColor = (1.0, 0.3, 0.0)
    hull_obj.ViewObject.Visibility = True
except:
    pass

# Command 2: The Tapered Lid
# Circle at Z=460 (400 hull + 60 offset)
circle_radius = 450
lid_top_z = 400 + 60
circle = Part.makeCircle(circle_radius, FreeCAD.Vector(0,0,lid_top_z))
circle_wire = Part.Wire(circle)

# Find top face (Z=400)
top_wire = None
for f in hull_obj.Shape.Faces:
    if abs(f.CenterOfMass.z - 400) < 0.1:
        top_wire = f.OuterWire
        break

if top_wire:
    lid_shape = Part.makeLoft([top_wire, circle_wire], True)
    lid_obj = doc.addObject("Part::Feature", "Lid_v2")
    lid_obj.Shape = lid_shape
    try:
        lid_obj.ViewObject.ShapeColor = (1.0, 0.3, 0.0)
        lid_obj.ViewObject.Visibility = True
    except:
        pass
else:
    print("Error: Could not find top face at Z=400")
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
