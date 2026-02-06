"""
Statistical Analysis Utilities
Functions for statistical calculations and analysis
"""

import pandas as pd
import numpy as np
from scipy import stats as scipy_stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import config


def get_summary_statistics(data):
    """
    Calculate comprehensive summary statistics
    
    Args:
        data (pd.Series or array-like): Input data
    
    Returns:
        dict: Summary statistics
    """
    
    if isinstance(data, pd.DataFrame):
        data = data.values.flatten()
    elif isinstance(data, pd.Series):
        data = data.values
    
    # Remove NaN values
    data = data[~np.isnan(data)]
    
    if len(data) == 0:
        return {}
    
    return {
        'count': len(data),
        'mean': np.mean(data),
        'median': np.median(data),
        'std': np.std(data),
        'variance': np.var(data),
        'min': np.min(data),
        'max': np.max(data),
        'range': np.max(data) - np.min(data),
        'q25': np.percentile(data, 25),
        'q50': np.percentile(data, 50),
        'q75': np.percentile(data, 75),
        'iqr': np.percentile(data, 75) - np.percentile(data, 25),
        'skewness': scipy_stats.skew(data),
        'kurtosis': scipy_stats.kurtosis(data),
    }


def calculate_correlation(data, method='pearson'):
    """
    Calculate correlation matrix
    
    Args:
        data (pd.DataFrame): Input data
        method (str): Correlation method ('pearson', 'spearman', 'kendall')
    
    Returns:
        pd.DataFrame: Correlation matrix
    """
    
    if data.empty:
        return pd.DataFrame()
    
    # Select only numeric columns
    numeric_data = data.select_dtypes(include=[np.number])
    
    if numeric_data.empty:
        return pd.DataFrame()
    
    try:
        corr_matrix = numeric_data.corr(method=method)
        return corr_matrix
    except Exception:
        return pd.DataFrame()


def perform_regression(X, y):
    """
    Perform linear regression analysis
    
    Args:
        X (pd.DataFrame or array-like): Independent variables
        y (pd.Series or array-like): Dependent variable
    
    Returns:
        dict: Regression results including coefficients and metrics
    """
    
    # Ensure proper format
    if isinstance(X, pd.Series):
        X = X.values.reshape(-1, 1)
    elif isinstance(X, pd.DataFrame):
        X = X.values
    
    if isinstance(y, pd.Series):
        y = y.values
    
    # Remove rows with NaN
    mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
    X = X[mask]
    y = y[mask]
    
    if len(X) == 0 or len(y) == 0:
        return {
            'coefficients': [],
            'intercept': 0,
            'r2_score': 0,
            'adjusted_r2': 0,
            'rmse': 0,
            'mae': 0
        }
    
    # Fit model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predictions
    y_pred = model.predict(X)
    
    # Metrics
    r2 = r2_score(y, y_pred)
    n = len(y)
    p = X.shape[1]
    adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    
    return {
        'coefficients': model.coef_.tolist(),
        'intercept': float(model.intercept_),
        'r2_score': r2,
        'adjusted_r2': adjusted_r2,
        'rmse': rmse,
        'mae': mae,
        'model': model
    }


def perform_ttest(group1, group2, alternative='two-sided'):
    """
    Perform independent t-test
    
    Args:
        group1 (array-like): First group
        group2 (array-like): Second group
        alternative (str): 'two-sided', 'less', or 'greater'
    
    Returns:
        dict: T-test results
    """
    
    # Remove NaN values
    group1 = np.array(group1)[~np.isnan(group1)]
    group2 = np.array(group2)[~np.isnan(group2)]
    
    if len(group1) == 0 or len(group2) == 0:
        return {'statistic': 0, 'pvalue': 1, 'significant': False}
    
    try:
        statistic, pvalue = scipy_stats.ttest_ind(group1, group2, alternative=alternative)
        
        return {
            'statistic': float(statistic),
            'pvalue': float(pvalue),
            'significant': pvalue < (1 - config.CONFIDENCE_LEVEL),
            'mean_group1': np.mean(group1),
            'mean_group2': np.mean(group2),
            'std_group1': np.std(group1),
            'std_group2': np.std(group2)
        }
    except Exception:
        return {'statistic': 0, 'pvalue': 1, 'significant': False}


def calculate_confidence_interval(data, confidence=None):
    """
    Calculate confidence interval
    
    Args:
        data (array-like): Input data
        confidence (float): Confidence level (default from config)
    
    Returns:
        tuple: (lower_bound, upper_bound)
    """
    
    confidence = confidence or config.CONFIDENCE_LEVEL
    
    data = np.array(data)[~np.isnan(data)]
    
    if len(data) == 0:
        return (0, 0)
    
    mean = np.mean(data)
    se = scipy_stats.sem(data)
    margin = se * scipy_stats.t.ppf((1 + confidence) / 2, len(data) - 1)
    
    return (mean - margin, mean + margin)


def perform_anova(*groups):
    """
    Perform one-way ANOVA
    
    Args:
        *groups: Variable number of groups
    
    Returns:
        dict: ANOVA results
    """
    
    # Remove NaN values from each group
    clean_groups = [np.array(g)[~np.isnan(g)] for g in groups]
    clean_groups = [g for g in clean_groups if len(g) > 0]
    
    if len(clean_groups) < 2:
        return {'f_statistic': 0, 'pvalue': 1, 'significant': False}
    
    try:
        f_stat, pvalue = scipy_stats.f_oneway(*clean_groups)
        
        return {
            'f_statistic': float(f_stat),
            'pvalue': float(pvalue),
            'significant': pvalue < (1 - config.CONFIDENCE_LEVEL),
            'num_groups': len(clean_groups)
        }
    except Exception:
        return {'f_statistic': 0, 'pvalue': 1, 'significant': False}


def calculate_zscore(data):
    """
    Calculate z-scores for data
    
    Args:
        data (array-like): Input data
    
    Returns:
        np.array: Z-scores
    """
    
    data = np.array(data)
    mean = np.nanmean(data)
    std = np.nanstd(data)
    
    if std == 0:
        return np.zeros_like(data)
    
    return (data - mean) / std


def detect_outliers(data, method='iqr', threshold=3):
    """
    Detect outliers in data
    
    Args:
        data (array-like): Input data
        method (str): 'iqr' or 'zscore'
        threshold (float): Threshold for outlier detection
    
    Returns:
        np.array: Boolean mask of outliers
    """
    
    data = np.array(data)
    
    if method == 'iqr':
        q1 = np.nanpercentile(data, 25)
        q3 = np.nanpercentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        outliers = (data < lower_bound) | (data > upper_bound)
    
    elif method == 'zscore':
        zscores = np.abs(calculate_zscore(data))
        outliers = zscores > threshold
    
    else:
        outliers = np.zeros(len(data), dtype=bool)
    
    return outliers


def calculate_growth_rate(values, periods=1):
    """
    Calculate growth rate over time
    
    Args:
        values (array-like): Time series values
        periods (int): Number of periods for growth calculation
    
    Returns:
        np.array: Growth rates (as percentages)
    """
    
    values = np.array(values)
    
    if len(values) < periods + 1:
        return np.array([])
    
    growth_rates = np.zeros(len(values))
    growth_rates[:periods] = np.nan
    
    for i in range(periods, len(values)):
        if values[i - periods] != 0:
            growth_rates[i] = ((values[i] - values[i - periods]) / values[i - periods]) * 100
        else:
            growth_rates[i] = np.nan
    
    return growth_rates


def calculate_moving_average(data, window=3):
    """
    Calculate moving average
    
    Args:
        data (array-like): Input data
        window (int): Window size
    
    Returns:
        np.array: Moving averages
    """
    
    data = np.array(data)
    
    if len(data) < window:
        return data
    
    return np.convolve(data, np.ones(window) / window, mode='valid')
