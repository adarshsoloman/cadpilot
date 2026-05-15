import sys
import json
import os
from dotenv import load_dotenv

# Add the current directory to sys.path to allow imports of tools/utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

def main():
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

if __name__ == "__main__":
    main()
