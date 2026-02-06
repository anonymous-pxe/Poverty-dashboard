"""
Filter Components - Year, state, country, and indicator filters
"""

import streamlit as st
import config


def create_filters():
    """
    Create filter controls and return filter values
    
    Returns:
        dict: Dictionary with filter values
    """
    
    filters = {}
    
    # Year range filter
    filters['year_range'] = create_year_filter()
    
    # State filter
    filters['states'] = create_state_filter()
    
    # Country filter (commented out by default, can be enabled)
    # filters['countries'] = create_country_filter()
    
    # Area type filter
    filters['area_type'] = create_area_type_filter()
    
    # Indicator filter (for multi-indicator pages)
    # filters['indicator'] = create_indicator_filter()
    
    return filters


def create_year_filter():
    """Create year range filter"""
    
    st.markdown("#### 📅 Year Range")
    
    year_range = st.slider(
        "Select year range",
        min_value=config.DATA_START_YEAR,
        max_value=config.DATA_END_YEAR,
        value=(config.DATA_START_YEAR, config.DATA_END_YEAR),
        step=1,
        label_visibility="collapsed"
    )
    
    return year_range


def create_state_filter():
    """Create state selection filter"""
    
    st.markdown("#### 🗺️ Indian States")
    
    filter_type = st.radio(
        "State Filter",
        options=["All States", "Select Specific"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if filter_type == "Select Specific":
        states = st.multiselect(
            "Select states",
            options=config.INDIAN_STATES,
            default=[],
            label_visibility="collapsed"
        )
        return states if states else None
    else:
        return None


def create_country_filter():
    """Create country selection filter"""
    
    st.markdown("#### 🌍 Countries")
    
    # Placeholder - in production, load from data
    common_countries = [
        'USA', 'IND', 'CHN', 'BRA', 'NGA', 'IDN', 'PAK', 'BGD',
        'RUS', 'MEX', 'JPN', 'DEU', 'GBR', 'FRA', 'ITA', 'ZAF'
    ]
    
    filter_type = st.radio(
        "Country Filter",
        options=["All Countries", "Select Specific"],
        horizontal=True,
        label_visibility="collapsed",
        key='country_filter_type'
    )
    
    if filter_type == "Select Specific":
        countries = st.multiselect(
            "Select countries",
            options=common_countries,
            default=[],
            label_visibility="collapsed"
        )
        return countries if countries else None
    else:
        return None


def create_area_type_filter():
    """Create area type filter (Rural/Urban)"""
    
    st.markdown("#### 🏘️ Area Type")
    
    area_type = st.selectbox(
        "Select area type",
        options=config.AREA_TYPES,
        index=0,
        label_visibility="collapsed"
    )
    
    return area_type


def create_indicator_filter():
    """Create indicator selection filter"""
    
    st.markdown("#### 📊 Indicators")
    
    indicators = st.multiselect(
        "Select indicators",
        options=config.INDIA_POVERTY_INDICATORS,
        default=[config.INDIA_POVERTY_INDICATORS[0]],
        label_visibility="collapsed"
    )
    
    return indicators if indicators else [config.INDIA_POVERTY_INDICATORS[0]]


def create_advanced_filters():
    """Create advanced filter options"""
    
    with st.expander("🔧 Advanced Filters"):
        st.markdown("#### Data Quality")
        
        remove_outliers = st.checkbox("Remove outliers", value=False)
        
        st.markdown("#### Aggregation")
        
        aggregation = st.selectbox(
            "Aggregation method",
            options=["Mean", "Median", "Sum", "Min", "Max"],
            index=0
        )
        
        return {
            'remove_outliers': remove_outliers,
            'aggregation': aggregation.lower()
        }
