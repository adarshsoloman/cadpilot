# scripts/test_connection.py
import subprocess
import os
import sys
from dotenv import load_dotenv

# Add server directory to path to use utilities
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "server"))
from utils.freecad_path import find_freecad_python

load_dotenv()

FREECAD_PYTHON = os.getenv(
    "FREECAD_PYTHON_PATH",
    find_freecad_python()
)

print(f"Using FreeCAD Python: {FREECAD_PYTHON}")

TEST_SCRIPT = """
import FreeCAD
import Part
print("FreeCAD version:", FreeCAD.Version())
doc = FreeCAD.newDocument("TestDoc")
box = doc.addObject("Part::Box", "TestBox")
box.Length = 50
box.Width = 50
box.Height = 50
doc.recompute()
print("Test box created successfully")
print("Objects in document:", [obj.Name for obj in doc.Objects])
"""

try:
    result = subprocess.run(
        [FREECAD_PYTHON, "-c", TEST_SCRIPT],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        print("SUCCESS — FreeCAD connection working")
        print("STDOUT:")
        print(result.stdout)
    else:
        print("FAILED — Error executing FreeCAD script")
        print("STDERR:")
        print(result.stderr)
except Exception as e:
    print(f"FAILED — {str(e)}")
