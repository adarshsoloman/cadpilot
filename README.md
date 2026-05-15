# FreeCAD MCP Server

Connect Gemini CLI to FreeCAD on Windows using the Model Context Protocol.

## Features
- **Stateless Persistence:** Uses a file-based session manager (`session.FCStd`) to maintain state between tool calls.
- **7+ Tools:** Primitives, Boolean operations, Transforms, Export, Raw Python execution.
- **Windows Optimized:** Automatically finds FreeCAD bundled Python.
- **Powered by uv:** Fast dependency and environment management.

## Prerequisites
- **FreeCAD 0.21+** (Tested on 1.1)
- **uv** (Python package manager)
- **Gemini CLI** (or any MCP client)

## Setup

1. **Clone the repository** (or navigate to this folder).
2. **Configure .env**:
   Ensure `FREECAD_PATH` and `FREECAD_PYTHON_PATH` match your installation.
   ```env
   FREECAD_PATH=C:\Program Files\FreeCAD 1.1\bin\FreeCAD.exe
   FREECAD_PYTHON_PATH=C:\Program Files\FreeCAD 1.1\bin\python.exe
   ```
3. **Install dependencies**:
   ```bash
   uv sync
   ```
4. **Test connection**:
   ```bash
   uv run scripts/test_connection.py
   ```

## Gemini CLI Integration
Add the following to your `gemini_settings.json`:
```json
{
  "mcpServers": {
    "freecad": {
      "command": "uv",
      "args": ["run", "C:/path/to/server/freecad_mcp_server.py"],
      "env": {
        "FREECAD_PATH": "C:/Program Files/FreeCAD 1.1/bin/FreeCAD.exe",
        "OUTPUT_DIR": "C:/path/to/project"
      }
    }
  }
}
```

## Tools
- `create_primitive`: Box, Cylinder, Sphere, Cone, Torus.
- `boolean_operation`: Union, Cut, Intersection.
- `transform_object`: Move, Rotate, Scale.
- `export_model`: STL, STEP, FCStd.
- `execute_raw`: Direct FreeCAD Python API access.
- `list_objects`: View current document objects.
- `new_document` / `reset_session`: Start fresh.

---
*VYASN Marine Intelligence Platform*
