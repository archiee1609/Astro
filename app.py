"""
app.py - Alternative root entry point for Streamlit Community Cloud (streamlit.io)
Allows deployment when 'app.py' is selected as the main file path.
"""
import os
import sys
import runpy

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

runpy.run_path(os.path.join(PROJECT_ROOT, "ui", "streamlit_app.py"), run_name="__main__")
