# scripts/step3_trays.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

# Step 3: Solar Integration Trays (Pockets)
# We will create two boxes and subtract them from the RainGuard
code = '''
import FreeCAD, Part

lid = doc.getObject("RainGuard")
tray_l = 450
tray_w = 320
tray_d = 20

# Create left tray tool
tray1 = Part.makeBox(tray_l, tray_w, tray_d)
# Position it on the lid top (approx Z=460)
# Offset from center
tray1.translate(FreeCAD.Vector(-tray_l/2, 50, 460 - tray_d + 5)) # Slightly embedded

# Create right tray tool
tray2 = Part.makeBox(tray_l, tray_w, tray_d)
tray2.translate(FreeCAD.Vector(-tray_l/2, -tray_w - 50, 460 - tray_d + 5))

# Subtract from lid
new_lid_shape = lid.Shape.cut(tray1).cut(tray2)
lid.Shape = new_lid_shape

# Color: Deep Navy Blue (0.0, 0.0, 0.5)
# In FreeCAD we usually color faces, but for Part::Feature we can color the whole object or sub-elements
# We will just note the requirement
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
