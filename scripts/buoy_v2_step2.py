# scripts/buoy_v2_step2.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

code = '''
import FreeCAD, Part, Draft

# Command 3: Solar Trays
lid = doc.getObject("Lid_v2")
tray_l = 450
tray_w = 320
tray_d = 25

# Create cut tools
tool1 = Part.makeBox(tray_l, tray_w, tray_d)
tool1.translate(FreeCAD.Vector(-tray_l/2, 50, 460 - tray_d + 5))

tool2 = Part.makeBox(tray_l, tray_w, tray_d)
tool2.translate(FreeCAD.Vector(-tray_l/2, -tray_w - 50, 460 - tray_d + 5))

# Apply cut to lid
lid.Shape = lid.Shape.cut(tool1).cut(tool2)

# Command 4: Antenna Stack
ped_r = 35
ped_h = 50
pedestal = Part.makeCylinder(ped_r, ped_h, FreeCAD.Vector(0,0,460))
ped_obj = doc.addObject("Part::Feature", "AntennaPedestal_v2")
ped_obj.Shape = pedestal

whip_r = 10
whip_h = 600
whip = Part.makeCylinder(whip_r, whip_h, FreeCAD.Vector(0,0,460 + ped_h))
whip_obj = doc.addObject("Part::Feature", "AntennaWhip_v2")
whip_obj.Shape = whip

try:
    ped_obj.ViewObject.ShapeColor = (0.1, 0.1, 0.1)
    ped_obj.ViewObject.Visibility = True
    whip_obj.ViewObject.ShapeColor = (0.1, 0.1, 0.1)
    whip_obj.ViewObject.Visibility = True
except:
    pass

# Command 5: Branding
font_path = "C:/Windows/Fonts/arialbd.ttf"
text_h = 45
sh_str = Draft.makeShapeString("VYASN IOT-SN491", font_path, text_h)

# Align to facet (centered on 400mm height)
# Facet is at radius 500, height 400. Center at Z=200
sh_str.Placement.Base = FreeCAD.Vector(501, -160, 200 - (text_h/2))
sh_str.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,0,1), 90) * FreeCAD.Rotation(FreeCAD.Vector(1,0,0), 90)

# Pocket (depth 5mm)
text_vol = sh_str.Shape.extrude(FreeCAD.Vector(-10, 0, 0))
hull = doc.getObject("MainHull_v2")
hull.Shape = hull.Shape.cut(text_vol)

doc.removeObject(sh_str.Name)

# Save Final
doc.saveAs(r"D:/ADARSH/VYASN_Industrial_v2_Final.FCStd")
import Mesh
Mesh.export(doc.Objects, r"D:/ADARSH/VYASN_Industrial_v2_Final.stl")
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
