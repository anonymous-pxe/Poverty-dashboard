"""
India State-wise Poverty Data API
Placeholder functions for fetching India-specific poverty data
Replace with actual API calls when endpoints are available
"""

import pandas as pd
import numpy as np
import streamlit as st
import config

@st.cache_data(ttl=config.CACHE_TTL)
def fetch_india_poverty_data(indicator=None, start_year=None, end_year=None, states=None, area_type="All"):
    """
    Fetch India state-wise poverty data
    
    Args:
        indicator (str): Poverty indicator (e.g., 'Poverty Rate (%)')
        start_year (int): Start year
        end_year (int): End year
        states (list): List of state names
        area_type (str): 'All', 'Rural', or 'Urban'
    
    Returns:
        pd.DataFrame: State-wise poverty data
    
    TODO: Replace with actual API endpoint:
        url = "https://api.data.gov.in/resource/..."
        params = {'api-key': 'YOUR_API_KEY', 'format': 'json', ...}
        response = requests.get(url, params=params)
    """
    
    start_year = start_year or config.DATA_START_YEAR
    end_year = end_year or config.DATA_END_YEAR
    states_list = states or config.INDIAN_STATES
    indicator = indicator or "Poverty Rate (%)"
    
    years = list(range(start_year, end_year + 1))
    data = []
    
    for state in states_list:
        # Generate synthetic data with regional patterns
        base_rural = np.random.uniform(15, 50)
        base_urban = base_rural * np.random.uniform(0.3, 0.7)
        trend = np.random.uniform(-0.8, -0.1)
        
        for i, year in enumerate(years):
            if area_type in ["All", "Rural"]:
                rural_value = base_rural + (trend * i) + np.random.normal(0, 3)
                rural_value = max(0, min(100, rural_value))
                
                data.append({
                    'state': state,
                    'year': year,
                    'area_type': 'Rural',
                    'indicator': indicator,
                    'value': round(rural_value, 2)
                })
            
            if area_type in ["All", "Urban"]:
                urban_value = base_urban + (trend * i) + np.random.normal(0, 2)
                urban_value = max(0, min(100, urban_value))
                
                data.append({
                    'state': state,
                    'year': year,
                    'area_type': 'Urban',
                    'indicator': indicator,
                    'value': round(urban_value, 2)
                })
    
    return pd.DataFrame(data)


@st.cache_data(ttl=config.CACHE_TTL)
def fetch_india_multi_indicator_data(start_year=None, end_year=None):
    """
    Fetch multiple indicators for India states
    
    Returns:
        pd.DataFrame: Multi-indicator state-wise data
    """
    
    all_data = []
    
    for indicator in config.INDIA_POVERTY_INDICATORS:
        df = fetch_india_poverty_data(
            indicator=indicator,
            start_year=start_year,
            end_year=end_year
        )
        all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True)


@st.cache_data(ttl=config.CACHE_TTL)
def fetch_state_demographics(state=None):
    """
    Fetch demographic data for Indian states
    
    Args:
        state (str): State name (None for all states)
    
    Returns:
        pd.DataFrame: Demographic data
    
    TODO: Replace with actual census/demographic API
    """
    
    states_list = [state] if state else config.INDIAN_STATES
    
    data = []
    for state_name in states_list:
        data.append({
            'state': state_name,
            'population': np.random.randint(5_000_000, 200_000_000),
            'rural_population_pct': round(np.random.uniform(30, 80), 2),
            'urban_population_pct': round(np.random.uniform(20, 70), 2),
            'literacy_rate': round(np.random.uniform(60, 95), 2),
            'gdp_per_capita': round(np.random.uniform(50000, 300000), 2),
        })
    
    return pd.DataFrame(data)
