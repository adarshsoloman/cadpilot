import os
import winreg

COMMON_FREECAD_PATHS = [
    r"C:\Program Files\FreeCAD 1.1\bin\FreeCAD.exe",
    r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe",
    r"C:\Program Files\FreeCAD 0.22\bin\FreeCAD.exe",
    r"C:\Program Files\FreeCAD 0.21\bin\FreeCAD.exe",
    r"C:\Program Files\FreeCAD 0.20\bin\FreeCAD.exe",
    r"C:\Program Files (x86)\FreeCAD 0.21\bin\FreeCAD.exe",
]

def find_freecad_executable():
    """Attempts to find the FreeCAD executable on Windows."""
    # Check environment variable first
    env_path = os.getenv("FREECAD_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    
    # Check common paths
    for path in COMMON_FREECAD_PATHS:
        if os.path.exists(path):
            return path
            
    # Try registry (optional but helpful)
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\FreeCAD") as key:
            # This is a bit speculative as FreeCAD might not always register here
            # but it's a good fallback if we knew the key structure.
            pass
    except WindowsError:
        pass

    raise FileNotFoundError(
        "FreeCAD not found. Please install FreeCAD 0.21+ or set FREECAD_PATH in .env"
    )

def find_freecad_python():
    """FreeCAD ships its own Python on Windows. This finds it."""
    # Check environment variable first
    env_python = os.getenv("FREECAD_PYTHON_PATH")
    if env_python and os.path.exists(env_python):
        return env_python

    try:
        freecad_exe = find_freecad_executable()
        freecad_dir = os.path.dirname(os.path.dirname(freecad_exe))
        python_path = os.path.join(freecad_dir, "bin", "python.exe")
        
        if os.path.exists(python_path):
            return python_path
    except FileNotFoundError:
        pass
        
    return "python" # Fallback to system python, though unlikely to work for FreeCAD API
