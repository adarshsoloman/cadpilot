# scripts/step5_branding.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

# Step 5: Branding (ShapeString + Pocket)
code = '''
import FreeCAD, Part
import Draft

# Create ShapeString
font_path = "C:/Windows/Fonts/arialbd.ttf"
text_height = 40
text_content = "VYASN IOT-SN491"

# Create the string object
# Draft.makeShapeString(String, FontFile, Height, LSpace)
sh_str = Draft.makeShapeString(text_content, font_path, text_height)

# Move and rotate to the side of the hull
# Hull radius is 500. We put it at X=500
sh_str.Placement.Base = FreeCAD.Vector(501, -150, 200) # Slightly outside
sh_str.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,0,1), 90) * FreeCAD.Rotation(FreeCAD.Vector(1,0,0), 90)

# Extrude text slightly to perform cut
text_face = sh_str.Shape
text_vol = text_face.extrude(FreeCAD.Vector(-10, 0, 0)) # Extrude into the hull

# Subtract from MainHull
hull = doc.getObject("MainHull")
new_hull = hull.Shape.cut(text_vol)
hull.Shape = new_hull

doc.removeObject(sh_str.Name)
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
