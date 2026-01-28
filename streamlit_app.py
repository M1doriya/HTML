import runpy

# Streamlit Cloud defaults to 'streamlit_app.py' as the entrypoint.
# This wrapper keeps the core app in 'streamlit_app_v5.1_fixed_patched.py'.
runpy.run_path('streamlit_app_v5.1_fixed_patched.py', run_name='__main__')
