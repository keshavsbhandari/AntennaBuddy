import plotly.graph_objects as go
from src.config.constants import DISTINCT_COLORS
import random

def get_next_color(existing_colors):
    """Get the next color from the predefined distinct colors."""
    used_colors = set(existing_colors)
    for color in DISTINCT_COLORS:
        if color not in used_colors:
            return color
    # If all colors are used, generate a new one
    return f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'

def format_legend_name(plot_data):
    """Format the legend name with detailed parameter information."""
    base_name = f"Plot {plot_data['name'].split()[-1]}"
    params = []
    
    if plot_data['type'] == "Basic Radiation Pattern":
        params.extend([
            f"N={plot_data['N']}",
            f"d={plot_data['d']}λ",
            f"β={plot_data['beta']:.2f} rad"
        ])
    elif plot_data['type'] == "Beam Steering":
        params.extend([
            f"N={plot_data['N']}",
            f"d={plot_data['d']}λ",
            f"θ={plot_data['theta_steer_deg']}°"
        ])
    elif plot_data['type'] == "Chebyshev Array":
        params.extend([
            f"N={plot_data['N']}",
            f"d={plot_data['d']}λ",
            f"R={plot_data['R_dB']} dB"
        ])
    elif plot_data['type'] == "Grating Lobe Check":
        params.extend([
            f"N={plot_data['N']}",
            f"d={plot_data['d']}λ",
            f"λ={plot_data['wavelength']:.2f}"
        ])
    
    return f"{base_name} ({', '.join(params)})"

def get_plot_layout(title, xaxis_title, yaxis_title):
    """Get common plot layout settings."""
    return dict(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        template='plotly_white',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02
        )
    ) 