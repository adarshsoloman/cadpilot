# FreeCAD MCP Server — Product Requirements Document

**Project Name:** FreeCAD MCP Server for VYASN  
**Version:** 1.0  
**Date:** May 2026  
**Author:** Adarsh Soloman Banjare, CTO — VYASN  
**Platform:** Windows  

---

## 1. PROJECT OVERVIEW

A Model Context Protocol (MCP) server that connects Gemini CLI (or any MCP-compatible AI) to FreeCAD on Windows. The server acts as a bridge — the AI describes what to build in natural language, the MCP server translates that into FreeCAD Python API commands, and the 3D model gets built automatically inside FreeCAD.

**Primary use case:** Describe the VYASN Mark 1 buoy from an image or text description and have FreeCAD build it automatically — without manually clicking through the FreeCAD UI.

---

## 2. THE PROBLEM

FreeCAD is powerful but manual. Building complex marine hardware enclosures requires:
- Opening FreeCAD manually
- Clicking through menus
- Writing Python scripts by hand
- Iterating slowly

This MCP server removes all of that. Describe the object → it gets built.

---

## 3. GOALS

- Connect Gemini CLI to FreeCAD via MCP protocol on Windows
- Allow natural language descriptions to produce working 3D models
- Support the VYASN buoy design iteration workflow
- Enable AI-assisted CAD without manual FreeCAD UI interaction
- Be buildable and testable in under 60 minutes

---

## 4. NON-GOALS

- Not a full parametric CAD system
- Not replacing FreeCAD — augmenting it
- Not cloud-based — runs locally on Windows
- Not supporting other CAD tools in v1.0

---

## 5. SYSTEM ARCHITECTURE

```
User (natural language description)
        ↓
Gemini CLI
        ↓
MCP Protocol (stdio JSON)
        ↓
FreeCAD MCP Server (Python)
        ↓
Session Manager (file-based state)
        ↓            ↑
   session.FCStd ←──┘  (persists between tool calls)
        ↓
FreeCAD Python API (subprocess)
        ↓
FreeCAD application (Windows)
        ↓
Output: .FCStd file / .STL export
```

**State Model:** Each tool call loads `session.FCStd` at the start and saves it on completion. This means sequential tool calls (e.g. create hull → add antenna → export) share the same persistent document across subprocess boundaries.

---

## 6. TECH STACK

| Component | Technology |
|-----------|-----------|
| MCP Server | Python 3.11+ |
| Package Manager | uv |
| AI Client | Gemini CLI |
| CAD Software | FreeCAD 0.21+ (Windows) |
| Protocol | MCP stdio (JSON) |
| CAD API | FreeCAD Python API |
| Config | .env + gemini_settings.json |
| Output formats | .FCStd, .STL, .STEP |

---

## 7. FILE STRUCTURE

```
freecad-mcp/
├── server/
│   ├── freecad_mcp_server.py      # Main MCP server
│   ├── tools/
│   │   ├── primitives.py          # Box, cylinder, sphere, cone
│   │   ├── boolean_ops.py         # Union, cut, intersection
│   │   ├── transforms.py          # Move, rotate, scale
│   │   ├── export.py              # STL, STEP, FCStd export
│   │   └── raw_executor.py        # Execute raw FreeCAD Python
│   └── utils/
│       ├── freecad_path.py        # Windows FreeCAD path resolver
│       ├── script_runner.py       # Subprocess manager with session wrapping
│       └── session_manager.py     # File-based session state manager
├── config/
│   ├── gemini_settings.json       # Gemini CLI MCP config
│   └── freecad_paths.json         # FreeCAD install paths
├── scripts/
│   └── test_connection.py         # Test FreeCAD connectivity
├── examples/
│   ├── buoy_hull.py               # VYASN buoy example script
│   └── hexagonal_enclosure.py     # Hexagonal body example
├── session/                       # Runtime session files (git-ignored)
│   └── .gitkeep
├── requirements.txt
└── README.md
```

---

## 8. MCP TOOLS SPECIFICATION

### Tool 1: create_primitive

Creates basic 3D shapes.

```json
{
  "tool": "create_primitive",
  "params": {
    "shape": "box | cylinder | sphere | cone | torus",
    "dimensions": {
      "length": 100,
      "width": 100,
      "height": 50,
      "radius": 30
    },
    "name": "BuoyHull",
    "position": { "x": 0, "y": 0, "z": 0 }
  }
}
```

### Tool 2: boolean_operation

Combines or subtracts shapes.

```json
{
  "tool": "boolean_operation",
  "params": {
    "operation": "union | cut | intersection",
    "base_object": "BuoyHull",
    "tool_object": "SolarTray"
  }
}
```

### Tool 3: transform_object

Moves, rotates, or scales objects.

```json
{
  "tool": "transform_object",
  "params": {
    "object_name": "Antenna",
    "operation": "move | rotate | scale",
    "values": { "x": 0, "y": 0, "z": 150 }
  }
}
```

### Tool 4: export_model

Exports the current document.

```json
{
  "tool": "export_model",
  "params": {
    "format": "stl | step | fcstd",
    "output_path": "C:/Users/Adarsh/vyasn_buoy.stl",
    "object_name": "all | specific_object_name"
  }
}
```

### Tool 5: execute_raw

Most powerful tool. Sends raw FreeCAD Python directly.

```json
{
  "tool": "execute_raw",
  "params": {
    "code": "import FreeCAD\nimport Part\ndoc = FreeCAD.newDocument()\n..."
  }
}
```

### Tool 6: list_objects

Returns all objects currently in the document.

```json
{
  "tool": "list_objects",
  "params": {}
}
```

### Tool 7: new_document

Creates a fresh FreeCAD document and resets the session file.

```json
{
  "tool": "new_document",
  "params": {
    "name": "VYASN_Mark1"
  }
}
```

### Tool 8: reset_session

Deletes the current session file, giving a clean slate. Use this before starting a completely new model build.

```json
{
  "tool": "reset_session",
  "params": {}
}
```

---

## 9. WINDOWS-SPECIFIC IMPLEMENTATION

### FreeCAD Path Resolution

FreeCAD on Windows requires finding the correct executable and Python interpreter:

```python
# freecad_path.py
import os
import winreg

COMMON_FREECAD_PATHS = [
    r"C:\Program Files\FreeCAD 0.21\bin\FreeCAD.exe",
    r"C:\Program Files\FreeCAD 0.20\bin\FreeCAD.exe",
    r"C:\Program Files (x86)\FreeCAD 0.21\bin\FreeCAD.exe",
]

def find_freecad_executable():
    for path in COMMON_FREECAD_PATHS:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "FreeCAD not found. Set FREECAD_PATH in .env"
    )

def find_freecad_python():
    """FreeCAD ships its own Python on Windows"""
    freecad_dir = os.path.dirname(
        os.path.dirname(find_freecad_executable())
    )
    python_path = os.path.join(freecad_dir, "bin", "python.exe")
    if os.path.exists(python_path):
        return python_path
    return "python"
```

### Session State Manager

Every tool call shares a persistent `.FCStd` document via file-based state. The session manager wraps all user code with a preamble (load session) and postamble (save session).

```python
# utils/session_manager.py
import os

def get_session_file() -> str:
    output_dir = os.getenv("OUTPUT_DIR", os.path.expanduser("~"))
    return os.path.join(output_dir, "session", "freecad_mcp_session.FCStd")

def build_session_preamble(session_file: str) -> str:
    """Load existing session doc or create a fresh one."""
    return f"""
import FreeCAD, Part, os
SESSION_FILE = r'{session_file}'
os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
if os.path.exists(SESSION_FILE):
    doc = FreeCAD.openDocument(SESSION_FILE)
else:
    doc = FreeCAD.newDocument('Session')
"""

def build_session_postamble(session_file: str) -> str:
    """Recompute and save the session doc after every tool call."""
    return f"""
doc.recompute()
doc.saveAs(r'{session_file}')
print("__SESSION_SAVED__")
"""

def reset_session(session_file: str) -> dict:
    """Delete the session file to start fresh."""
    if os.path.exists(session_file):
        os.remove(session_file)
        return {"success": True, "message": "Session reset. Next tool call starts a new document."}
    return {"success": True, "message": "No active session to reset."}
```

### Script Execution on Windows

Every script is now wrapped with session preamble and postamble before execution:

```python
# utils/script_runner.py
import subprocess
import tempfile
import os
from .session_manager import (
    get_session_file,
    build_session_preamble,
    build_session_postamble
)

def run_freecad_script(
    user_code: str,
    freecad_python_path: str,
    use_session: bool = True
) -> dict:
    session_file = get_session_file()

    if use_session:
        full_code = (
            build_session_preamble(session_file)
            + "\n" + user_code + "\n"
            + build_session_postamble(session_file)
        )
    else:
        full_code = user_code

    # Write full script to temp file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        delete=False,
        encoding='utf-8'
    ) as f:
        f.write(full_code)
        temp_path = f.name

    try:
        result = subprocess.run(
            [freecad_python_path, temp_path],
            capture_output=True,
            text=True,
            timeout=int(os.getenv("SCRIPT_TIMEOUT", 30)),
            env={
                **os.environ,
                "FREECAD_USER_HOME": os.path.expanduser("~")
            }
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "session_file": session_file,
            "returncode": result.returncode
        }
    finally:
        os.unlink(temp_path)
```

---

## 10. GEMINI CLI CONFIGURATION

Add to your Gemini CLI settings file (`gemini_settings.json`):

```json
{
  "mcpServers": {
    "freecad": {
      "command": "python",
      "args": ["C:/path/to/freecad-mcp/server/freecad_mcp_server.py"],
      "description": "Controls FreeCAD 3D modeling. Use this to create 3D models, shapes, and export files. Supports primitives, boolean operations, transforms, and raw FreeCAD Python execution.",
      "env": {
        "FREECAD_PATH": "C:/Program Files/FreeCAD 0.21/bin/FreeCAD.exe"
      }
    }
  }
}
```

---

## 11. MAIN SERVER IMPLEMENTATION

```python
# freecad_mcp_server.py
import sys
import json
import os
from dotenv import load_dotenv
from utils.freecad_path import find_freecad_python
from utils.script_runner import run_freecad_script
from utils.session_manager import get_session_file, reset_session
from tools.primitives import create_primitive
from tools.boolean_ops import boolean_operation
from tools.transforms import transform_object
from tools.export import export_model

load_dotenv()

FREECAD_PYTHON = os.getenv(
    "FREECAD_PYTHON_PATH",
    find_freecad_python()
)

def handle_new_document(params: dict) -> dict:
    """Reset session file, then create a named document."""
    reset_session(get_session_file())  # wipe old session first
    name = params.get('name', 'Document')
    return run_freecad_script(
        f"doc = FreeCAD.newDocument('{name}')",
        FREECAD_PYTHON,
        use_session=True
    )

TOOL_HANDLERS = {
    "create_primitive":  create_primitive,
    "boolean_operation": boolean_operation,
    "transform_object":  transform_object,
    "export_model":      export_model,
    "execute_raw": lambda p: run_freecad_script(
        p.get("code", ""), FREECAD_PYTHON, use_session=True
    ),
    "new_document":  handle_new_document,
    "list_objects": lambda p: run_freecad_script(
        "print([obj.Name for obj in doc.Objects])",
        FREECAD_PYTHON,
        use_session=True
    ),
    "reset_session": lambda p: reset_session(get_session_file()),
}

def handle_request(request: dict) -> dict:
    tool = request.get("tool")
    params = request.get("params", {})

    if tool not in TOOL_HANDLERS:
        return {"error": f"Unknown tool: {tool}"}

    try:
        return TOOL_HANDLERS[tool](params)
    except Exception as e:
        return {"error": str(e)}

# MCP stdio loop
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        request = json.loads(line)
        response = handle_request(request)
        print(json.dumps(response), flush=True)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), flush=True)
    except Exception as e:
        print(json.dumps({"error": str(e)}), flush=True)
```

---

## 12. EXAMPLE WORKFLOW — VYASN BUOY

Once connected, this is the Gemini CLI conversation:

```
You: "Build the VYASN Mark 1 buoy. 
      Hexagonal body, 200mm wide, 100mm tall.
      Solar panel array recessed on top.
      Single antenna 150mm tall on top center.
      Three sensor probes 80mm long hanging from bottom."

Gemini → MCP → FreeCAD:

Step 1: new_document { name: "VYASN_Mark1" }
Step 2: create_primitive { shape: "box", hexagonal body approximation }
Step 3: create_primitive { shape: "cylinder", antenna }
Step 4: transform_object { move antenna to top center }
Step 5: create_primitive { shape: "cylinder", probe x3 }
Step 6: transform_object { move probes to bottom }
Step 7: export_model { format: "stl", output: "vyasn_mark1.stl" }
```

---

## 13. ENVIRONMENT VARIABLES

Create a `.env` file in the project root:

```env
FREECAD_PATH=C:\Program Files\FreeCAD 0.21\bin\FreeCAD.exe
FREECAD_PYTHON_PATH=C:\Program Files\FreeCAD 0.21\bin\python.exe
OUTPUT_DIR=C:\Users\Adarsh\vyasn_models
SCRIPT_TIMEOUT=30
# Session file is auto-created at: OUTPUT_DIR/session/freecad_mcp_session.FCStd
```

---

## 14. DEPENDENCIES (uv)

This project uses [uv](https://docs.astral.sh/uv/) for environment and dependency management.
Dependencies are declared in `pyproject.toml` and pinned in `uv.lock`.

```toml
# pyproject.toml (auto-generated by uv init)
[project]
name = "freecad-mcp"
version = "0.1.0"
description = "FreeCAD MCP Server for VYASN"
requires-python = ">=3.11"
dependencies = [
    "python-dotenv>=1.0.0",
]
```

No other dependencies needed for v1.0. FreeCAD Python API is accessed via subprocess
using FreeCAD's bundled Python — it is NOT installed into this venv.

---

## 15. INSTALLATION STEPS

```bash
# Step 1: Install uv (if not already installed)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Step 2: Clone or create project folder
mkdir freecad-mcp
cd freecad-mcp

# Step 3: Initialise project with uv (creates pyproject.toml + .venv)
uv init .

# Step 4: Add the only dependency
uv add python-dotenv

# Step 5: Set up .env with your FreeCAD paths (copy from §13 above)

# Step 6: Test FreeCAD connection
uv run scripts/test_connection.py

# Step 7: Add MCP config to Gemini CLI settings (see §10)

# Step 8: Run the MCP server directly via uv
uv run server/freecad_mcp_server.py
```

> **Note:** Never activate the venv manually. Always use `uv run <script>` —
> uv handles activation automatically and ensures the correct Python is used.

---

## 16. TEST CONNECTION SCRIPT

```python
# scripts/test_connection.py
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

FREECAD_PYTHON = os.getenv(
    "FREECAD_PYTHON_PATH",
    r"C:\Program Files\FreeCAD 0.21\bin\python.exe"
)

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

result = subprocess.run(
    [FREECAD_PYTHON, "-c", TEST_SCRIPT],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("SUCCESS — FreeCAD MCP connection working")
    print(result.stdout)
else:
    print("FAILED — Check FreeCAD path in .env")
    print(result.stderr)
```

---

## 17. MVP DELIVERABLES

- freecad_mcp_server.py — working MCP server
- All 8 tools implemented and tested (including `reset_session`)
- session_manager.py — file-based state persistence across tool calls
- Gemini CLI connected and responding
- VYASN buoy built successfully from natural language description
- STL export working
- README with setup instructions

---

## 18. SUCCESS CRITERIA

The MCP is successful when:

- Gemini CLI can describe the VYASN buoy in natural language
- FreeCAD builds a recognizable buoy model automatically
- STL file is exported and viewable in any 3D viewer
- Total time from description to STL under 2 minutes
- No manual FreeCAD UI interaction required

---

## 19. FUTURE FEATURES (v2.0)

- Real-time FreeCAD GUI updates — see model building live
- Image to 3D — feed buoy photo, get FreeCAD model
- Parametric templates — "make the buoy 20% larger"
- Multi-document support
- Version history of model iterations
- Direct integration with VYASN hardware manufacturing workflow

---

## 20. KNOWN LIMITATIONS (v1.0)

- FreeCAD must be installed on the same Windows machine
- Complex organic shapes are difficult via primitives alone — use `execute_raw` for those
- No real-time preview — model builds in background
- FreeCAD GUI will not open automatically — headless only
- **State persistence is file-based:** Each tool call saves/loads `session.FCStd`. This means there is a small I/O overhead per call, but state survives crashes and is human-inspectable in FreeCAD
- Hexagonal primitives are not natively supported — approximate with `execute_raw` using `Part.makePolygon()` or a swept profile
- If `session.FCStd` becomes corrupt (e.g. mid-write crash), call `reset_session` to recover

---

*End of PRD — FreeCAD MCP Server v1.0*
*VYASN Marine Intelligence Platform*
*May 2026*