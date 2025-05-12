import numpy as np
import plotly.graph_objects as go
import streamlit as st
from src.plots.base_plot import BasePlot
from src.config.constants import DEFAULT_N, DEFAULT_D, DEFAULT_THETA_STEER

class BeamSteering(BasePlot):
    def __init__(self):
        super().__init__()
        self.title = "Beam Steering Pattern"
    
    def plot(self, N, d, theta_steer_deg, wavelength=1.0, color=None, name=None):
        """
        Plot the beam-steered radiation pattern of a ULA.
        
        Parameters:
        - N (int): Number of antenna elements
        - d (float): Element spacing in wavelengths
        - theta_steer_deg (float): Desired steering angle in degrees
        - wavelength (float): Wavelength of operation
        - color (str): Color for the plot
        - name (str): Name for the plot in the legend
        """
        theta = np.linspace(0, np.pi, 1000)
        theta_steer = np.radians(theta_steer_deg)
        beta = -2 * np.pi * d * np.cos(theta_steer)
        mu = 2 * np.pi * d * np.cos(theta) + beta
        AF = np.abs(np.sin(N * mu / 2) / (N * np.sin(mu / 2)))
        AF_normalized = AF / np.max(AF)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=np.degrees(theta),
            y=AF_normalized,
            mode='lines',
            name=name or f'N={N}, d={d}λ, θ={theta_steer_deg}°',
            line=dict(color=color or '#1f77b4', width=2)
        ))
        
        fig.update_layout(self.get_layout())
        return fig
    
    def get_controls(self):
        """Get the Streamlit controls for beam steering parameters."""
        theta_steer_deg = st.slider(
            "Steering Angle (degrees)", 
            0, 180, 
            value=st.session_state.get('theta_steer_deg', DEFAULT_THETA_STEER),
            help="Desired steering angle in degrees"
        )
        st.session_state.theta_steer_deg = theta_steer_deg
        return {'theta_steer_deg': theta_steer_deg}
    
    def get_about_text(self):
        return """
        ### Beam Steering
        
        This visualization demonstrates how to electronically steer the main beam of an antenna array without physically moving it.
        
        #### What You're Seeing
        - The main beam is steered to a specific angle
        - The phase shift (β) is automatically calculated
        - The pattern shows how the beam shape changes with steering
        
        #### Key Parameters
        - **Number of Elements (N)**: Affects steering resolution
        - **Element Spacing (d/λ)**: Critical for steering range
        - **Steering Angle**: The desired direction of the main beam
        
        #### Tips for Analysis
        - Try different steering angles to see the phase shift requirements
        - Observe how the pattern distorts at large steering angles
        - Compare different element spacings to find the steering limits
        - Use the comparison feature to see how N affects steering precision
        
        #### Technical Details
        - The phase shift (β) is calculated as: β = -2πd cos(θ₀)
        - The array factor is: AF = |sin(Nμ/2)/(N sin(μ/2))|
        - Where μ = 2πd cos(θ) + β
        - The pattern is normalized to show relative strength
        """ 