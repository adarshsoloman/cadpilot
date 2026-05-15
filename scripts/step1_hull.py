# scripts/step1_hull.py
import sys
import os
import json

# Add server directory to path
sys.path.append(os.path.join(os.getcwd(), 'server'))

from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python
from utils.session_manager import get_session_file, reset_session

# Reset session for a new industrial build
reset_session(get_session_file())

python_path = find_freecad_python()

# Step 1: Create Dodecagon Hull
code = '''
import FreeCAD, Part, math
# The preamble handles doc creation/loading

# Create a regular 12-sided polygon
radius = 500
height = 400
points = []
for i in range(13):
    angle = math.radians(i * 30)
    points.append(FreeCAD.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))

wire = Part.makePolygon(points)
face = Part.Face(wire)
hull = face.extrude(FreeCAD.Vector(0,0,height))
obj = doc.addObject("Part::Feature", "MainHull")
obj.Shape = hull

# Set Color: International Orange (1.0, 0.3, 0.0)
# In headless mode ViewObject might not be accessible but we attempt it
try:
    obj.ViewObject.ShapeColor = (1.0, 0.3, 0.0)
except Exception:
    pass
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
