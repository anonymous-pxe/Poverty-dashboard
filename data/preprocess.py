"""
Data Preprocessing and Transformation
Functions for cleaning, filtering, and transforming poverty data
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Tuple


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize dataframe
    
    Args:
        df (pd.DataFrame): Raw data
    
    Returns:
        pd.DataFrame: Cleaned data
    """
    
    if df is None or df.empty:
        return df
    
    df_clean = df.copy()
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values in numeric columns
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        # Fill with median for numeric columns
        if df_clean[col].isnull().any():
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    # Handle missing values in categorical columns
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_clean[col].isnull().any():
            df_clean[col].fillna('Unknown', inplace=True)
    
    # Remove outliers using IQR method for 'value' column if exists
    if 'value' in df_clean.columns:
        Q1 = df_clean['value'].quantile(0.25)
        Q3 = df_clean['value'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 3 * IQR
        upper_bound = Q3 + 3 * IQR
        df_clean = df_clean[
            (df_clean['value'] >= lower_bound) & 
            (df_clean['value'] <= upper_bound)
        ]
    
    return df_clean


def filter_data(
    df: pd.DataFrame,
    year_range: Optional[Tuple[int, int]] = None,
    states: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    area_type: Optional[str] = None,
    indicators: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filter dataframe based on multiple criteria
    
    Args:
        df (pd.DataFrame): Input data
        year_range (tuple): (start_year, end_year)
        states (list): State names to filter
        countries (list): Country codes to filter
        area_type (str): 'Rural', 'Urban', or 'All'
        indicators (list): Indicator names to filter
    
    Returns:
        pd.DataFrame: Filtered data
    """
    
    if df is None or df.empty:
        return df
    
    df_filtered = df.copy()
    
    # Filter by year range
    if year_range and 'year' in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered['year'] >= year_range[0]) & 
            (df_filtered['year'] <= year_range[1])
        ]
    
    # Filter by states
    if states and 'state' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['state'].isin(states)]
    
    # Filter by countries
    if countries and 'country' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['country'].isin(countries)]
    
    # Filter by area type
    if area_type and area_type != "All" and 'area_type' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['area_type'] == area_type]
    
    # Filter by indicators
    if indicators and 'indicator' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['indicator'].isin(indicators)]
    
    return df_filtered


def transform_data(df: pd.DataFrame, transformation: str = 'none') -> pd.DataFrame:
    """
    Apply transformations to data
    
    Args:
        df (pd.DataFrame): Input data
        transformation (str): Type of transformation
            - 'none': No transformation
            - 'log': Log transformation
            - 'sqrt': Square root transformation
            - 'normalize': Min-max normalization
            - 'standardize': Z-score standardization
    
    Returns:
        pd.DataFrame: Transformed data
    """
    
    if df is None or df.empty or 'value' not in df.columns:
        return df
    
    df_transformed = df.copy()
    
    if transformation == 'log':
        df_transformed['value'] = np.log1p(df_transformed['value'])
    
    elif transformation == 'sqrt':
        df_transformed['value'] = np.sqrt(df_transformed['value'])
    
    elif transformation == 'normalize':
        min_val = df_transformed['value'].min()
        max_val = df_transformed['value'].max()
        if max_val > min_val:
            df_transformed['value'] = (df_transformed['value'] - min_val) / (max_val - min_val)
    
    elif transformation == 'standardize':
        mean_val = df_transformed['value'].mean()
        std_val = df_transformed['value'].std()
        if std_val > 0:
            df_transformed['value'] = (df_transformed['value'] - mean_val) / std_val
    
    return df_transformed


def aggregate_data(
    df: pd.DataFrame,
    group_by: List[str],
    agg_func: str = 'mean'
) -> pd.DataFrame:
    """
    Aggregate data by specified columns
    
    Args:
        df (pd.DataFrame): Input data
        group_by (list): Columns to group by
        agg_func (str): Aggregation function ('mean', 'sum', 'count', 'min', 'max')
    
    Returns:
        pd.DataFrame: Aggregated data
    """
    
    if df is None or df.empty:
        return df
    
    # Verify group_by columns exist
    valid_cols = [col for col in group_by if col in df.columns]
    if not valid_cols:
        return df
    
    # Find numeric columns to aggregate
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        return df
    
    agg_dict = {col: agg_func for col in numeric_cols}
    
    df_agg = df.groupby(valid_cols, as_index=False).agg(agg_dict)
    
    return df_agg


def pivot_data(
    df: pd.DataFrame,
    index: str,
    columns: str,
    values: str
) -> pd.DataFrame:
    """
    Pivot data for easier visualization
    
    Args:
        df (pd.DataFrame): Input data
        index (str): Column to use as index
        columns (str): Column to use as columns
        values (str): Column to use as values
    
    Returns:
        pd.DataFrame: Pivoted data
    """
    
    if df is None or df.empty:
        return df
    
    required_cols = [index, columns, values]
    if not all(col in df.columns for col in required_cols):
        return df
    
    try:
        df_pivot = df.pivot_table(
            index=index,
            columns=columns,
            values=values,
            aggfunc='mean'
        )
        return df_pivot.reset_index()
    except Exception:
        return df


def calculate_growth_rate(df: pd.DataFrame, value_col: str = 'value') -> pd.DataFrame:
    """
    Calculate year-over-year growth rate
    
    Args:
        df (pd.DataFrame): Input data with 'year' column
        value_col (str): Column to calculate growth for
    
    Returns:
        pd.DataFrame: Data with growth_rate column
    """
    
    if df is None or df.empty or 'year' not in df.columns or value_col not in df.columns:
        return df
    
    df_growth = df.copy()
    df_growth = df_growth.sort_values('year')
    
    # Calculate percentage change
    df_growth['growth_rate'] = df_growth.groupby(
        [col for col in df.columns if col not in ['year', value_col, 'growth_rate']]
    )[value_col].pct_change() * 100
    
    return df_growth
