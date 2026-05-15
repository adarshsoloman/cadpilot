# scripts/final_step2_bumper.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

code = '''
import FreeCAD, Part

# Command 2: Rubber Bumper Ring
bumper = doc.addObject("Part::Torus", "Bumper")
bumper.Radius1 = 500
bumper.Radius2 = 25
bumper.Placement.Base = FreeCAD.Vector(0, 0, 170)

# Set Color: Matte Black (0.08, 0.08, 0.08)
try:
    bumper.ViewObject.ShapeColor = (0.08, 0.08, 0.08)
    bumper.ViewObject.Visibility = True
except:
    pass

doc.recompute()
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
