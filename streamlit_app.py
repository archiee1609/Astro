"""
streamlit_app.py - Root entry point for Streamlit Community Cloud (streamlit.io)
Enables 1-click deployment on Streamlit Cloud without custom path configuration.
"""
import os
import sys
import runpy

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__" or True:
    runpy.run_path(os.path.join(PROJECT_ROOT, "ui", "streamlit_app.py"), run_name="__main__")
