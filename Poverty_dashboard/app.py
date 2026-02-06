"""
Poverty Dashboard - Main Entry Point
A comprehensive Streamlit dashboard for analyzing global and India-specific poverty data.
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from components.sidebar import render_sidebar
from pages import dashboard, global_trends, rural_vs_urban, analysis, visualization, reports, learn_more
import config

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load custom CSS styles"""
    css_path = project_root / "assets" / "css" / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


def main():
    """Main application logic"""
    
    # Render sidebar and get navigation selection
    page_selection, filters = render_sidebar()
    
    # Page routing
    if page_selection == "Dashboard":
        dashboard.render(filters)
    elif page_selection == "Global Trends":
        global_trends.render(filters)
    elif page_selection == "Rural vs Urban":
        rural_vs_urban.render(filters)
    elif page_selection == "Statistical Analysis":
        analysis.render(filters)
    elif page_selection == "Visualization":
        visualization.render(filters)
    elif page_selection == "Reports":
        reports.render(filters)
    elif page_selection == "Learn More":
        learn_more.render()


if __name__ == "__main__":
    main()
