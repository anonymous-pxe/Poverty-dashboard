"""
Sidebar Component - Navigation and main filters
"""

import streamlit as st
from .filters import create_filters
import config


def render_sidebar():
    """
    Render the sidebar with navigation and filters
    
    Returns:
        tuple: (page_selection, filters_dict)
    """
    
    with st.sidebar:
        # Logo and title
        st.markdown(f"# {config.APP_ICON} {config.APP_TITLE}")
        st.markdown(f"*Version {config.APP_VERSION}*")
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📑 Navigation")
        page_selection = st.radio(
            "Select Page",
            options=[
                "Dashboard",
                "Global Trends",
                "Rural vs Urban",
                "Statistical Analysis",
                "Visualization",
                "Reports",
                "Learn More"
            ],
            label_visibility="collapsed",
            key="page_navigation"
        )
        
        st.markdown("---")
        
        # Filters (only for data pages)
        if page_selection != "Learn More":
            st.markdown("### 🔧 Filters")
            filters = create_filters()
        else:
            filters = {}
        
        st.markdown("---")
        
        # Quick Stats
        render_quick_stats()
        
        st.markdown("---")
        
        # Footer
        render_footer()
    
    return page_selection, filters


def render_quick_stats():
    """Render quick statistics in sidebar"""
    
    st.markdown("### 📊 Quick Stats")
    
    # These are placeholder values - in production, load from cache
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Countries", "195", help="Total countries tracked")
    
    with col2:
        st.metric("States", "36", help="Indian states and territories")
    
    st.metric(
        "Global Avg",
        "18.5%",
        delta="-2.3%",
        delta_color="inverse",
        help="Global average poverty rate (latest year)"
    )
    
    st.metric(
        "India Avg",
        "21.2%",
        delta="-3.1%",
        delta_color="inverse",
        help="India average poverty rate (latest year)"
    )


def render_footer():
    """Render sidebar footer"""
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Poverty Dashboard** provides comprehensive poverty data analysis and visualization.
    
    - 🌍 Global coverage
    - 🇮🇳 India focus
    - 📈 Trend analysis
    - 🤖 ML predictions
    
    [📚 Documentation](#) | [🐛 Report Issue](#)
    """)
    
    st.markdown("---")
    st.markdown(f"*Data range: {config.DATA_START_YEAR}-{config.DATA_END_YEAR}*")
