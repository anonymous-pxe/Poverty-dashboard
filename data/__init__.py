"""
Data module for Poverty Dashboard
Handles data fetching, caching, and preprocessing
"""

from .wb_api import fetch_wb_poverty_data
from .india_poverty_api import fetch_india_poverty_data
from .data_loader import load_data, get_cached_data
from .preprocess import clean_data, filter_data, transform_data

__all__ = [
    'fetch_wb_poverty_data',
    'fetch_india_poverty_data',
    'load_data',
    'get_cached_data',
    'clean_data',
    'filter_data',
    'transform_data',
]
