"""
Streamlit app untuk deteksi parkir motor
Optimized untuk deployment di Streamlit Cloud
"""
import streamlit as st
import os

# Set page config sebagai hal pertama
st.set_page_config(
    page_title="Dashboard Deteksi Parkir - AFEnter",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caching untuk mempercepat loading
@st.cache_resource
def check_environment():
    """Check if all dependencies are available"""
    try:
        import cv2
        import numpy as np
        from rembg import remove
        return True, "All dependencies loaded successfully"
    except ImportError as e:
        return False, f"Missing dependency: {str(e)}"

# Check environment
deps_ok, deps_msg = check_environment()
if not deps_ok:
    st.error(f"❌ Dependency Error: {deps_msg}")
    st.stop()

# Import the main app
from app import *
