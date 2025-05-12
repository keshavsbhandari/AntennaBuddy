import numpy as np
import plotly.graph_objects as go
import streamlit as st
from src.plots.base_plot import BasePlot
from src.config.constants import DEFAULT_N, DEFAULT_D, DEFAULT_WAVELENGTH

class GratingLobeCheck(BasePlot):
    def __init__(self):
        super().__init__()
        self.title = "Grating Lobe Check"
    
    def plot(self, N, d, wavelength, color=None, name=None):
        """
        Check for the presence of grating lobes and plot the radiation pattern.
        
        Parameters:
        - N (int): Number of elements
        - d (float): Element spacing in wavelengths
        - wavelength (float): Wavelength of operation
        - color (str): Color for the plot
        - name (str): Name for the plot in the legend
        """
        # Calculate critical spacing
        critical_spacing = wavelength / 2
        d_actual = d * wavelength
        
        # Calculate array factor
        theta = np.linspace(0, np.pi, 1000)
        mu = 2 * np.pi * d * np.cos(theta)
        AF = np.abs(np.sin(N * mu / 2) / (N * np.sin(mu / 2)))
        AF_normalized = AF / np.max(AF)
        
        # Create the plot
        fig = go.Figure()
        
        # Add the radiation pattern
        fig.add_trace(go.Scatter(
            x=np.degrees(theta),
            y=AF_normalized,
            mode='lines',
            name=name or f'N={N}, d={d}λ, λ={wavelength:.2f}',
            line=dict(color=color or '#1f77b4', width=2)
        ))
        
        # Add a vertical line at the critical spacing
        if d_actual > critical_spacing:
            # Find the angles where grating lobes occur
            grating_lobe_angles = np.arccos(np.array([-1, 1]) * wavelength / d_actual)
            for angle in grating_lobe_angles:
                fig.add_trace(go.Scatter(
                    x=[np.degrees(angle), np.degrees(angle)],
                    y=[0, 1],
                    mode='lines',
                    name='Grating Lobe',
                    line=dict(color='red', width=1, dash='dash')
                ))
        
        # Update layout
        fig.update_layout(self.get_layout())
        
        # Add warning or success message
        if d_actual > critical_spacing:
            st.warning(f"⚠️ Grating lobes likely: d = {d_actual:.2f} > λ/2 = {critical_spacing:.2f}")
        else:
            st.success(f"✅ No grating lobes: d = {d_actual:.2f} ≤ λ/2 = {critical_spacing:.2f}")
        
        return fig
    
    def get_controls(self):
        """Get the Streamlit controls for grating lobe check parameters."""
        wavelength = st.slider(
            "Wavelength (λ)", 
            0.1, 2.0, 
            value=st.session_state.get('wavelength', DEFAULT_WAVELENGTH),
            help="Wavelength of operation"
        )
        st.session_state.wavelength = wavelength
        return {'wavelength': wavelength}
    
    def get_about_text(self):
        return """
        ### Grating Lobe Check
        
        This visualization helps identify potential grating lobes, which are unwanted radiation peaks that can occur in antenna arrays.
        
        #### What You're Seeing
        - The radiation pattern for your current configuration
        - A warning if grating lobes are likely to occur
        - The relationship between wavelength and element spacing
        - Dashed red lines indicating grating lobe locations (if present)
        
        #### Key Parameters
        - **Number of Elements (N)**: Affects the overall pattern
        - **Element Spacing (d/λ)**: Critical for grating lobe formation
        - **Wavelength (λ)**: Determines the physical spacing requirements
        
        #### Tips for Analysis
        - Compare different wavelengths to see how they affect the critical spacing
        - Look for the λ/2 threshold in the warning message
        - Use the comparison feature to see how different spacings affect grating lobes
        - Try to find the optimal spacing for your operating frequency
        
        #### Technical Details
        - Grating lobes occur when d > λ/2
        - The grating lobe angles are given by: θ = ±arccos(λ/d)
        - The array factor is calculated as: AF = |sin(Nμ/2)/(N sin(μ/2))|
        - Where μ = 2πd cos(θ)
        - The pattern is normalized to show relative strength
        """ 