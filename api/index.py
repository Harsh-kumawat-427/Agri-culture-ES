import os
import sys
import traceback
 
# Ensure project root is on sys.path so modules like crop_expert_system and app can be imported
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
 
try:
    from app import app
except Exception:
    # DIAGNOSTIC: show the real startup error in the browser instead of a blank 500.
    # Once the site works, this block never runs and can stay or be removed.
    _err = traceback.format_exc()
    print(_err, file=sys.stderr)
    from flask import Flask, Response
    app = Flask(__name__)
 
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def _startup_error(path):
        info = (
            "STARTUP ERROR - copy this and send it to Claude\n\n"
            f"Python {sys.version}\n\n{_err}\n"
            f"ROOT_DIR={ROOT_DIR}\nFiles in root: {sorted(os.listdir(ROOT_DIR))}\n"
        )
        return Response(info, status=500, mimetype="text/plain")
 
