"""
Machine Learning Utilities
Functions for ML models and predictions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import config


def train_model(data, target, features, model_type='Linear Regression'):
    """
    Train a machine learning model
    
    Args:
        data (pd.DataFrame): Input data
        target (str): Target column name
        features (list): Feature column names
        model_type (str): Model type from config.ML_MODELS
    
    Returns:
        tuple: (trained_model, metrics_dict, predictions_df)
    """
    
    # Prepare data
    X = data[features].values
    y = data[target].values
    
    # Remove NaN values
    mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
    X = X[mask]
    y = y[mask]
    
    if len(X) == 0:
        return None, {}, pd.DataFrame()
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config.ML_TEST_SIZE,
        random_state=config.ML_RANDOM_STATE
    )
    
    # Select and train model
    if model_type == 'Linear Regression':
        model = LinearRegression()
    elif model_type == 'Random Forest':
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=config.ML_RANDOM_STATE,
            n_jobs=-1
        )
    elif model_type == 'Gradient Boosting':
        model = GradientBoostingRegressor(
            n_estimators=100,
            random_state=config.ML_RANDOM_STATE
        )
    else:
        model = LinearRegression()
    
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    metrics = evaluate_model(y_test, y_pred)
    
    # Create predictions dataframe
    predictions = pd.DataFrame({
        'actual': y_test,
        'predicted': y_pred
    })
    
    return model, metrics, predictions


def evaluate_model(y_true, y_pred):
    """
    Evaluate model performance
    
    Args:
        y_true (array-like): True values
        y_pred (array-like): Predicted values
    
    Returns:
        dict: Evaluation metrics
    """
    
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    
    # MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    return {
        'r2': r2,
        'rmse': rmse,
        'mae': mae,
        'mape': mape
    }


def predict_future(model, historical_data, years_ahead=5):
    """
    Predict future values
    
    Args:
        model: Trained model
        historical_data (pd.DataFrame): Historical data with 'year' and 'value'
        years_ahead (int): Number of years to predict
    
    Returns:
        pd.DataFrame: Future predictions
    """
    
    if model is None or historical_data.empty:
        return pd.DataFrame()
    
    # Get last year in historical data
    last_year = historical_data['year'].max()
    
    # Create future years
    future_years = np.arange(last_year + 1, last_year + years_ahead + 1)
    
    # Prepare features (simplified - just year)
    X_future = future_years.reshape(-1, 1)
    
    # Predict
    predictions = model.predict(X_future)
    
    # Create dataframe
    future_df = pd.DataFrame({
        'year': future_years,
        'value': predictions
    })
    
    return future_df


def feature_importance(model, feature_names):
    """
    Get feature importance from tree-based models
    
    Args:
        model: Trained tree-based model
        feature_names (list): Names of features
    
    Returns:
        pd.DataFrame: Feature importance scores
    """
    
    if not hasattr(model, 'feature_importances_'):
        return pd.DataFrame()
    
    importance = model.feature_importances_
    
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)
    
    return importance_df


def cross_validate_model(data, target, features, model_type='Linear Regression', cv=5):
    """
    Perform cross-validation
    
    Args:
        data (pd.DataFrame): Input data
        target (str): Target column
        features (list): Feature columns
        model_type (str): Model type
        cv (int): Number of folds
    
    Returns:
        dict: Cross-validation results
    """
    
    from sklearn.model_selection import cross_val_score
    
    # Prepare data
    X = data[features].values
    y = data[target].values
    
    # Remove NaN
    mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
    X = X[mask]
    y = y[mask]
    
    if len(X) < cv:
        return {'mean_score': 0, 'std_score': 0, 'scores': []}
    
    # Select model
    if model_type == 'Linear Regression':
        model = LinearRegression()
    elif model_type == 'Random Forest':
        model = RandomForestRegressor(random_state=config.ML_RANDOM_STATE)
    elif model_type == 'Gradient Boosting':
        model = GradientBoostingRegressor(random_state=config.ML_RANDOM_STATE)
    else:
        model = LinearRegression()
    
    # Cross-validate
    scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
    
    return {
        'mean_score': scores.mean(),
        'std_score': scores.std(),
        'scores': scores.tolist()
    }


def hyperparameter_tuning(data, target, features, model_type='Random Forest'):
    """
    Perform basic hyperparameter tuning
    
    Args:
        data (pd.DataFrame): Input data
        target (str): Target column
        features (list): Feature columns
        model_type (str): Model type
    
    Returns:
        dict: Best parameters and score
    """
    
    from sklearn.model_selection import GridSearchCV
    
    # Prepare data
    X = data[features].values
    y = data[target].values
    
    # Remove NaN
    mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
    X = X[mask]
    y = y[mask]
    
    if len(X) < 10:
        return {'best_params': {}, 'best_score': 0}
    
    # Define parameter grid
    if model_type == 'Random Forest':
        model = RandomForestRegressor(random_state=config.ML_RANDOM_STATE)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, None],
            'min_samples_split': [2, 5, 10]
        }
    elif model_type == 'Gradient Boosting':
        model = GradientBoostingRegressor(random_state=config.ML_RANDOM_STATE)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 5, 7]
        }
    else:
        return {'best_params': {}, 'best_score': 0}
    
    # Grid search
    grid_search = GridSearchCV(
        model, 
        param_grid, 
        cv=3, 
        scoring='r2',
        n_jobs=-1
    )
    
    grid_search.fit(X, y)
    
    return {
        'best_params': grid_search.best_params_,
        'best_score': grid_search.best_score_
    }


def create_ensemble_prediction(models, X):
    """
    Create ensemble prediction from multiple models
    
    Args:
        models (list): List of trained models
        X (array-like): Input features
    
    Returns:
        np.array: Averaged predictions
    """
    
    predictions = []
    
    for model in models:
        pred = model.predict(X)
        predictions.append(pred)
    
    # Average predictions
    ensemble_pred = np.mean(predictions, axis=0)
    
    return ensemble_pred
