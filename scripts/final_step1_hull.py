# scripts/final_step1_hull.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python
from utils.session_manager import get_session_file, reset_session

# Reset session to start fresh
reset_session(get_session_file())

python_path = find_freecad_python()

code = '''
import FreeCAD, Part

# Vertices
p1 = FreeCAD.Vector(0, 0, 0)
p2 = FreeCAD.Vector(480, 0, 0)
p3 = FreeCAD.Vector(500, 0, 40)
p4 = FreeCAD.Vector(500, 0, 300)
p5 = FreeCAD.Vector(480, 0, 340)
p6 = FreeCAD.Vector(0, 0, 340)
p7 = FreeCAD.Vector(0, 0, 0)

# Create segments
l1 = Part.LineSegment(p1, p2)
l2 = Part.LineSegment(p2, p3)
l3 = Part.LineSegment(p3, p4)
l4 = Part.LineSegment(p4, p5)
l5 = Part.LineSegment(p5, p6)
l6 = Part.LineSegment(p6, p7)

wire = Part.Wire([l1.toShape(), l2.toShape(), l3.toShape(), l4.toShape(), l5.toShape(), l6.toShape()])

# Revolve 360 around Z-axis
revolve_shape = wire.revolve(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1))

hull = doc.addObject("Part::Feature", "Hull")
hull.Shape = revolve_shape

# Set Color: International Orange (1.0, 0.3, 0.0)
try:
    hull.ViewObject.ShapeColor = (1.0, 0.3, 0.0)
    hull.ViewObject.Visibility = True
except:
    pass

doc.recompute()
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
