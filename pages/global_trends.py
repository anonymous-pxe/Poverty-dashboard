"""
Global Trends Page - Worldwide poverty indicators visualization
"""

import streamlit as st
import pandas as pd
from data.data_loader import load_data
from data.preprocess import clean_data, filter_data
from utils.visualization import create_line_chart, create_bar_chart, create_choropleth_map
import config


def render(filters):
    """Render the global trends page"""
    
    st.title("🌍 Global Poverty Trends")
    st.markdown("Explore worldwide poverty indicators and trends across countries and regions")
    st.markdown("---")
    
    # Indicator selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_indicator = st.selectbox(
            "Select Poverty Indicator",
            options=[ind['code'] for ind in config.WB_POVERTY_INDICATORS],
            format_func=lambda x: next(
                (ind['name'] for ind in config.WB_POVERTY_INDICATORS if ind['code'] == x),
                x
            )
        )
    
    with col2:
        view_type = st.radio("View Type", ["Time Series", "Regional Comparison", "Country Ranking"])
    
    # Load data
    with st.spinner("Loading global data..."):
        wb_data = load_data(
            'wb_poverty',
            indicator_code=selected_indicator,
            start_year=filters['year_range'][0],
            end_year=filters['year_range'][1]
        )
        wb_metadata = load_data('wb_metadata')
    
    wb_data = clean_data(wb_data)
    
    if wb_data.empty:
        st.warning("No data available for selected filters")
        return
    
    # Merge with metadata
    wb_data = wb_data.merge(wb_metadata, left_on='country', right_on='country_code', how='left')
    
    st.markdown("---")
    
    # Render based on view type
    if view_type == "Time Series":
        render_time_series_view(wb_data, selected_indicator)
    elif view_type == "Regional Comparison":
        render_regional_comparison(wb_data, selected_indicator)
    elif view_type == "Country Ranking":
        render_country_ranking(wb_data, selected_indicator)
    
    # Summary statistics
    st.markdown("---")
    st.subheader("📊 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    latest_year = wb_data['year'].max()
    latest_data = wb_data[wb_data['year'] == latest_year]
    
    with col1:
        st.metric("Countries Tracked", wb_data['country'].nunique())
    
    with col2:
        st.metric("Average Poverty Rate", f"{latest_data['value'].mean():.2f}%")
    
    with col3:
        st.metric("Highest Rate", f"{latest_data['value'].max():.2f}%")
    
    with col4:
        st.metric("Lowest Rate", f"{latest_data['value'].min():.2f}%")


def render_time_series_view(wb_data, indicator):
    """Render time series visualization"""
    
    st.subheader("📈 Poverty Trends Over Time")
    
    # Country selection for detailed view
    countries = wb_data['country_name'].unique()
    selected_countries = st.multiselect(
        "Select countries to compare (leave empty for global average)",
        options=countries,
        default=[]
    )
    
    if selected_countries:
        # Show selected countries
        plot_data = wb_data[wb_data['country_name'].isin(selected_countries)]
        
        fig = create_line_chart(
            plot_data,
            x='year',
            y='value',
            color='country_name',
            title=f'Poverty Rate Comparison: {", ".join(selected_countries[:3])}{"..." if len(selected_countries) > 3 else ""}',
            x_label='Year',
            y_label='Poverty Rate (%)'
        )
    else:
        # Show global average
        global_avg = wb_data.groupby('year')['value'].mean().reset_index()
        
        fig = create_line_chart(
            global_avg,
            x='year',
            y='value',
            title='Global Average Poverty Rate',
            x_label='Year',
            y_label='Poverty Rate (%)'
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data table
    with st.expander("📋 View Data Table"):
        if selected_countries:
            display_data = plot_data[['country_name', 'year', 'value', 'region']].sort_values(['country_name', 'year'])
        else:
            display_data = global_avg
        st.dataframe(display_data, use_container_width=True, hide_index=True)


def render_regional_comparison(wb_data, indicator):
    """Render regional comparison"""
    
    st.subheader("🗺️ Regional Poverty Comparison")
    
    # Aggregate by region and year
    regional_data = wb_data.groupby(['region', 'year'])['value'].mean().reset_index()
    
    # Create area chart for regions
    fig = create_line_chart(
        regional_data,
        x='year',
        y='value',
        color='region',
        title='Poverty Rates by Region',
        x_label='Year',
        y_label='Average Poverty Rate (%)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Latest year comparison
    st.subheader("📊 Latest Regional Comparison")
    
    latest_year = regional_data['year'].max()
    latest_regional = regional_data[regional_data['year'] == latest_year].sort_values('value', ascending=False)
    
    fig = create_bar_chart(
        latest_regional,
        x='region',
        y='value',
        title=f'Poverty Rates by Region ({latest_year})',
        x_label='Region',
        y_label='Poverty Rate (%)',
        orientation='v'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional statistics table
    with st.expander("📋 Regional Statistics"):
        regional_stats = wb_data.groupby('region')['value'].agg(['mean', 'min', 'max', 'std']).round(2)
        regional_stats.columns = ['Average', 'Minimum', 'Maximum', 'Std Dev']
        st.dataframe(regional_stats, use_container_width=True)


def render_country_ranking(wb_data, indicator):
    """Render country ranking"""
    
    st.subheader("🏆 Country Rankings")
    
    # Year selection
    year_options = sorted(wb_data['year'].unique(), reverse=True)
    selected_year = st.selectbox("Select Year", options=year_options, index=0)
    
    # Filter data for selected year
    year_data = wb_data[wb_data['year'] == selected_year].sort_values('value', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔴 Top 10 Highest Poverty Rates")
        highest = year_data.head(10)
        fig_high = create_bar_chart(
            highest,
            x='country_name',
            y='value',
            title=f'Highest Poverty Rates ({selected_year})',
            x_label='Country',
            y_label='Poverty Rate (%)',
            orientation='v',
            color=config.COLOR_SCHEME['danger']
        )
        st.plotly_chart(fig_high, use_container_width=True)
    
    with col2:
        st.markdown("#### 🟢 Top 10 Lowest Poverty Rates")
        lowest = year_data.tail(10).sort_values('value', ascending=True)
        fig_low = create_bar_chart(
            lowest,
            x='country_name',
            y='value',
            title=f'Lowest Poverty Rates ({selected_year})',
            x_label='Country',
            y_label='Poverty Rate (%)',
            orientation='v',
            color=config.COLOR_SCHEME['success']
        )
        st.plotly_chart(fig_low, use_container_width=True)
    
    # Full ranking table
    with st.expander("📋 Full Country Rankings"):
        ranking_data = year_data[['country_name', 'region', 'income_level', 'value']].reset_index(drop=True)
        ranking_data.index += 1
        ranking_data.columns = ['Country', 'Region', 'Income Level', 'Poverty Rate (%)']
        st.dataframe(ranking_data, use_container_width=True)
