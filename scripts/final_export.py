# scripts/final_export.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

# Final Export and Save
code = '''
import Mesh, Part
# Save the document as requested
doc.saveAs(r"D:/ADARSH/VYASN_Industrial_Draft.FCStd")

# Export everything to STL
objs = doc.Objects
Mesh.export(objs, r"D:/ADARSH/VYASN_Industrial_Final.stl")
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
