import os
from utils.freecad_path import find_freecad_python
from utils.script_runner import run_freecad_script

def create_primitive(params: dict) -> dict:
    shape = params.get("shape", "box").lower()
    name = params.get("name", f"Primitive_{shape}")
    dims = params.get("dimensions", {})
    pos = params.get("position", {"x": 0, "y": 0, "z": 0})
    
    python_python = find_freecad_python()
    
    script = f"import Part, FreeCAD\n"
    
    if shape == "box":
        l = dims.get("length", 10)
        w = dims.get("width", 10)
        h = dims.get("height", 10)
        script += f"obj = doc.addObject('Part::Box', '{name}')\n"
        script += f"obj.Length = {l}\nobj.Width = {w}\nobj.Height = {h}\n"
    elif shape == "cylinder":
        r = dims.get("radius", 5)
        h = dims.get("height", 10)
        script += f"obj = doc.addObject('Part::Cylinder', '{name}')\n"
        script += f"obj.Radius = {r}\nobj.Height = {h}\n"
    elif shape == "sphere":
        r = dims.get("radius", 5)
        script += f"obj = doc.addObject('Part::Sphere', '{name}')\n"
        script += f"obj.Radius = {r}\n"
    elif shape == "cone":
        r1 = dims.get("radius1", 5)
        r2 = dims.get("radius2", 0)
        h = dims.get("height", 10)
        script += f"obj = doc.addObject('Part::Cone', '{name}')\n"
        script += f"obj.Radius1 = {r1}\nobj.Radius2 = {r2}\nobj.Height = {h}\n"
    elif shape == "torus":
        r1 = dims.get("radius1", 10)
        r2 = dims.get("radius2", 2)
        script += f"obj = doc.addObject('Part::Torus', '{name}')\n"
        script += f"obj.Radius1 = {r1}\nobj.Radius2 = {r2}\n"
    else:
        return {"success": False, "error": f"Unsupported shape: {shape}"}
        
    # Set position
    script += f"obj.Placement.Base = FreeCAD.Vector({pos.get('x',0)}, {pos.get('y',0)}, {pos.get('z',0)})\n"
    
    return run_freecad_script(script, python_python)
