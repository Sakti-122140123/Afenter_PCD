"""
Streamlit app wrapper untuk deteksi parkir motor
Optimized untuk deployment di Streamlit Cloud
"""
import streamlit as st
import sys
import os

# Set page config sebagai hal pertama
st.set_page_config(
    page_title="Dashboard Deteksi Parkir - AFEnter",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check dependencies availability
@st.cache_resource
def check_dependencies():
    """Check if all dependencies are available"""
    missing_deps = []
    try:
        import cv2
    except ImportError:
        missing_deps.append("opencv-python-headless")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        from rembg import remove
    except ImportError:
        missing_deps.append("rembg")
    
    try:
        from PIL import Image
    except ImportError:
        missing_deps.append("Pillow")
    
    return missing_deps

# Check environment
missing = check_dependencies()
if missing:
    st.error(f"❌ Missing dependencies: {', '.join(missing)}")
    st.info("Please install required packages from requirements.txt")
    st.stop()

# Everything OK, load the main app
try:
    # Import semua dari app module
    import app
except Exception as e:
    st.error(f"❌ Error loading app: {str(e)}")
    st.info("Please check app.py for errors")
    st.stop()
