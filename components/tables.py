"""
Table Components - Styled data tables
"""

import streamlit as st
import pandas as pd


def render_data_table(data, title=None, height=400):
    """
    Render a basic data table
    
    Args:
        data (pd.DataFrame): Data to display
        title (str): Optional table title
        height (int): Table height in pixels
    """
    
    if title:
        st.markdown(f"### {title}")
    
    st.dataframe(
        data,
        use_container_width=True,
        height=height,
        hide_index=True
    )


def render_styled_table(data, title=None, color_column=None, highlight_max=True):
    """
    Render a styled data table with conditional formatting
    
    Args:
        data (pd.DataFrame): Data to display
        title (str): Optional table title
        color_column (str): Column to apply color gradient
        highlight_max (bool): Whether to highlight maximum values
    """
    
    if title:
        st.markdown(f"### {title}")
    
    if data.empty:
        st.info("No data available")
        return
    
    # Create styled dataframe
    styled_df = data.style
    
    # Apply gradient to numeric columns
    if color_column and color_column in data.columns:
        styled_df = styled_df.background_gradient(
            subset=[color_column],
            cmap='RdYlGn_r',  # Red-Yellow-Green reversed
            vmin=data[color_column].min(),
            vmax=data[color_column].max()
        )
    elif highlight_max:
        # Apply gradient to all numeric columns
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 0:
            styled_df = styled_df.background_gradient(
                subset=numeric_cols.tolist(),
                cmap='RdYlGn_r'
            )
    
    # Format numeric columns
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    format_dict = {col: '{:.2f}' for col in numeric_cols}
    styled_df = styled_df.format(format_dict, na_rep='-')
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)


def render_comparison_table(data1, data2, labels=None, title=None):
    """
    Render side-by-side comparison tables
    
    Args:
        data1 (pd.DataFrame): First dataset
        data2 (pd.DataFrame): Second dataset
        labels (tuple): Labels for the two tables
        title (str): Optional title
    """
    
    if title:
        st.markdown(f"### {title}")
    
    labels = labels or ("Dataset 1", "Dataset 2")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {labels[0]}")
        st.dataframe(data1, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown(f"#### {labels[1]}")
        st.dataframe(data2, use_container_width=True, hide_index=True)


def render_pivot_table(data, index, columns, values, aggfunc='mean', title=None):
    """
    Render a pivot table
    
    Args:
        data (pd.DataFrame): Input data
        index (str): Column to use as row index
        columns (str): Column to use as columns
        values (str): Column to aggregate
        aggfunc (str): Aggregation function
        title (str): Optional title
    """
    
    if title:
        st.markdown(f"### {title}")
    
    try:
        pivot = pd.pivot_table(
            data,
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
            fill_value=0
        )
        
        st.dataframe(
            pivot.style.background_gradient(cmap='YlOrRd'),
            use_container_width=True
        )
    
    except Exception as e:
        st.error(f"Error creating pivot table: {str(e)}")


def render_summary_table(data, group_by, agg_cols, title=None):
    """
    Render a summary statistics table
    
    Args:
        data (pd.DataFrame): Input data
        group_by (str or list): Column(s) to group by
        agg_cols (list): Columns to aggregate
        title (str): Optional title
    """
    
    if title:
        st.markdown(f"### {title}")
    
    try:
        summary = data.groupby(group_by)[agg_cols].agg(['mean', 'median', 'min', 'max', 'std'])
        summary = summary.round(2)
        
        st.dataframe(summary, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error creating summary table: {str(e)}")


def render_downloadable_table(data, filename="data", title=None):
    """
    Render a table with download button
    
    Args:
        data (pd.DataFrame): Data to display
        filename (str): Base filename for download
        title (str): Optional title
    """
    
    if title:
        st.markdown(f"### {title}")
    
    st.dataframe(data, use_container_width=True, hide_index=True)
    
    # Download button
    csv = data.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv"
    )
