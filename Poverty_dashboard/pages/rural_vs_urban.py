"""
Rural vs Urban Page - Comparison of poverty rates by area type
"""

import streamlit as st
import pandas as pd
from data.data_loader import load_data
from data.preprocess import clean_data, filter_data
from utils.visualization import create_line_chart, create_bar_chart, create_box_plot
import config


def render(filters):
    """Render the rural vs urban comparison page"""
    
    st.title("🏘️ Rural vs Urban Poverty Comparison")
    st.markdown("Compare poverty rates between rural and urban areas across Indian states")
    st.markdown("---")
    
    # Load India data
    with st.spinner("Loading India poverty data..."):
        india_data = load_data(
            'india_poverty',
            start_year=filters['year_range'][0],
            end_year=filters['year_range'][1],
            states=filters.get('states'),
            area_type='All'  # Load both rural and urban
        )
    
    india_data = clean_data(india_data)
    
    if india_data.empty:
        st.warning("No data available for selected filters")
        return
    
    # Overview metrics
    st.subheader("📊 Overview")
    render_overview_metrics(india_data)
    
    st.markdown("---")
    
    # Visualization tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Time Trends",
        "State Comparison",
        "Distribution Analysis",
        "Gap Analysis"
    ])
    
    with tab1:
        render_time_trends(india_data)
    
    with tab2:
        render_state_comparison(india_data)
    
    with tab3:
        render_distribution_analysis(india_data)
    
    with tab4:
        render_gap_analysis(india_data)


def render_overview_metrics(india_data):
    """Render overview metrics comparing rural and urban"""
    
    latest_year = india_data['year'].max()
    latest_data = india_data[india_data['year'] == latest_year]
    
    rural_data = latest_data[latest_data['area_type'] == 'Rural']
    urban_data = latest_data[latest_data['area_type'] == 'Urban']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        rural_avg = rural_data['value'].mean()
        st.metric("Rural Average", f"{rural_avg:.2f}%")
    
    with col2:
        urban_avg = urban_data['value'].mean()
        st.metric("Urban Average", f"{urban_avg:.2f}%")
    
    with col3:
        gap = rural_avg - urban_avg
        st.metric("Rural-Urban Gap", f"{gap:.2f}%", delta=f"{gap:.2f}%", delta_color="inverse")
    
    with col4:
        states_count = india_data['state'].nunique()
        st.metric("States Tracked", states_count)


def render_time_trends(india_data):
    """Render time trends comparison"""
    
    st.subheader("📈 Poverty Rate Trends Over Time")
    
    # Aggregate by area type and year
    trend_data = india_data.groupby(['area_type', 'year'])['value'].mean().reset_index()
    
    fig = create_line_chart(
        trend_data,
        x='year',
        y='value',
        color='area_type',
        title='Rural vs Urban Poverty Trends',
        x_label='Year',
        y_label='Average Poverty Rate (%)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # State-specific trends
    st.markdown("#### State-Specific Trends")
    
    states = sorted(india_data['state'].unique())
    selected_states = st.multiselect(
        "Select states to compare",
        options=states,
        default=states[:3] if len(states) >= 3 else states
    )
    
    if selected_states:
        state_data = india_data[india_data['state'].isin(selected_states)]
        
        # Create a combined column for better legend
        state_data['state_area'] = state_data['state'] + ' - ' + state_data['area_type']
        
        fig = create_line_chart(
            state_data,
            x='year',
            y='value',
            color='state_area',
            title=f'Poverty Trends: {", ".join(selected_states)}',
            x_label='Year',
            y_label='Poverty Rate (%)'
        )
        st.plotly_chart(fig, use_container_width=True)


def render_state_comparison(india_data):
    """Render state-by-state comparison"""
    
    st.subheader("🗺️ State-by-State Comparison")
    
    # Year selection
    year_options = sorted(india_data['year'].unique(), reverse=True)
    selected_year = st.selectbox("Select Year", options=year_options, index=0, key='state_comp_year')
    
    year_data = india_data[india_data['year'] == selected_year]
    
    # Pivot data for side-by-side comparison
    pivot_data = year_data.pivot_table(
        index='state',
        columns='area_type',
        values='value',
        aggfunc='mean'
    ).reset_index()
    
    # Sort by rural poverty rate
    pivot_data = pivot_data.sort_values('Rural', ascending=False)
    
    # Create grouped bar chart
    fig = create_bar_chart(
        year_data,
        x='state',
        y='value',
        color='area_type',
        title=f'Rural vs Urban Poverty by State ({selected_year})',
        x_label='State',
        y_label='Poverty Rate (%)',
        orientation='v',
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    with st.expander("📋 View State Data Table"):
        if 'Rural' in pivot_data.columns and 'Urban' in pivot_data.columns:
            pivot_data['Gap'] = pivot_data['Rural'] - pivot_data['Urban']
            pivot_data = pivot_data.round(2)
        st.dataframe(pivot_data, use_container_width=True, hide_index=True)


def render_distribution_analysis(india_data):
    """Render distribution analysis"""
    
    st.subheader("📊 Distribution Analysis")
    
    latest_year = india_data['year'].max()
    latest_data = india_data[india_data['year'] == latest_year]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Box Plot Analysis")
        fig = create_box_plot(
            latest_data,
            x='area_type',
            y='value',
            title=f'Poverty Rate Distribution ({latest_year})',
            x_label='Area Type',
            y_label='Poverty Rate (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Statistical Summary")
        
        summary_stats = latest_data.groupby('area_type')['value'].describe().round(2)
        st.dataframe(summary_stats, use_container_width=True)
    
    # Histogram comparison
    st.markdown("#### Distribution Histogram")
    
    import plotly.graph_objects as go
    
    rural_values = latest_data[latest_data['area_type'] == 'Rural']['value']
    urban_values = latest_data[latest_data['area_type'] == 'Urban']['value']
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=rural_values,
        name='Rural',
        opacity=0.7,
        marker_color=config.COLOR_SCHEME['rural']
    ))
    fig.add_trace(go.Histogram(
        x=urban_values,
        name='Urban',
        opacity=0.7,
        marker_color=config.COLOR_SCHEME['urban']
    ))
    
    fig.update_layout(
        title='Poverty Rate Distribution Comparison',
        xaxis_title='Poverty Rate (%)',
        yaxis_title='Frequency',
        barmode='overlay',
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_gap_analysis(india_data):
    """Render rural-urban gap analysis"""
    
    st.subheader("📉 Rural-Urban Poverty Gap Analysis")
    
    # Calculate gap for each state and year
    rural_data = india_data[india_data['area_type'] == 'Rural'].copy()
    urban_data = india_data[india_data['area_type'] == 'Urban'].copy()
    
    # Merge and calculate gap
    gap_data = rural_data.merge(
        urban_data,
        on=['state', 'year'],
        suffixes=('_rural', '_urban')
    )
    gap_data['gap'] = gap_data['value_rural'] - gap_data['value_urban']
    
    # Gap trends over time
    st.markdown("#### Gap Trends Over Time")
    
    avg_gap = gap_data.groupby('year')['gap'].mean().reset_index()
    
    fig = create_line_chart(
        avg_gap,
        x='year',
        y='gap',
        title='Average Rural-Urban Poverty Gap Over Time',
        x_label='Year',
        y_label='Gap (Percentage Points)',
        color=config.COLOR_SCHEME['warning']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # States with largest gaps
    st.markdown("#### States with Largest Gaps")
    
    latest_year = gap_data['year'].max()
    latest_gaps = gap_data[gap_data['year'] == latest_year].sort_values('gap', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Top 10 Largest Gaps")
        top_gaps = latest_gaps.head(10)
        fig = create_bar_chart(
            top_gaps,
            x='state',
            y='gap',
            title=f'Largest Rural-Urban Gaps ({latest_year})',
            x_label='State',
            y_label='Gap (Percentage Points)',
            orientation='v',
            color=config.COLOR_SCHEME['danger']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### Top 10 Smallest Gaps")
        bottom_gaps = latest_gaps.tail(10).sort_values('gap')
        fig = create_bar_chart(
            bottom_gaps,
            x='state',
            y='gap',
            title=f'Smallest Rural-Urban Gaps ({latest_year})',
            x_label='State',
            y_label='Gap (Percentage Points)',
            orientation='v',
            color=config.COLOR_SCHEME['success']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Gap data table
    with st.expander("📋 View Complete Gap Analysis"):
        gap_table = latest_gaps[['state', 'value_rural', 'value_urban', 'gap']].copy()
        gap_table.columns = ['State', 'Rural Rate (%)', 'Urban Rate (%)', 'Gap (pp)']
        gap_table = gap_table.round(2)
        st.dataframe(gap_table, use_container_width=True, hide_index=True)
