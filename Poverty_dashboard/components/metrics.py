"""
Metrics Components - KPI cards and metric displays
"""

import streamlit as st
import config


def render_kpi_cards(kpi_data):
    """
    Render KPI cards in a grid layout
    
    Args:
        kpi_data (dict): Dictionary with KPI values
    """
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            label="Global Avg Poverty",
            value=f"{kpi_data.get('global_avg', 0):.2f}%",
            delta=f"{kpi_data.get('global_change', 0):.2f}%",
            delta_color="inverse",
            help_text="Average global poverty rate (latest year)"
        )
    
    with col2:
        render_metric_card(
            label="India Avg Poverty",
            value=f"{kpi_data.get('india_avg', 0):.2f}%",
            delta=f"{kpi_data.get('india_change', 0):.2f}%",
            delta_color="inverse",
            help_text="Average India poverty rate (latest year)"
        )
    
    with col3:
        render_metric_card(
            label="Countries Tracked",
            value=str(kpi_data.get('total_countries', 0)),
            help_text="Total number of countries in dataset"
        )
    
    with col4:
        render_metric_card(
            label="Indian States",
            value=str(kpi_data.get('total_states', 0)),
            help_text="Total number of Indian states/territories"
        )


def render_metric_card(label, value, delta=None, delta_color="normal", help_text=None):
    """
    Render a single metric card
    
    Args:
        label (str): Metric label
        value (str): Metric value
        delta (str): Change value (optional)
        delta_color (str): 'normal', 'inverse', or 'off'
        help_text (str): Help tooltip text
    """
    
    st.metric(
        label=label,
        value=value,
        delta=delta,
        delta_color=delta_color,
        help=help_text
    )


def render_metric_grid(metrics_list, columns=4):
    """
    Render multiple metrics in a grid
    
    Args:
        metrics_list (list): List of metric dictionaries
        columns (int): Number of columns in grid
    """
    
    cols = st.columns(columns)
    
    for i, metric in enumerate(metrics_list):
        with cols[i % columns]:
            render_metric_card(
                label=metric.get('label', 'Metric'),
                value=metric.get('value', 'N/A'),
                delta=metric.get('delta'),
                delta_color=metric.get('delta_color', 'normal'),
                help_text=metric.get('help')
            )


def render_comparison_metrics(metrics_dict, title=None):
    """
    Render comparison metrics side by side
    
    Args:
        metrics_dict (dict): Dictionary with 'left' and 'right' metrics
        title (str): Optional title
    """
    
    if title:
        st.markdown(f"### {title}")
    
    col1, col2 = st.columns(2)
    
    left_metric = metrics_dict.get('left', {})
    right_metric = metrics_dict.get('right', {})
    
    with col1:
        render_metric_card(
            label=left_metric.get('label', 'Metric 1'),
            value=left_metric.get('value', 'N/A'),
            delta=left_metric.get('delta'),
            delta_color=left_metric.get('delta_color', 'normal'),
            help_text=left_metric.get('help')
        )
    
    with col2:
        render_metric_card(
            label=right_metric.get('label', 'Metric 2'),
            value=right_metric.get('value', 'N/A'),
            delta=right_metric.get('delta'),
            delta_color=right_metric.get('delta_color', 'normal'),
            help_text=right_metric.get('help')
        )


def render_colored_metric(label, value, color="primary", icon=None):
    """
    Render a colored metric card
    
    Args:
        label (str): Metric label
        value (str): Metric value
        color (str): Color scheme key from config
        icon (str): Optional icon emoji
    """
    
    color_hex = config.COLOR_SCHEME.get(color, config.COLOR_SCHEME['primary'])
    
    icon_display = f"{icon} " if icon else ""
    
    st.markdown(
        f"""
        <div style="
            background-color: {color_hex}15;
            border-left: 4px solid {color_hex};
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        ">
            <p style="margin: 0; font-size: 14px; color: #666;">{icon_display}{label}</p>
            <p style="margin: 5px 0 0 0; font-size: 28px; font-weight: bold; color: {color_hex};">
                {value}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_progress_metric(label, current, target, units=""):
    """
    Render a progress metric with progress bar
    
    Args:
        label (str): Metric label
        current (float): Current value
        target (float): Target value
        units (str): Units for display
    """
    
    progress_pct = min(current / target * 100, 100) if target > 0 else 0
    
    st.markdown(f"**{label}**")
    st.progress(progress_pct / 100)
    st.markdown(f"*{current}{units} of {target}{units} ({progress_pct:.1f}%)*")
