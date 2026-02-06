"""
Dashboard Page - Overview with KPIs and Highlights
"""

import streamlit as st
import pandas as pd
from data.data_loader import load_data
from data.preprocess import filter_data, clean_data
from components.metrics import render_kpi_cards
from utils.visualization import create_line_chart, create_bar_chart
import config


def render(filters):
    """Render the dashboard overview page"""
    
    st.title("📊 Poverty Dashboard Overview")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading data..."):
        wb_data = load_data(
            'wb_poverty',
            indicator_code='SI.POV.DDAY',
            start_year=filters['year_range'][0],
            end_year=filters['year_range'][1]
        )
        
        india_data = load_data(
            'india_poverty',
            start_year=filters['year_range'][0],
            end_year=filters['year_range'][1],
            states=filters.get('states'),
            area_type=filters.get('area_type', 'All')
        )
    
    # Clean data
    wb_data = clean_data(wb_data)
    india_data = clean_data(india_data)
    
    # Calculate KPIs
    st.subheader("📈 Key Performance Indicators")
    
    kpi_data = calculate_kpis(wb_data, india_data, filters)
    render_kpi_cards(kpi_data)
    
    st.markdown("---")
    
    # Two-column layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌍 Global Poverty Trends")
        if not wb_data.empty:
            # Aggregate global data by year
            global_trend = wb_data.groupby('year')['value'].mean().reset_index()
            fig = create_line_chart(
                global_trend,
                x='year',
                y='value',
                title='Average Global Poverty Rate Over Time',
                x_label='Year',
                y_label='Poverty Rate (%)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No global data available for selected filters")
    
    with col2:
        st.subheader("🇮🇳 India Poverty Trends")
        if not india_data.empty:
            # Aggregate India data by year
            india_trend = india_data.groupby('year')['value'].mean().reset_index()
            fig = create_line_chart(
                india_trend,
                x='year',
                y='value',
                title='Average India Poverty Rate Over Time',
                x_label='Year',
                y_label='Poverty Rate (%)',
                color=config.COLOR_SCHEME['secondary']
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No India data available for selected filters")
    
    st.markdown("---")
    
    # Highlights section
    st.subheader("💡 Key Insights")
    render_highlights(wb_data, india_data, filters)
    
    # Recent data table
    st.markdown("---")
    st.subheader("📋 Recent Data Summary")
    
    tab1, tab2 = st.tabs(["Global Data", "India Data"])
    
    with tab1:
        if not wb_data.empty:
            recent_year = wb_data['year'].max()
            recent_data = wb_data[wb_data['year'] == recent_year].sort_values('value', ascending=False)
            st.dataframe(
                recent_data[['country_name', 'year', 'value']].head(20),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No data available")
    
    with tab2:
        if not india_data.empty:
            recent_year = india_data['year'].max()
            recent_data = india_data[india_data['year'] == recent_year].sort_values('value', ascending=False)
            st.dataframe(
                recent_data[['state', 'area_type', 'year', 'value']].head(20),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No data available")


def calculate_kpis(wb_data, india_data, filters):
    """Calculate key performance indicators"""
    
    kpis = {
        'global_avg': 0,
        'global_change': 0,
        'india_avg': 0,
        'india_change': 0,
        'total_countries': 0,
        'total_states': 0
    }
    
    if not wb_data.empty:
        latest_year = wb_data['year'].max()
        kpis['global_avg'] = wb_data[wb_data['year'] == latest_year]['value'].mean()
        kpis['total_countries'] = wb_data['country'].nunique()
        
        # Calculate year-over-year change
        if latest_year > wb_data['year'].min():
            prev_year = latest_year - 1
            if prev_year in wb_data['year'].values:
                prev_avg = wb_data[wb_data['year'] == prev_year]['value'].mean()
                kpis['global_change'] = ((kpis['global_avg'] - prev_avg) / prev_avg) * 100
    
    if not india_data.empty:
        latest_year = india_data['year'].max()
        kpis['india_avg'] = india_data[india_data['year'] == latest_year]['value'].mean()
        kpis['total_states'] = india_data['state'].nunique()
        
        # Calculate year-over-year change
        if latest_year > india_data['year'].min():
            prev_year = latest_year - 1
            if prev_year in india_data['year'].values:
                prev_avg = india_data[india_data['year'] == prev_year]['value'].mean()
                kpis['india_change'] = ((kpis['india_avg'] - prev_avg) / prev_avg) * 100
    
    return kpis


def render_highlights(wb_data, india_data, filters):
    """Render key highlights and insights"""
    
    insights = []
    
    # Global insights
    if not wb_data.empty:
        latest_year = wb_data['year'].max()
        latest_data = wb_data[wb_data['year'] == latest_year]
        
        highest_country = latest_data.nlargest(1, 'value')
        lowest_country = latest_data.nsmallest(1, 'value')
        
        if not highest_country.empty:
            insights.append(
                f"🔴 **Highest global poverty rate**: {highest_country.iloc[0]['country_name']} "
                f"({highest_country.iloc[0]['value']:.2f}%)"
            )
        
        if not lowest_country.empty:
            insights.append(
                f"🟢 **Lowest global poverty rate**: {lowest_country.iloc[0]['country_name']} "
                f"({lowest_country.iloc[0]['value']:.2f}%)"
            )
    
    # India insights
    if not india_data.empty:
        latest_year = india_data['year'].max()
        latest_data = india_data[india_data['year'] == latest_year]
        
        highest_state = latest_data.nlargest(1, 'value')
        lowest_state = latest_data.nsmallest(1, 'value')
        
        if not highest_state.empty:
            insights.append(
                f"🔴 **Highest India poverty rate**: {highest_state.iloc[0]['state']} "
                f"({highest_state.iloc[0]['area_type']}) - {highest_state.iloc[0]['value']:.2f}%"
            )
        
        if not lowest_state.empty:
            insights.append(
                f"🟢 **Lowest India poverty rate**: {lowest_state.iloc[0]['state']} "
                f"({lowest_state.iloc[0]['area_type']}) - {lowest_state.iloc[0]['value']:.2f}%"
            )
        
        # Rural vs Urban insight
        rural_avg = latest_data[latest_data['area_type'] == 'Rural']['value'].mean()
        urban_avg = latest_data[latest_data['area_type'] == 'Urban']['value'].mean()
        
        if rural_avg > urban_avg:
            diff = rural_avg - urban_avg
            insights.append(
                f"📊 **Rural-Urban gap**: Rural areas have {diff:.2f}% higher poverty rate than urban areas"
            )
    
    # Display insights
    if insights:
        for insight in insights:
            st.markdown(insight)
    else:
        st.info("No insights available for current filters")
