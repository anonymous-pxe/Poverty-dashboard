"""
Visualization Page - Interactive charts and maps
"""

import streamlit as st
import pandas as pd
from data.data_loader import load_data
from data.preprocess import clean_data, filter_data
from utils.visualization import (
    create_line_chart, create_bar_chart, create_pie_chart,
    create_scatter_plot, create_box_plot, create_choropleth_map
)
import config


def render(filters):
    """Render the visualization page"""
    
    st.title("📊 Data Visualization")
    st.markdown("Explore poverty data through interactive charts and maps")
    st.markdown("---")
    
    # Visualization type selection
    viz_type = st.selectbox(
        "Select Visualization Type",
        [
            "Line Chart",
            "Bar Chart",
            "Scatter Plot",
            "Box Plot",
            "Pie Chart",
            "Geographic Map"
        ]
    )
    
    st.markdown("---")
    
    # Render appropriate visualization
    if viz_type == "Line Chart":
        render_line_chart(filters)
    elif viz_type == "Bar Chart":
        render_bar_chart(filters)
    elif viz_type == "Scatter Plot":
        render_scatter_plot_viz(filters)
    elif viz_type == "Box Plot":
        render_box_plot_viz(filters)
    elif viz_type == "Pie Chart":
        render_pie_chart(filters)
    elif viz_type == "Geographic Map":
        render_geographic_map(filters)


def render_line_chart(filters):
    """Render line chart visualization"""
    
    st.subheader("📈 Line Chart")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_source = st.radio("Data Source", ["Global", "India"], horizontal=True, key='line_source')
    
    with col2:
        group_by = st.radio("Group By", ["None", "Category"], horizontal=True, key='line_group')
    
    # Load data
    with st.spinner("Loading data..."):
        if data_source == "Global":
            data = load_data(
                'wb_poverty',
                indicator_code='SI.POV.DDAY',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            category_col = 'country_name' if 'country_name' in data.columns else 'country'
        else:
            data = load_data(
                'india_poverty',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            category_col = 'state'
    
    data = clean_data(data)
    
    if data.empty:
        st.warning("No data available")
        return
    
    # Category selection if grouping
    if group_by == "Category":
        categories = st.multiselect(
            f"Select {category_col}s",
            options=sorted(data[category_col].unique()),
            default=sorted(data[category_col].unique())[:5]
        )
        
        if categories:
            data = data[data[category_col].isin(categories)]
            
            fig = create_line_chart(
                data,
                x='year',
                y='value',
                color=category_col,
                title=f'Poverty Rate Trends',
                x_label='Year',
                y_label='Poverty Rate (%)'
            )
        else:
            st.info("Please select at least one category")
            return
    else:
        # Aggregate data
        agg_data = data.groupby('year')['value'].mean().reset_index()
        
        fig = create_line_chart(
            agg_data,
            x='year',
            y='value',
            title='Average Poverty Rate Over Time',
            x_label='Year',
            y_label='Poverty Rate (%)'
        )
    
    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(filters):
    """Render bar chart visualization"""
    
    st.subheader("📊 Bar Chart")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data_source = st.radio("Data Source", ["Global", "India"], horizontal=True, key='bar_source')
    
    with col2:
        orientation = st.radio("Orientation", ["Vertical", "Horizontal"], horizontal=True, key='bar_orient')
    
    with col3:
        top_n = st.slider("Show Top N", 5, 30, 15, key='bar_topn')
    
    # Load data
    with st.spinner("Loading data..."):
        if data_source == "Global":
            data = load_data(
                'wb_poverty',
                indicator_code='SI.POV.DDAY',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            category_col = 'country_name' if 'country_name' in data.columns else 'country'
        else:
            data = load_data(
                'india_poverty',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            category_col = 'state'
    
    data = clean_data(data)
    
    if data.empty:
        st.warning("No data available")
        return
    
    # Get latest year data
    latest_year = data['year'].max()
    latest_data = data[data['year'] == latest_year].sort_values('value', ascending=False).head(top_n)
    
    fig = create_bar_chart(
        latest_data,
        x=category_col if orientation == "Vertical" else 'value',
        y='value' if orientation == "Vertical" else category_col,
        title=f'Top {top_n} Poverty Rates ({latest_year})',
        x_label=category_col if orientation == "Vertical" else 'Poverty Rate (%)',
        y_label='Poverty Rate (%)' if orientation == "Vertical" else category_col,
        orientation='v' if orientation == "Vertical" else 'h'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_scatter_plot_viz(filters):
    """Render scatter plot visualization"""
    
    st.subheader("🔵 Scatter Plot")
    
    st.markdown("Analyze relationships between different indicators")
    
    # Load multi-indicator data
    with st.spinner("Loading data..."):
        india_data = load_data('india_multi_indicator',
                              start_year=filters['year_range'][0],
                              end_year=filters['year_range'][1])
        demographics = load_data('india_demographics')
    
    india_data = clean_data(india_data)
    
    if india_data.empty:
        st.warning("No data available")
        return
    
    # Prepare data
    latest_year = india_data['year'].max()
    latest_data = india_data[india_data['year'] == latest_year]
    
    # Pivot to get different indicators as columns
    pivot_data = latest_data.pivot_table(
        index='state',
        columns='indicator',
        values='value',
        aggfunc='mean'
    ).reset_index()
    
    # Merge with demographics
    pivot_data = pivot_data.merge(demographics, on='state', how='left')
    
    # Variable selection
    col1, col2 = st.columns(2)
    
    available_cols = [col for col in pivot_data.columns if col != 'state']
    
    with col1:
        x_var = st.selectbox("X-axis Variable", available_cols, index=0 if available_cols else None)
    
    with col2:
        y_var = st.selectbox("Y-axis Variable", available_cols, index=1 if len(available_cols) > 1 else 0)
    
    if x_var and y_var:
        fig = create_scatter_plot(
            pivot_data,
            x=x_var,
            y=y_var,
            title=f'{y_var} vs {x_var}',
            x_label=x_var,
            y_label=y_var,
            hover_name='state',
            trendline='ols'
        )
        st.plotly_chart(fig, use_container_width=True)


def render_box_plot_viz(filters):
    """Render box plot visualization"""
    
    st.subheader("📦 Box Plot")
    
    data_source = st.radio("Data Source", ["Global", "India"], horizontal=True, key='box_source')
    
    # Load data
    with st.spinner("Loading data..."):
        if data_source == "Global":
            data = load_data(
                'wb_poverty',
                indicator_code='SI.POV.DDAY',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            data = data.merge(load_data('wb_metadata'), left_on='country', right_on='country_code', how='left')
            group_col = 'region'
        else:
            data = load_data(
                'india_poverty',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            group_col = 'area_type'
    
    data = clean_data(data)
    
    if data.empty or group_col not in data.columns:
        st.warning("No data available")
        return
    
    # Get latest year
    latest_year = data['year'].max()
    latest_data = data[data['year'] == latest_year]
    
    fig = create_box_plot(
        latest_data,
        x=group_col,
        y='value',
        title=f'Poverty Rate Distribution by {group_col} ({latest_year})',
        x_label=group_col,
        y_label='Poverty Rate (%)'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_pie_chart(filters):
    """Render pie chart visualization"""
    
    st.subheader("🥧 Pie Chart")
    
    st.markdown("Distribution of poverty across categories")
    
    # Load India data for pie chart
    with st.spinner("Loading data..."):
        india_data = load_data(
            'india_poverty',
            start_year=filters['year_range'][0],
            end_year=filters['year_range'][1]
        )
    
    india_data = clean_data(india_data)
    
    if india_data.empty:
        st.warning("No data available")
        return
    
    # Get latest year
    latest_year = india_data['year'].max()
    latest_data = india_data[india_data['year'] == latest_year]
    
    # Categorize poverty levels
    latest_data['poverty_level'] = pd.cut(
        latest_data['value'],
        bins=[0, 10, 20, 30, 100],
        labels=['Low (<10%)', 'Medium (10-20%)', 'High (20-30%)', 'Very High (>30%)']
    )
    
    # Count by category
    pie_data = latest_data.groupby('poverty_level').size().reset_index(name='count')
    
    fig = create_pie_chart(
        pie_data,
        values='count',
        names='poverty_level',
        title=f'Distribution of Poverty Levels ({latest_year})'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_geographic_map(filters):
    """Render geographic map visualization"""
    
    st.subheader("🗺️ Geographic Map")
    
    st.markdown("Interactive map showing poverty rates across Indian states")
    
    # Load India data
    with st.spinner("Loading data..."):
        india_data = load_data(
            'india_poverty',
            start_year=filters['year_range'][0],
            end_year=filters['year_range'][1],
            area_type=filters.get('area_type', 'All')
        )
    
    india_data = clean_data(india_data)
    
    if india_data.empty:
        st.warning("No data available")
        return
    
    # Year selection
    year_options = sorted(india_data['year'].unique(), reverse=True)
    selected_year = st.selectbox("Select Year", options=year_options, index=0, key='map_year')
    
    # Filter data
    map_data = india_data[india_data['year'] == selected_year]
    
    # Aggregate by state if needed
    if 'area_type' in map_data.columns:
        map_data = map_data.groupby('state')['value'].mean().reset_index()
    
    # Create choropleth map
    fig = create_choropleth_map(
        map_data,
        locations='state',
        values='value',
        title=f'Poverty Rate by State ({selected_year})',
        color_scale='Reds'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Map legend
    st.markdown("#### Map Legend")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("🟢 **Low**: < 15%")
    with col2:
        st.markdown("🟡 **Medium**: 15-30%")
    with col3:
        st.markdown("🔴 **High**: > 30%")
