import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
runpy.run_path(str(HERE / "streamlit_app_v5.1_fixed_patched_v3.py"), run_name="__main__")
