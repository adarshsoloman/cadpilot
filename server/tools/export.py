import os
from utils.freecad_path import find_freecad_python
from utils.script_runner import run_freecad_script

def export_model(params: dict) -> dict:
    fmt = params.get("format", "stl").lower()
    path = params.get("output_path")
    obj_name = params.get("object_name", "all")
    
    if not path:
        return {"success": False, "error": "output_path is required"}
        
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    
    python_python = find_freecad_python()
    escaped_path = path.replace("\\", "\\\\")
    
    script = f"import Mesh, Part, Import\n"
    if obj_name == "all":
        script += "objs = doc.Objects\n"
    else:
        script += f"objs = [doc.getObject('{obj_name}')]\n"
        
    script += "if not any(objs): print('Error: No objects found to export')\nelse:\n"
    
    if fmt == "stl":
        script += f"    Mesh.export(objs, r'{escaped_path}')\n"
    elif fmt == "step":
        script += f"    Part.export(objs, r'{escaped_path}')\n"
    elif fmt == "fcstd":
        script += f"    doc.saveAs(r'{escaped_path}')\n"
    else:
        return {"success": False, "error": f"Unsupported format: {fmt}"}
        
    return run_freecad_script(script, python_python)
