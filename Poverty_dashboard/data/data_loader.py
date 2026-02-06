"""
Unified Data Loading and Caching
Central module for loading all data sources
"""

import pandas as pd
import streamlit as st
from .wb_api import fetch_wb_poverty_data, fetch_wb_country_metadata, fetch_all_wb_indicators
from .india_poverty_api import fetch_india_poverty_data, fetch_india_multi_indicator_data, fetch_state_demographics
import config


@st.cache_data(ttl=config.CACHE_TTL)
def load_data(data_type, **kwargs):
    """
    Universal data loader with caching
    
    Args:
        data_type (str): Type of data to load
            - 'wb_poverty': World Bank poverty data
            - 'wb_all_indicators': All WB indicators
            - 'wb_metadata': Country metadata
            - 'india_poverty': India state-wise poverty
            - 'india_multi_indicator': Multiple India indicators
            - 'india_demographics': India state demographics
        **kwargs: Additional arguments passed to specific loader functions
    
    Returns:
        pd.DataFrame or dict: Loaded data
    """
    
    loaders = {
        'wb_poverty': fetch_wb_poverty_data,
        'wb_all_indicators': fetch_all_wb_indicators,
        'wb_metadata': fetch_wb_country_metadata,
        'india_poverty': fetch_india_poverty_data,
        'india_multi_indicator': fetch_india_multi_indicator_data,
        'india_demographics': fetch_state_demographics,
    }
    
    if data_type not in loaders:
        raise ValueError(f"Unknown data_type: {data_type}")
    
    return loaders[data_type](**kwargs)


@st.cache_data(ttl=config.CACHE_TTL)
def get_cached_data(cache_key):
    """
    Get data from cache with a specific key
    
    Args:
        cache_key (str): Unique cache identifier
    
    Returns:
        Any: Cached data
    """
    # This is a placeholder for more sophisticated caching
    # In production, you might use Redis, database, or file-based caching
    return None


def clear_cache():
    """Clear all cached data"""
    st.cache_data.clear()


@st.cache_data(ttl=config.CACHE_TTL)
def load_combined_dataset(filters=None):
    """
    Load and combine all datasets based on filters
    
    Args:
        filters (dict): Filter parameters
            - year_range: (start, end)
            - states: list of states
            - countries: list of countries
            - indicators: list of indicators
    
    Returns:
        dict: Combined datasets
    """
    
    filters = filters or {}
    
    # Extract filter parameters
    year_range = filters.get('year_range', (config.DATA_START_YEAR, config.DATA_END_YEAR))
    states = filters.get('states', None)
    countries = filters.get('countries', None)
    
    datasets = {}
    
    # Load World Bank data
    datasets['wb_poverty'] = load_data(
        'wb_poverty',
        indicator_code='SI.POV.DDAY',
        start_year=year_range[0],
        end_year=year_range[1],
        countries=countries
    )
    
    # Load India data
    datasets['india_poverty'] = load_data(
        'india_poverty',
        start_year=year_range[0],
        end_year=year_range[1],
        states=states
    )
    
    # Load metadata
    datasets['wb_metadata'] = load_data('wb_metadata')
    datasets['india_demographics'] = load_data('india_demographics')
    
    return datasets


def get_data_summary(df):
    """
    Get summary statistics for a dataframe
    
    Args:
        df (pd.DataFrame): Input dataframe
    
    Returns:
        dict: Summary statistics
    """
    
    if df is None or df.empty:
        return {}
    
    return {
        'row_count': len(df),
        'column_count': len(df.columns),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
        'null_counts': df.isnull().sum().to_dict(),
        'dtypes': df.dtypes.astype(str).to_dict(),
    }
