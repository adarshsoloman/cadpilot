import subprocess
import tempfile
import os
import json
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
    # On Windows, we need to be careful with file closing before subprocess access
    temp_fd, temp_path = tempfile.mkstemp(suffix='.py', text=True)
    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            f.write(full_code)
        
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
        
        # Check if we should parse stdout as JSON if it's expected
        # For now, just return raw results
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "session_file": session_file,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Script execution timed out",
            "stdout": "",
            "stderr": "TimeoutExpired"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
