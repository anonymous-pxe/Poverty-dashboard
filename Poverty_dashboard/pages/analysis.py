"""
Statistical Analysis Page - Advanced analytics, correlation, regression
"""

import streamlit as st
import pandas as pd
from data.data_loader import load_data
from data.preprocess import clean_data
from utils.stats import calculate_correlation, perform_regression, get_summary_statistics
from utils.ml import train_model, predict_future, evaluate_model
from utils.visualization import create_scatter_plot, create_heatmap
import config


def render(filters):
    """Render the statistical analysis page"""
    
    st.title("📊 Statistical Analysis")
    st.markdown("Advanced statistical analysis and machine learning predictions")
    st.markdown("---")
    
    # Analysis type selection
    analysis_tabs = st.tabs([
        "Summary Statistics",
        "Correlation Analysis",
        "Regression Analysis",
        "ML Predictions"
    ])
    
    with analysis_tabs[0]:
        render_summary_statistics(filters)
    
    with analysis_tabs[1]:
        render_correlation_analysis(filters)
    
    with analysis_tabs[2]:
        render_regression_analysis(filters)
    
    with analysis_tabs[3]:
        render_ml_predictions(filters)


def render_summary_statistics(filters):
    """Render summary statistics"""
    
    st.subheader("📋 Summary Statistics")
    
    # Data source selection
    data_source = st.radio("Select Data Source", ["Global", "India"], horizontal=True)
    
    # Load data
    with st.spinner("Loading data..."):
        if data_source == "Global":
            data = load_data(
                'wb_poverty',
                indicator_code='SI.POV.DDAY',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
        else:
            data = load_data(
                'india_poverty',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
    
    data = clean_data(data)
    
    if data.empty:
        st.warning("No data available")
        return
    
    # Calculate summary statistics
    stats = get_summary_statistics(data['value'])
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mean", f"{stats['mean']:.2f}%")
        st.metric("Median", f"{stats['median']:.2f}%")
    
    with col2:
        st.metric("Std Dev", f"{stats['std']:.2f}")
        st.metric("Variance", f"{stats['variance']:.2f}")
    
    with col3:
        st.metric("Minimum", f"{stats['min']:.2f}%")
        st.metric("Maximum", f"{stats['max']:.2f}%")
    
    with col4:
        st.metric("25th Percentile", f"{stats['q25']:.2f}%")
        st.metric("75th Percentile", f"{stats['q75']:.2f}%")
    
    # Detailed statistics table
    st.markdown("#### Detailed Statistics")
    
    if data_source == "Global":
        group_cols = ['country_name'] if 'country_name' in data.columns else ['country']
    else:
        group_cols = ['state']
    
    if all(col in data.columns for col in group_cols):
        detailed_stats = data.groupby(group_cols)['value'].describe().round(2)
        st.dataframe(detailed_stats, use_container_width=True)
    
    # Distribution info
    st.markdown("#### Distribution Characteristics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Skewness", f"{stats.get('skewness', 0):.3f}")
        skew_interpretation = "Right-skewed" if stats.get('skewness', 0) > 0 else "Left-skewed" if stats.get('skewness', 0) < 0 else "Symmetric"
        st.caption(f"Distribution is {skew_interpretation}")
    
    with col2:
        st.metric("Kurtosis", f"{stats.get('kurtosis', 0):.3f}")
        kurt_interpretation = "Heavy-tailed" if stats.get('kurtosis', 0) > 0 else "Light-tailed" if stats.get('kurtosis', 0) < 0 else "Normal"
        st.caption(f"Distribution has {kurt_interpretation} tails")


def render_correlation_analysis(filters):
    """Render correlation analysis"""
    
    st.subheader("🔗 Correlation Analysis")
    
    st.info("Analyzing correlations between poverty indicators and other socioeconomic factors")
    
    # Load multi-indicator data
    with st.spinner("Loading indicator data..."):
        india_data = load_data('india_multi_indicator', 
                              start_year=filters['year_range'][0],
                              end_year=filters['year_range'][1])
    
    india_data = clean_data(india_data)
    
    if india_data.empty:
        st.warning("No data available")
        return
    
    # Pivot data for correlation analysis
    pivot_data = india_data.pivot_table(
        index=['state', 'year'],
        columns='indicator',
        values='value',
        aggfunc='mean'
    )
    
    # Correlation method selection
    corr_method = st.selectbox(
        "Correlation Method",
        options=config.CORRELATION_METHODS,
        format_func=lambda x: x.capitalize()
    )
    
    # Calculate correlation
    correlation_matrix = calculate_correlation(pivot_data, method=corr_method)
    
    # Display correlation heatmap
    st.markdown("#### Correlation Heatmap")
    fig = create_heatmap(
        correlation_matrix,
        title=f'Indicator Correlation Matrix ({corr_method.capitalize()})',
        color_scale='RdBu'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation table
    with st.expander("📋 View Correlation Values"):
        st.dataframe(correlation_matrix.round(3), use_container_width=True)
    
    # Key insights
    st.markdown("#### Key Insights")
    
    # Find strongest correlations
    corr_pairs = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_pairs.append({
                'Indicator 1': correlation_matrix.columns[i],
                'Indicator 2': correlation_matrix.columns[j],
                'Correlation': correlation_matrix.iloc[i, j]
            })
    
    corr_df = pd.DataFrame(corr_pairs).sort_values('Correlation', key=abs, ascending=False)
    
    st.markdown("**Strongest Positive Correlations:**")
    st.dataframe(corr_df.head(5), use_container_width=True, hide_index=True)
    
    st.markdown("**Strongest Negative Correlations:**")
    st.dataframe(corr_df.tail(5), use_container_width=True, hide_index=True)


def render_regression_analysis(filters):
    """Render regression analysis"""
    
    st.subheader("📈 Regression Analysis")
    
    st.markdown("Analyze the relationship between poverty and other variables")
    
    # Load data
    with st.spinner("Loading data..."):
        india_data = load_data('india_multi_indicator',
                              start_year=filters['year_range'][0],
                              end_year=filters['year_range'][1])
        demographics = load_data('india_demographics')
    
    india_data = clean_data(india_data)
    
    if india_data.empty:
        st.warning("No data available")
        return
    
    # Prepare data for regression
    latest_year = india_data['year'].max()
    latest_data = india_data[india_data['year'] == latest_year]
    
    # Pivot to get poverty rate
    poverty_data = latest_data[latest_data['indicator'] == 'Poverty Rate (%)'].copy()
    poverty_data = poverty_data.merge(demographics, on='state', how='left')
    
    # Variable selection
    col1, col2 = st.columns(2)
    
    with col1:
        dependent_var = st.selectbox("Dependent Variable (Y)", ['value'], format_func=lambda x: 'Poverty Rate')
    
    with col2:
        independent_vars = st.multiselect(
            "Independent Variables (X)",
            ['literacy_rate', 'gdp_per_capita', 'rural_population_pct'],
            default=['literacy_rate', 'gdp_per_capita']
        )
    
    if not independent_vars:
        st.info("Please select at least one independent variable")
        return
    
    # Perform regression
    X = poverty_data[independent_vars].fillna(poverty_data[independent_vars].median())
    y = poverty_data[dependent_var]
    
    regression_results = perform_regression(X, y)
    
    # Display results
    st.markdown("#### Regression Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("R² Score", f"{regression_results['r2_score']:.4f}")
    
    with col2:
        st.metric("Adjusted R²", f"{regression_results['adjusted_r2']:.4f}")
    
    with col3:
        st.metric("RMSE", f"{regression_results['rmse']:.4f}")
    
    # Coefficients
    st.markdown("#### Regression Coefficients")
    coef_df = pd.DataFrame({
        'Variable': independent_vars,
        'Coefficient': regression_results['coefficients'],
        'Interpretation': [f"{'Positive' if c > 0 else 'Negative'} relationship" for c in regression_results['coefficients']]
    })
    st.dataframe(coef_df, use_container_width=True, hide_index=True)
    
    # Scatter plot with regression line
    if len(independent_vars) >= 1:
        st.markdown("#### Scatter Plot with Regression Line")
        
        selected_x = st.selectbox("Select X variable for plot", independent_vars)
        
        fig = create_scatter_plot(
            poverty_data,
            x=selected_x,
            y='value',
            title=f'Poverty Rate vs {selected_x}',
            x_label=selected_x,
            y_label='Poverty Rate (%)',
            trendline='ols'
        )
        st.plotly_chart(fig, use_container_width=True)


def render_ml_predictions(filters):
    """Render machine learning predictions"""
    
    st.subheader("🤖 Machine Learning Predictions")
    
    st.markdown("Train models to predict future poverty rates")
    
    # Model selection
    model_type = st.selectbox("Select Model", config.ML_MODELS)
    
    # Data source
    data_source = st.radio("Data Source", ["Global", "India"], horizontal=True, key='ml_source')
    
    # Load data
    with st.spinner("Loading data..."):
        if data_source == "Global":
            data = load_data(
                'wb_poverty',
                indicator_code='SI.POV.DDAY',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
        else:
            data = load_data(
                'india_poverty',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
    
    data = clean_data(data)
    
    if data.empty:
        st.warning("No data available")
        return
    
    # Prepare features
    data_agg = data.groupby('year')['value'].mean().reset_index()
    
    # Train model
    with st.spinner(f"Training {model_type} model..."):
        model, metrics, predictions = train_model(
            data_agg,
            target='value',
            features=['year'],
            model_type=model_type
        )
    
    # Display metrics
    st.markdown("#### Model Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("R² Score", f"{metrics['r2']:.4f}")
    
    with col2:
        st.metric("RMSE", f"{metrics['rmse']:.4f}")
    
    with col3:
        st.metric("MAE", f"{metrics['mae']:.4f}")
    
    with col4:
        st.metric("MAPE", f"{metrics.get('mape', 0):.2f}%")
    
    # Future predictions
    st.markdown("#### Future Predictions")
    
    years_ahead = st.slider("Years to predict ahead", 1, 10, 5)
    
    future_predictions = predict_future(model, data_agg, years_ahead=years_ahead)
    
    # Combine historical and predictions
    combined_data = pd.concat([
        data_agg.assign(type='Historical'),
        future_predictions.assign(type='Predicted')
    ])
    
    # Plot
    fig = create_scatter_plot(
        combined_data,
        x='year',
        y='value',
        color='type',
        title='Historical Data and Future Predictions',
        x_label='Year',
        y_label='Poverty Rate (%)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Predictions table
    with st.expander("📋 View Prediction Details"):
        st.dataframe(future_predictions, use_container_width=True, hide_index=True)
    
    # Feature importance (for tree-based models)
    if model_type in ["Random Forest", "Gradient Boosting"]:
        st.markdown("#### Feature Importance")
        st.info("Feature importance analysis for tree-based models")
