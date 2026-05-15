# scripts/add_solar_v2.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

code = '''
import FreeCAD, Part

# Step A: Mounting arms
arm1 = doc.addObject("Part::Cylinder", "SolarArm1")
arm1.Radius = 14
arm1.Height = 220
arm1.Placement.Base = FreeCAD.Vector(0, 0, 680)
arm1.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90)

arm2 = doc.addObject("Part::Cylinder", "SolarArm2")
arm2.Radius = 14
arm2.Height = 220
arm2.Placement.Base = FreeCAD.Vector(0, 0, 680)
arm2.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -90)

# Step B: Solar panels
panel1 = doc.addObject("Part::Box", "SolarPanel1")
panel1.Length = 400
panel1.Width = 15
panel1.Height = 280
panel1.Placement.Base = FreeCAD.Vector(-200, 60, 620)
panel1.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -25)

panel2 = doc.addObject("Part::Box", "SolarPanel2")
panel2.Length = 400
panel2.Width = 15
panel2.Height = 280
panel2.Placement.Base = FreeCAD.Vector(-200, -340, 620)
panel2.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 25)

# Colors and Visibility
for arm in [arm1, arm2]:
    try:
        arm.ViewObject.ShapeColor = (0.9, 0.9, 0.9)
        arm.ViewObject.Visibility = True
    except: pass

for panel in [panel1, panel2]:
    try:
        panel.ViewObject.ShapeColor = (0.02, 0.02, 0.3)
        panel.ViewObject.Visibility = True
    except: pass

doc.recompute()
# Update the STL and FCStd files
doc.saveAs(r"D:/ADARSH/vyasn_mark1_final.FCStd")
import Mesh
Mesh.export(doc.Objects, r"D:/ADARSH/vyasn_mark1_final.stl")
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
