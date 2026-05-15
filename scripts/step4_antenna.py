# scripts/step4_antenna.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

# Step 4: Antenna Array
code = '''
import FreeCAD, Part

# Pedestal
base_r = 35
base_h = 50
pedestal = Part.makeCylinder(base_r, base_h, FreeCAD.Vector(0,0,460))
ped_obj = doc.addObject("Part::Feature", "AntennaPedestal")
ped_obj.Shape = pedestal

# Whip
whip_r = 10
whip_h = 600
whip = Part.makeCylinder(whip_r, whip_h, FreeCAD.Vector(0,0,460 + base_h))
whip_obj = doc.addObject("Part::Feature", "AntennaWhip")
whip_obj.Shape = whip

# Set Color: Matte Black (0.1, 0.1, 0.1)
try:
    ped_obj.ViewObject.ShapeColor = (0.1, 0.1, 0.1)
    whip_obj.ViewObject.ShapeColor = (0.1, 0.1, 0.1)
except Exception:
    pass
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
