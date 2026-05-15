# scripts/build_buoy_hull.py
import sys
import os

# Add server directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "server"))

from tools.primitives import create_primitive
from tools.export import export_model
from utils.session_manager import get_session_file, reset_session

def main():
    print("Building VYASN Mark 1 Hull...")
    
    # 1. Start fresh
    reset_session(get_session_file())
    
    # 2. Create base cylinder
    print("- Creating cylinder (r:100, h:200)")
    create_primitive({
        "shape": "cylinder",
        "name": "HullBase",
        "dimensions": {"radius": 100, "height": 200},
        "position": {"x": 0, "y": 0, "z": 0}
    })
    
    # 3. Create box on top (Centering 50x50 box on top of 100 radius cylinder)
    print("- Creating box (50x50x50) at Z=200")
    create_primitive({
        "shape": "box",
        "name": "HullTop",
        "dimensions": {"length": 50, "width": 50, "height": 50},
        "position": {"x": -25, "y": -25, "z": 200}
    })
    
    # 4. Export to STL
    print(f"- Exporting to D:/ADARSH/vyasn_test.stl")
    export_model({
        "format": "stl",
        "output_path": "D:/ADARSH/vyasn_test.stl",
        "object_name": "all"
    })
    
    print("SUCCESS: VYASN Mark 1 Hull built and exported.")

if __name__ == "__main__":
    main()
