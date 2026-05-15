# scripts/update_mast_v2.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

code = '''
import FreeCAD, Part

# Objects to delete
to_delete = [
    "Leg1", "Leg2", "Leg3", "MastBase", "TopRing", 
    "SolarArm1", "SolarArm2", "SolarPanel1", "SolarPanel2", 
    "BrandText", "Nameplate"
]

for name in to_delete:
    obj = doc.getObject(name)
    if obj:
        doc.removeObject(name)

# 1. MastBase cylinder
mb = doc.addObject("Part::Cylinder", "MastBase")
mb.Radius = 65
mb.Height = 80
mb.Placement.Base = FreeCAD.Vector(0, 0, 340)

# 2. CenterMast cylinder
cm = doc.addObject("Part::Cylinder", "CenterMast")
cm.Radius = 40
cm.Height = 650
cm.Placement.Base = FreeCAD.Vector(0, 0, 420)

# 3. Three legs
# Leg 1
l1 = doc.addObject("Part::Cylinder", "Leg1")
l1.Radius = 18
l1.Height = 600
l1.Placement.Base = FreeCAD.Vector(160, 0, 340)
l1.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,1,0), 18)

# Leg 2
l2 = doc.addObject("Part::Cylinder", "Leg2")
l2.Radius = 18
l2.Height = 600
l2.Placement.Base = FreeCAD.Vector(-80, 138, 340)
l2.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(-0.866,-0.5,0), 18)

# Leg 3
l3 = doc.addObject("Part::Cylinder", "Leg3")
l3.Radius = 18
l3.Height = 600
l3.Placement.Base = FreeCAD.Vector(-80, -138, 340)
l3.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(-0.866,0.5,0), 18)

# 4. TopRing torus
tr = doc.addObject("Part::Torus", "TopRing")
tr.Radius1 = 130
tr.Radius2 = 14
tr.Placement.Base = FreeCAD.Vector(0, 0, 1000)

# Visibility and Colors
for obj in [mb, cm, l1, l2, l3, tr]:
    try:
        obj.ViewObject.ShapeColor = (0.9, 0.9, 0.9)
        obj.ViewObject.Visibility = True
    except:
        pass

doc.recompute()
# Update the STL and FCStd files
doc.saveAs(r"D:/ADARSH/vyasn_mark1_final.FCStd")
import Mesh
Mesh.export(doc.Objects, r"D:/ADARSH/vyasn_mark1_final.stl")
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
