# scripts/final_step4_solar.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

code = '''
import FreeCAD, Part

# Command 4: Angled Solar Array

# Step A: Mounting arms
arm1 = doc.addObject("Part::Cylinder", "SolarArm1")
arm1.Radius = 12
arm1.Height = 180
arm1.Placement.Base = FreeCAD.Vector(0, 0, 430)
arm1.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90)

arm2 = doc.addObject("Part::Cylinder", "SolarArm2")
arm2.Radius = 12
arm2.Height = 180
arm2.Placement.Base = FreeCAD.Vector(0, 0, 430)
arm2.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -90)

# Step B: Solar panels
panel1 = doc.addObject("Part::Box", "SolarPanel1")
panel1.Length = 380
panel1.Width = 260
panel1.Height = 12
panel1.Placement.Base = FreeCAD.Vector(-190, 30, 415)
panel1.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -30)

panel2 = doc.addObject("Part::Box", "SolarPanel2")
panel2.Length = 380
panel2.Width = 260
panel2.Height = 12
panel2.Placement.Base = FreeCAD.Vector(-190, -290, 415)
panel2.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 30)

# Colors
for arm in [arm1, arm2]:
    try:
        arm.ViewObject.ShapeColor = (0.95, 0.95, 0.95)
        arm.ViewObject.Visibility = True
    except: pass

for panel in [panel1, panel2]:
    try:
        panel.ViewObject.ShapeColor = (0.03, 0.03, 0.35)
        panel.ViewObject.Visibility = True
    except: pass

doc.recompute()
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
