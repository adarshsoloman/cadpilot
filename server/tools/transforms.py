from utils.freecad_path import find_freecad_python
from utils.script_runner import run_freecad_script

def transform_object(params: dict) -> dict:
    obj_name = params.get("object_name")
    op = params.get("operation", "move").lower()
    vals = params.get("values", {})
    
    if not obj_name:
        return {"success": False, "error": "object_name is required"}
        
    python_python = find_freecad_python()
    
    script = f"import FreeCAD\nobj = doc.getObject('{obj_name}')\nif obj:\n"
    
    if op == "move":
        x = vals.get("x", 0)
        y = vals.get("y", 0)
        z = vals.get("z", 0)
        script += f"    obj.Placement.Base += FreeCAD.Vector({x}, {y}, {z})\n"
    elif op == "rotate":
        ax = vals.get("axis_x", 0)
        ay = vals.get("axis_y", 0)
        az = vals.get("axis_z", 1)
        angle = vals.get("angle", 0)
        script += f"    obj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({ax}, {ay}, {az}), {angle})\n"
    elif op == "scale":
        # Note: Part objects don't always have a simple scale property, 
        # but some do or we use Draft.scale if available.
        # For simplicity in v1.0, we'll try to use a common method if it exists
        s = vals.get("factor", 1.0)
        script += f"    if hasattr(obj, 'Scale'): obj.Scale = {s}\n"
    else:
        return {"success": False, "error": f"Unsupported transform: {op}"}
    
    script += "else:\n    print(f'Error: Object {obj_name} not found')\n"
    
    return run_freecad_script(script, python_python)
