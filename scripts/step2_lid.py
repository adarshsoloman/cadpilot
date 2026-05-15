# scripts/step2_lid.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

# Step 2: Tapered Lid (Loft)
# Find the face with the highest Z
code = '''
import FreeCAD, Part, math

# Find the top face of MainHull
hull_obj = doc.getObject("MainHull")
top_face = None
max_z = -1e9

for f in hull_obj.Shape.Faces:
    if f.CenterOfMass.z > max_z:
        max_z = f.CenterOfMass.z
        top_face = f

if top_face:
    # Create circular sketch at Z=400 (top of hull)
    circle_radius = 450
    offset_height = 60
    
    # Create a circle at the top center
    circle = Part.makeCircle(circle_radius, FreeCAD.Vector(0,0,400 + offset_height))
    circle_wire = Part.Wire(circle)
    
    # Loft the top face to the circle wire
    loft = Part.makeLoft([top_face.OuterWire, circle_wire], True)
    lid_obj = doc.addObject("Part::Feature", "RainGuard")
    lid_obj.Shape = loft
    
    # Set Color: International Orange
    try:
        lid_obj.ViewObject.ShapeColor = (1.0, 0.3, 0.0)
    except Exception:
        pass
else:
    print("Error: Could not find top face")
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
