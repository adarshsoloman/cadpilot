from utils.freecad_path import find_freecad_python
from utils.script_runner import run_freecad_script

def boolean_operation(params: dict) -> dict:
    op = params.get("operation", "union").lower()
    base_name = params.get("base_object")
    tool_name = params.get("tool_object")
    
    if not base_name or not tool_name:
        return {"success": False, "error": "Both base_object and tool_object are required"}
        
    python_python = find_freecad_python()
    
    script = f"""
import FreeCAD, Part
base = doc.getObject('{base_name}')
tool = doc.getObject('{tool_name}')
if not base or not tool:
    print(f"Error: Could not find objects {{'{base_name}' if not base else ''}} {{'{tool_name}' if not tool else ''}}")
else:
"""
    if op == "union":
        script += f"    fuse = doc.addObject('Part::Fuse', 'Union_{base_name}_{tool_name}')\n"
        script += f"    fuse.Base = base\n    fuse.Tool = tool\n"
    elif op == "cut":
        script += f"    cut = doc.addObject('Part::Cut', 'Cut_{base_name}_{tool_name}')\n"
        script += f"    cut.Base = base\n    cut.Tool = tool\n"
    elif op == "intersection":
        script += f"    inter = doc.addObject('Part::Common', 'Intersection_{base_name}_{tool_name}')\n"
        script += f"    inter.Base = base\n    inter.Tool = tool\n"
    else:
        return {"success": False, "error": f"Unsupported operation: {op}"}

    # Hide base and tool objects if GUI is available
    script += "    if hasattr(base, 'ViewObject') and base.ViewObject:\n"
    script += "        base.ViewObject.Visibility = False\n"
    script += "    if hasattr(tool, 'ViewObject') and tool.ViewObject:\n"
    script += "        tool.ViewObject.Visibility = False\n"
    
    return run_freecad_script(script, python_python)
