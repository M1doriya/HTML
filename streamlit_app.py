import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
runpy.run_path(str(ROOT / "streamlit_app_v5.1_fixed_patched_v3.py"), run_name="__main__")
