import os
import sys

# Add server directory to sys.path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
server_dir = os.path.join(project_root, "server")
sys.path.append(server_dir)

from tools.primitives import create_primitive
from tools.boolean_ops import boolean_operation
from tools.export import export_model

def main():
    print("Building model...")
    
    # 1. Create a box 10x10x10
    print("- Creating box...")
    res = create_primitive({
        "shape": "box",
        "name": "MyBox",
        "dimensions": {"length": 10, "width": 10, "height": 10}
    })
    if not res["success"]:
        print(f"Error creating box: {res.get('error', res.get('stderr'))}")
        return

    # 2. Create a sphere radius 5
    # Positioned at (5, 5, 5) to be in the center of the box if we want, 
    # but the prompt didn't specify position. Let's put it at (5,5,5) for a nice hole.
    # Actually, prompt says: "a box of size 10x10x10, then a sphere of radius 5, then subtract"
    # Default position is (0,0,0).
    print("- Creating sphere...")
    res = create_primitive({
        "shape": "sphere",
        "name": "MySphere",
        "dimensions": {"radius": 5},
        "position": {"x": 5, "y": 5, "z": 5}
    })
    if not res["success"]:
        print(f"Error creating sphere: {res.get('error', res.get('stderr'))}")
        return

    # 3. Subtract sphere from box
    print("- Subtracting sphere from box...")
    res = boolean_operation({
        "operation": "cut",
        "base_object": "MyBox",
        "tool_object": "MySphere"
    })
    if not res["success"]:
        print(f"Error in subtraction: {res.get('error', res.get('stderr'))}")
        return

    # 4. Export to STL
    print("- Exporting to STL...")
    # The result of the cut is named 'Cut_MyBox_MySphere' by boolean_operation.py
    stl_path = os.path.join(project_root, "mcp_test.stl")
    res = export_model({
        "format": "stl",
        "output_path": stl_path,
        "object_name": "Cut_MyBox_MySphere"
    })
    if not res["success"]:
        print(f"Error exporting STL: {res.get('error', res.get('stderr'))}")
        return

    print(f"Success! Model exported to {stl_path}")

if __name__ == "__main__":
    main()
