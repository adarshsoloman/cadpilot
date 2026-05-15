# scripts/final_step5_branding.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

code = '''
import FreeCAD, Part, Draft

# Command 5: Branding Nameplate

# Step A: Nameplate box
nameplate = doc.addObject("Part::Box", "Nameplate")
nameplate.Length = 320
nameplate.Width = 8
nameplate.Height = 70
nameplate.Placement.Base = FreeCAD.Vector(-160, 497, 135)

# Step B: Text Shape
font_path = "C:/Windows/Fonts/arial.ttf"
# If arial.ttf doesn't exist, Draft often falls back or errors.
# We'll use Draft.makeShapeString
sh_str = Draft.makeShapeString("VYASN IOT-SN491", font_path, 42)
sh_str.Placement.Base = FreeCAD.Vector(-155, 496, 149)
sh_str.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,0,1), 0) # Adjust if needed

# Extrude raised lettering
text_face = sh_str.Shape
text_extrude = text_face.extrude(FreeCAD.Vector(0, 4, 0)) # Extrude in +Y
brand_text = doc.addObject("Part::Feature", "BrandText")
brand_text.Shape = text_extrude

doc.removeObject(sh_str.Name)

# Colors
try:
    nameplate.ViewObject.ShapeColor = (1.0, 1.0, 1.0)
    nameplate.ViewObject.Visibility = True
    brand_text.ViewObject.ShapeColor = (0.0, 0.0, 0.0)
    brand_text.ViewObject.Visibility = True
except: pass

doc.recompute()
# Save as requested
doc.saveAs(r"D:/ADARSH/vyasn_mark1_final.FCStd")
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
