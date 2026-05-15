# scripts/final_step3_mast.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

code = '''
import FreeCAD, Part, math

# Command 3: Tripod Mast Structure

# Step A: Central mast base
mast_base = doc.addObject("Part::Cylinder", "MastBase")
mast_base.Radius = 60
mast_base.Height = 60
mast_base.Placement.Base = FreeCAD.Vector(0, 0, 340)

# Step B: Three support legs
# Leg 1
leg1 = doc.addObject("Part::Cylinder", "Leg1")
leg1.Radius = 15
leg1.Height = 260
leg1.Placement.Base = FreeCAD.Vector(140, 0, 340)
leg1.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,1,0), 15)

# Leg 2
leg2 = doc.addObject("Part::Cylinder", "Leg2")
leg2.Radius = 15
leg2.Height = 260
leg2.Placement.Base = FreeCAD.Vector(-70, 121, 340)
leg2.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0.866, 0.5, 0), 15)

# Leg 3
leg3 = doc.addObject("Part::Cylinder", "Leg3")
leg3.Radius = 15
leg3.Height = 260
leg3.Placement.Base = FreeCAD.Vector(-70, -121, 340)
leg3.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0.866, -0.5, 0), 15)

# Step C: Top ring
top_ring = doc.addObject("Part::Torus", "TopRing")
top_ring.Radius1 = 120
top_ring.Radius2 = 12
top_ring.Placement.Base = FreeCAD.Vector(0, 0, 590)

# Colors
for obj in [mast_base, leg1, leg2, leg3, top_ring]:
    try:
        obj.ViewObject.ShapeColor = (0.95, 0.95, 0.95)
        obj.ViewObject.Visibility = True
    except:
        pass

doc.recompute()
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
