import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.signal import chebwin
from src.plots.base_plot import BasePlot
from src.config.constants import DEFAULT_N, DEFAULT_D, DEFAULT_R_DB

class ChebyshevArray(BasePlot):
    def __init__(self):
        super().__init__()
        self.title = "Chebyshev Array Pattern"
    
    def plot(self, N, d, R_dB, wavelength=1.0, color=None, name=None):
        """
        Plot the radiation pattern of a Chebyshev-tapered antenna array.
        
        Parameters:
        - N (int): Number of antenna elements
        - d (float): Element spacing in wavelengths
        - R_dB (float): Desired sidelobe level in decibels
        - wavelength (float): Wavelength of operation
        - color (str): Color for the plot
        - name (str): Name for the plot in the legend
        """
        theta = np.linspace(0, np.pi, 1000)
        weights = chebwin(N, at=R_dB)
        AF = np.zeros_like(theta, dtype=complex)
        
        for n in range(N):
            AF += weights[n] * np.exp(1j * 2 * np.pi * d * n * np.cos(theta))
        
        AF = np.abs(AF)
        AF_normalized = AF / np.max(AF)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=np.degrees(theta),
            y=AF_normalized,
            mode='lines',
            name=name or f'N={N}, d={d}λ, R={R_dB} dB',
            line=dict(color=color or '#1f77b4', width=2)
        ))
        
        # Add a horizontal line at the desired sidelobe level
        fig.add_trace(go.Scatter(
            x=[0, 180],
            y=[10**(-R_dB/20), 10**(-R_dB/20)],
            mode='lines',
            name=f'Desired SLL ({R_dB} dB)',
            line=dict(color='red', width=1, dash='dash')
        ))
        
        fig.update_layout(self.get_layout())
        return fig
    
    def get_controls(self):
        """Get the Streamlit controls for Chebyshev array parameters."""
        R_dB = st.slider(
            "Sidelobe Level (dB)", 
            10, 50, 
            value=st.session_state.get('R_dB', DEFAULT_R_DB),
            help="Desired sidelobe level in decibels"
        )
        st.session_state.R_dB = R_dB
        return {'R_dB': R_dB}
    
    def get_about_text(self):
        return """
        ### Chebyshev Array
        
        This visualization shows how to control sidelobe levels using Chebyshev tapering, which is crucial for many applications.
        
        #### What You're Seeing
        - Equal-height sidelobes at a specified level
        - Trade-off between main beam width and sidelobe level
        - The effect of different sidelobe level requirements
        - A dashed red line showing the desired sidelobe level
        
        #### Key Parameters
        - **Number of Elements (N)**: Affects pattern control
        - **Element Spacing (d/λ)**: Influences the pattern characteristics
        - **Sidelobe Level (dB)**: The desired sidelobe suppression
        
        #### Tips for Analysis
        - Compare different sidelobe levels to see the trade-off with main beam width
        - Try different N values to see how they affect pattern control
        - Use the comparison feature to find the optimal sidelobe level
        - Observe how the pattern changes with different element spacings
        
        #### Technical Details
        - Uses Chebyshev window to generate array weights
        - The array factor is calculated as: AF = |Σ wₙ exp(j2πnd cos(θ))|
        - Where wₙ are the Chebyshev weights
        - The pattern is normalized to show relative strength
        - The dashed red line shows the desired sidelobe level in linear scale
        """ 