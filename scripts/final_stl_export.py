# scripts/final_stl_export.py
import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), 'server'))
from utils.script_runner import run_freecad_script
from utils.freecad_path import find_freecad_python

python_path = find_freecad_python()

code = '''
import Mesh
# Export everything to STL
objs = doc.Objects
Mesh.export(objs, r"D:/ADARSH/vyasn_mark1_final.stl")
'''

result = run_freecad_script(code, python_path)
print(json.dumps(result))
