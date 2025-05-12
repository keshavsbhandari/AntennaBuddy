import numpy as np
import plotly.graph_objects as go
import streamlit as st
from src.plots.base_plot import BasePlot
from src.config.constants import DEFAULT_N, DEFAULT_D, DEFAULT_BETA

class RadiationPattern(BasePlot):
    def __init__(self):
        super().__init__()
        self.title = "ULA Radiation Pattern"
    
    def plot(self, N, d, beta=0, wavelength=1.0, color=None, name=None):
        theta = np.linspace(0, np.pi, 1000)
        d_actual = d * wavelength
        mu = 2 * np.pi * d_actual * np.cos(theta) + beta
        AF = np.abs(np.sin(N * mu / 2) / (N * np.sin(mu / 2)))
        AF_normalized = AF / np.max(AF)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=np.degrees(theta),
            y=AF_normalized,
            mode='lines',
            name=name or f'N={N}, d={d}λ, β={beta:.2f}',
            line=dict(color=color or '#1f77b4', width=2)
        ))
        
        fig.update_layout(self.get_layout())
        return fig
    
    def get_controls(self):
        beta = st.slider("Phase Shift (β)", -np.pi, np.pi, 
                        value=st.session_state.get('beta', DEFAULT_BETA),
                        help="Progressive phase shift in radians")
        st.session_state.beta = beta
        return {'beta': beta}
    
    def get_about_text(self):
        return """
        ### Basic Radiation Pattern
        
        This visualization shows the normalized radiation pattern of a Uniform Linear Array (ULA), which is the fundamental building block of many antenna arrays.
        
        #### What You're Seeing
        - The plot shows how signal strength varies with angle (θ)
        - The main beam is the strongest radiation direction
        - Sidelobes are the smaller peaks around the main beam
        - The pattern is normalized to show relative strength
        
        #### Key Parameters
        - **Number of Elements (N)**: More elements create a narrower main beam and higher directivity
        - **Element Spacing (d/λ)**: Affects the beam width and sidelobe levels
        - **Phase Shift (β)**: Controls the beam direction
        
        #### Tips for Analysis
        - Try increasing N to see how it narrows the main beam
        - Experiment with different d/λ values to understand spacing effects
        - Use the comparison feature to see how β affects the pattern
        - Look for the relationship between spacing and sidelobe levels
        """ 