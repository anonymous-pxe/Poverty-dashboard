"""
Visualization Utilities
Functions for creating charts and maps
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import config


def create_line_chart(data, x, y, color=None, title='', x_label='', y_label='', **kwargs):
    """
    Create an interactive line chart
    
    Args:
        data (pd.DataFrame): Input data
        x (str): Column for x-axis
        y (str): Column for y-axis
        color (str or None): Column for color grouping or color hex
        title (str): Chart title
        x_label (str): X-axis label
        y_label (str): Y-axis label
    
    Returns:
        plotly.graph_objs.Figure: Line chart figure
    """
    
    if isinstance(color, str) and color.startswith('#'):
        # Single color provided
        fig = px.line(data, x=x, y=y, title=title, **kwargs)
        fig.update_traces(line_color=color)
    else:
        # Color by column
        fig = px.line(data, x=x, y=y, color=color, title=title, **kwargs)
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        template='plotly_white',
        hovermode='x unified',
        showlegend=True if color and not color.startswith('#') else False
    )
    
    return fig


def create_bar_chart(data, x, y, color=None, title='', x_label='', y_label='', orientation='v', barmode='relative', **kwargs):
    """
    Create an interactive bar chart
    
    Args:
        data (pd.DataFrame): Input data
        x (str): Column for x-axis
        y (str): Column for y-axis
        color (str or None): Column for color grouping or color hex
        title (str): Chart title
        x_label (str): X-axis label
        y_label (str): Y-axis label
        orientation (str): 'v' for vertical, 'h' for horizontal
        barmode (str): 'group', 'stack', or 'relative'
    
    Returns:
        plotly.graph_objs.Figure: Bar chart figure
    """
    
    if isinstance(color, str) and color.startswith('#'):
        # Single color provided
        fig = px.bar(data, x=x, y=y, title=title, orientation=orientation, **kwargs)
        fig.update_traces(marker_color=color)
    else:
        # Color by column
        fig = px.bar(data, x=x, y=y, color=color, title=title, orientation=orientation, barmode=barmode, **kwargs)
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        template='plotly_white',
        showlegend=True if color and not color.startswith('#') else False
    )
    
    return fig


def create_scatter_plot(data, x, y, color=None, size=None, hover_name=None, title='', x_label='', y_label='', trendline=None, **kwargs):
    """
    Create an interactive scatter plot
    
    Args:
        data (pd.DataFrame): Input data
        x (str): Column for x-axis
        y (str): Column for y-axis
        color (str): Column for color
        size (str): Column for point size
        hover_name (str): Column for hover labels
        title (str): Chart title
        x_label (str): X-axis label
        y_label (str): Y-axis label
        trendline (str): 'ols' for linear regression line
    
    Returns:
        plotly.graph_objs.Figure: Scatter plot figure
    """
    
    fig = px.scatter(
        data, 
        x=x, 
        y=y, 
        color=color,
        size=size,
        hover_name=hover_name,
        title=title,
        trendline=trendline,
        **kwargs
    )
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        template='plotly_white'
    )
    
    return fig


def create_box_plot(data, x, y, color=None, title='', x_label='', y_label='', **kwargs):
    """
    Create an interactive box plot
    
    Args:
        data (pd.DataFrame): Input data
        x (str): Column for x-axis (categories)
        y (str): Column for y-axis (values)
        color (str): Column for color grouping
        title (str): Chart title
        x_label (str): X-axis label
        y_label (str): Y-axis label
    
    Returns:
        plotly.graph_objs.Figure: Box plot figure
    """
    
    fig = px.box(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        template='plotly_white'
    )
    
    return fig


def create_pie_chart(data, values, names, title='', **kwargs):
    """
    Create an interactive pie chart
    
    Args:
        data (pd.DataFrame): Input data
        values (str): Column for values
        names (str): Column for labels
        title (str): Chart title
    
    Returns:
        plotly.graph_objs.Figure: Pie chart figure
    """
    
    fig = px.pie(
        data,
        values=values,
        names=names,
        title=title,
        **kwargs
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template='plotly_white')
    
    return fig


def create_heatmap(data, title='', color_scale='RdYlGn_r', **kwargs):
    """
    Create an interactive heatmap
    
    Args:
        data (pd.DataFrame): Input data (matrix)
        title (str): Chart title
        color_scale (str): Colorscale name
    
    Returns:
        plotly.graph_objs.Figure: Heatmap figure
    """
    
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale=color_scale,
        **kwargs
    ))
    
    fig.update_layout(
        title=title,
        template='plotly_white',
        xaxis_title='',
        yaxis_title=''
    )
    
    return fig


def create_choropleth_map(data, locations, values, title='', color_scale='Reds', **kwargs):
    """
    Create a choropleth map for India
    
    Args:
        data (pd.DataFrame): Input data
        locations (str): Column with state names
        values (str): Column with values to map
        title (str): Map title
        color_scale (str): Color scale
    
    Returns:
        plotly.graph_objs.Figure: Choropleth map figure
    """
    
    # For India map - using scatter_geo as simplified version
    # In production, load actual GeoJSON and use choropleth_mapbox
    
    fig = px.choropleth(
        data,
        locations=locations,
        locationmode='country names',  # Simplified - in production use GeoJSON
        color=values,
        title=title,
        color_continuous_scale=color_scale,
        **kwargs
    )
    
    fig.update_geos(
        center=dict(lat=config.MAP_CENTER_LAT, lon=config.MAP_CENTER_LON),
        projection_scale=config.MAP_ZOOM
    )
    
    fig.update_layout(
        template='plotly_white',
        height=600
    )
    
    return fig


def create_area_chart(data, x, y, color=None, title='', x_label='', y_label='', **kwargs):
    """
    Create an area chart
    
    Args:
        data (pd.DataFrame): Input data
        x (str): Column for x-axis
        y (str): Column for y-axis
        color (str): Column for color grouping
        title (str): Chart title
        x_label (str): X-axis label
        y_label (str): Y-axis label
    
    Returns:
        plotly.graph_objs.Figure: Area chart figure
    """
    
    fig = px.area(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        template='plotly_white'
    )
    
    return fig


def create_histogram(data, x, nbins=30, title='', x_label='', y_label='Frequency', **kwargs):
    """
    Create a histogram
    
    Args:
        data (pd.DataFrame): Input data
        x (str): Column for x-axis
        nbins (int): Number of bins
        title (str): Chart title
        x_label (str): X-axis label
        y_label (str): Y-axis label
    
    Returns:
        plotly.graph_objs.Figure: Histogram figure
    """
    
    fig = px.histogram(
        data,
        x=x,
        nbins=nbins,
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        template='plotly_white'
    )
    
    return fig
