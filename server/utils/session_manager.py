import os

def get_session_file() -> str:
    # Use project root session folder by default
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    session_dir = os.path.join(project_root, "session")
    
    # Allow override via ENV
    output_dir = os.getenv("OUTPUT_DIR")
    if output_dir:
        session_dir = os.path.join(output_dir, "session")
        
    return os.path.join(session_dir, "freecad_mcp_session.FCStd")

def build_session_preamble(session_file: str) -> str:
    """Load existing session doc or create a fresh one."""
    # Ensure backslashes are escaped for Python string literal
    escaped_path = session_file.replace("\\", "\\\\")
    return f"""
import FreeCAD, Part, os
SESSION_FILE = r'{escaped_path}'
os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
if os.path.exists(SESSION_FILE):
    try:
        doc = FreeCAD.openDocument(SESSION_FILE)
    except Exception:
        doc = FreeCAD.newDocument('Session')
else:
    doc = FreeCAD.newDocument('Session')
"""

def build_session_postamble(session_file: str) -> str:
    """Recompute and save the session doc after every tool call."""
    escaped_path = session_file.replace("\\", "\\\\")
    return f"""
if 'doc' in locals():
    doc.recompute()
    doc.saveAs(r'{escaped_path}')
    print("__SESSION_SAVED__")
"""

def reset_session(session_file: str) -> dict:
    """Delete the session file to start fresh."""
    if os.path.exists(session_file):
        try:
            os.remove(session_file)
            return {"success": True, "message": "Session reset. Next tool call starts a new document."}
        except Exception as e:
            return {"success": False, "message": f"Failed to reset session: {str(e)}"}
    return {"success": True, "message": "No active session to reset."}
