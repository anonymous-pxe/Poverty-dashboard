"""
Reports Page - Data downloads and PDF generation
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from data.data_loader import load_data
from data.preprocess import clean_data
from utils.pdf_generator import generate_pdf_report
import config


def render(filters):
    """Render the reports page"""
    
    st.title("📄 Reports & Downloads")
    st.markdown("Generate reports and download data in various formats")
    st.markdown("---")
    
    # Report type selection
    report_tabs = st.tabs([
        "Data Export",
        "PDF Reports",
        "Summary Reports"
    ])
    
    with report_tabs[0]:
        render_data_export(filters)
    
    with report_tabs[1]:
        render_pdf_reports(filters)
    
    with report_tabs[2]:
        render_summary_reports(filters)


def render_data_export(filters):
    """Render data export section"""
    
    st.subheader("💾 Data Export")
    
    st.markdown("Download filtered data in CSV or Excel format")
    
    # Data source selection
    col1, col2 = st.columns(2)
    
    with col1:
        data_source = st.selectbox(
            "Select Data Source",
            ["Global Poverty Data", "India Poverty Data", "India Demographics", "All Data"]
        )
    
    with col2:
        file_format = st.radio("File Format", ["CSV", "Excel"], horizontal=True)
    
    # Load data based on selection
    with st.spinner("Loading data..."):
        if data_source == "Global Poverty Data":
            data = load_data(
                'wb_poverty',
                indicator_code='SI.POV.DDAY',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            filename = "global_poverty_data"
        
        elif data_source == "India Poverty Data":
            data = load_data(
                'india_poverty',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            filename = "india_poverty_data"
        
        elif data_source == "India Demographics":
            data = load_data('india_demographics')
            filename = "india_demographics"
        
        else:  # All Data
            wb_data = load_data(
                'wb_poverty',
                indicator_code='SI.POV.DDAY',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            india_data = load_data(
                'india_poverty',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            # For "All Data", we'll export both as separate sheets (Excel) or combined (CSV)
            data = {'global': wb_data, 'india': india_data}
            filename = "all_poverty_data"
    
    if isinstance(data, pd.DataFrame):
        data = clean_data(data)
        
        # Preview data
        st.markdown("#### Data Preview")
        st.dataframe(data.head(100), use_container_width=True)
        
        # Download button
        st.markdown("#### Download")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if file_format == "CSV":
            csv = data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{filename}_{timestamp}.csv",
                mime="text/csv"
            )
        
        else:  # Excel
            # Create Excel file in memory
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, sheet_name='Data', index=False)
            
            st.download_button(
                label="📥 Download Excel",
                data=output.getvalue(),
                file_name=f"{filename}_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    elif isinstance(data, dict):
        # Multiple datasets
        st.markdown("#### Data Preview")
        
        for key, df in data.items():
            with st.expander(f"Preview {key.capitalize()} Data"):
                st.dataframe(clean_data(df).head(100), use_container_width=True)
        
        # Download
        st.markdown("#### Download")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if file_format == "CSV":
            # Combine all data for CSV
            combined = pd.concat([df.assign(source=key) for key, df in data.items()], ignore_index=True)
            csv = combined.to_csv(index=False)
            st.download_button(
                label="📥 Download Combined CSV",
                data=csv,
                file_name=f"{filename}_{timestamp}.csv",
                mime="text/csv"
            )
        
        else:  # Excel with multiple sheets
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for key, df in data.items():
                    clean_data(df).to_excel(writer, sheet_name=key.capitalize(), index=False)
            
            st.download_button(
                label="📥 Download Excel (Multiple Sheets)",
                data=output.getvalue(),
                file_name=f"{filename}_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


def render_pdf_reports(filters):
    """Render PDF report generation"""
    
    st.subheader("📑 PDF Reports")
    
    st.markdown("Generate comprehensive PDF reports with charts and analysis")
    
    # Report type
    report_type = st.selectbox(
        "Select Report Type",
        [
            "Executive Summary",
            "Detailed Analysis",
            "State-wise Report",
            "Comparative Report"
        ]
    )
    
    # Report configuration
    st.markdown("#### Report Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_charts = st.checkbox("Include Charts", value=True)
        include_tables = st.checkbox("Include Data Tables", value=True)
    
    with col2:
        include_statistics = st.checkbox("Include Statistics", value=True)
        include_insights = st.checkbox("Include Key Insights", value=True)
    
    # Generate button
    if st.button("🔄 Generate PDF Report", type="primary"):
        with st.spinner("Generating PDF report..."):
            # Load necessary data
            wb_data = load_data(
                'wb_poverty',
                indicator_code='SI.POV.DDAY',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            
            india_data = load_data(
                'india_poverty',
                start_year=filters['year_range'][0],
                end_year=filters['year_range'][1]
            )
            
            # Generate report
            report_config = {
                'report_type': report_type,
                'include_charts': include_charts,
                'include_tables': include_tables,
                'include_statistics': include_statistics,
                'include_insights': include_insights,
                'filters': filters
            }
            
            pdf_path = generate_pdf_report(
                wb_data=clean_data(wb_data),
                india_data=clean_data(india_data),
                config=report_config
            )
            
            if pdf_path and Path(pdf_path).exists():
                st.success("✅ PDF report generated successfully!")
                
                # Read and offer download
                with open(pdf_path, 'rb') as f:
                    pdf_bytes = f.read()
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"poverty_report_{timestamp}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Failed to generate PDF report")


def render_summary_reports(filters):
    """Render summary reports"""
    
    st.subheader("📊 Summary Reports")
    
    st.markdown("Quick summary statistics and insights")
    
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
            end_year=filters['year_range'][1]
        )
    
    wb_data = clean_data(wb_data)
    india_data = clean_data(india_data)
    
    # Global summary
    st.markdown("### 🌍 Global Summary")
    
    if not wb_data.empty:
        latest_year = wb_data['year'].max()
        latest_global = wb_data[wb_data['year'] == latest_year]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Countries", wb_data['country'].nunique())
        
        with col2:
            st.metric("Avg Poverty Rate", f"{latest_global['value'].mean():.2f}%")
        
        with col3:
            st.metric("Highest Rate", f"{latest_global['value'].max():.2f}%")
        
        with col4:
            st.metric("Lowest Rate", f"{latest_global['value'].min():.2f}%")
        
        # Top/Bottom countries
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 5 Highest")
            top5 = latest_global.nlargest(5, 'value')[['country_name', 'value']]
            top5.columns = ['Country', 'Rate (%)']
            st.dataframe(top5, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Top 5 Lowest")
            bottom5 = latest_global.nsmallest(5, 'value')[['country_name', 'value']]
            bottom5.columns = ['Country', 'Rate (%)']
            st.dataframe(bottom5, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # India summary
    st.markdown("### 🇮🇳 India Summary")
    
    if not india_data.empty:
        latest_year = india_data['year'].max()
        latest_india = india_data[india_data['year'] == latest_year]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("States", india_data['state'].nunique())
        
        with col2:
            st.metric("Avg Poverty Rate", f"{latest_india['value'].mean():.2f}%")
        
        with col3:
            rural_avg = latest_india[latest_india['area_type'] == 'Rural']['value'].mean()
            st.metric("Rural Average", f"{rural_avg:.2f}%")
        
        with col4:
            urban_avg = latest_india[latest_india['area_type'] == 'Urban']['value'].mean()
            st.metric("Urban Average", f"{urban_avg:.2f}%")
        
        # Top/Bottom states
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 5 Highest")
            top5_india = latest_india.nlargest(5, 'value')[['state', 'area_type', 'value']]
            top5_india.columns = ['State', 'Area', 'Rate (%)']
            st.dataframe(top5_india, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Top 5 Lowest")
            bottom5_india = latest_india.nsmallest(5, 'value')[['state', 'area_type', 'value']]
            bottom5_india.columns = ['State', 'Area', 'Rate (%)']
            st.dataframe(bottom5_india, use_container_width=True, hide_index=True)
    
    # Export summary as text
    st.markdown("---")
    
    if st.button("📋 Copy Summary to Clipboard"):
        summary_text = f"""
POVERTY DASHBOARD SUMMARY REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

GLOBAL STATISTICS ({latest_year if not wb_data.empty else 'N/A'})
- Countries tracked: {wb_data['country'].nunique() if not wb_data.empty else 'N/A'}
- Average poverty rate: {latest_global['value'].mean():.2f}% if not wb_data.empty else 'N/A'

INDIA STATISTICS ({latest_year if not india_data.empty else 'N/A'})
- States tracked: {india_data['state'].nunique() if not india_data.empty else 'N/A'}
- Average poverty rate: {latest_india['value'].mean():.2f}% if not india_data.empty else 'N/A'
- Rural average: {rural_avg:.2f}%
- Urban average: {urban_avg:.2f}%
        """
        st.code(summary_text, language=None)
        st.success("Summary text ready to copy!")
