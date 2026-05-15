# examples/buoy_hull.py
# This script simulates the VYASN buoy hull creation using the MCP tools
# Note: This is a standalone script for testing, not the actual MCP server.

import sys
import os

# Add server to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "server"))

from tools.primitives import create_primitive
from tools.transforms import transform_object
from tools.export import export_model
from utils.session_manager import get_session_file, reset_session

def build_buoy():
    print("Starting VYASN Buoy build simulation...")
    
    # 1. Reset Session
    reset_session(get_session_file())
    
    # 2. Create Hull (Base Box for now, hex later)
    print("Creating hull...")
    create_primitive({
        "shape": "box",
        "name": "BuoyHull",
        "dimensions": {"length": 150, "width": 150, "height": 100},
        "position": {"x": -75, "y": -75, "z": 0}
    })
    
    # 3. Create Antenna
    print("Creating antenna...")
    create_primitive({
        "shape": "cylinder",
        "name": "Antenna",
        "dimensions": {"radius": 5, "height": 150},
        "position": {"x": 0, "y": 0, "z": 100}
    })
    
    # 4. Export
    print("Exporting...")
    export_model({
        "format": "stl",
        "output_path": "examples/vyasn_buoy.stl"
    })
    
    print("Build complete. File saved to examples/vyasn_buoy.stl")

if __name__ == "__main__":
    build_buoy()
