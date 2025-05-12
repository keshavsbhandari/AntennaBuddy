import numpy as np
import plotly.graph_objects as go
import streamlit as st
from src.plots.base_plot import BasePlot
from src.config.constants import DEFAULT_N, DEFAULT_D

class ArrayFactor3D(BasePlot):
    def __init__(self):
        super().__init__()
        self.title = "3D Array Factor Pattern"
    
    def plot(self, N, d, wavelength=1.0, color=None, name=None):
        """
        Generate a 3D surface plot of the array factor across azimuth and elevation.
        
        Parameters:
        - N (int): Number of elements
        - d (float): Element spacing in wavelengths
        - wavelength (float): Wavelength of operation
        - color (str): Color for the plot
        - name (str): Name for the plot in the legend
        """
        # Create meshgrid for azimuth and elevation
        az = np.linspace(0, 2 * np.pi, 100)
        el = np.linspace(0, np.pi, 100)
        AZ, EL = np.meshgrid(az, el)
        
        # Calculate array factor
        mu = 2 * np.pi * d * np.cos(EL)
        AF = np.abs(np.sin(N * mu / 2) / (N * np.sin(mu / 2)))
        AF_normalized = AF / np.max(AF)
        
        # Convert to Cartesian coordinates for 3D plotting
        X = AF_normalized * np.sin(EL) * np.cos(AZ)
        Y = AF_normalized * np.sin(EL) * np.sin(AZ)
        Z = AF_normalized * np.cos(EL)
        
        # Create 3D surface plot
        fig_3d = go.Figure()
        fig_3d.add_trace(go.Surface(
            x=X, y=Y, z=Z,
            colorscale='Viridis',
            showscale=True,
            name=name or f'N={N}, d={d}λ'
        ))
        
        # Update layout for 3D plot
        fig_3d.update_layout(
            title=self.title,
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                aspectmode='cube'
            ),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02
            )
        )
        
        # Create contour plot
        fig_contour = go.Figure()
        fig_contour.add_trace(go.Contour(
            x=np.degrees(az),
            y=np.degrees(el),
            z=AF_normalized,
            colorscale='Viridis',
            showscale=True,
            name=name or f'N={N}, d={d}λ'
        ))
        
        # Update layout for contour plot
        fig_contour.update_layout(
            title="Array Factor Contour Plot",
            xaxis_title="Azimuth (degrees)",
            yaxis_title="Elevation (degrees)",
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02
            )
        )
        
        return fig_3d, fig_contour
    
    def get_controls(self):
        """Get the Streamlit controls for 3D array factor parameters."""
        # No additional controls needed beyond N and d
        return {}
    
    def get_about_text(self):
        return """
        ### 3D Array Factor
        
        This visualization provides a complete spatial view of the radiation pattern in three dimensions.
        
        #### What You're Seeing
        - 3D surface plot showing the radiation pattern in all directions
        - Contour plot showing the pattern in 2D projection
        - The complete spatial distribution of the radiation
        - Color scale indicating the relative strength of radiation
        
        #### Key Parameters
        - **Number of Elements (N)**: Affects the 3D pattern shape
        - **Element Spacing (d/λ)**: Influences the spatial distribution
        
        #### Tips for Analysis
        - Rotate the 3D plot to examine the pattern from different angles
        - Use the contour plot to see the pattern in 2D
        - Compare different element spacings to see their 3D effects
        - Look for the relationship between spacing and 3D pattern structure
        
        #### Technical Details
        - The array factor is calculated in spherical coordinates
        - Converted to Cartesian coordinates for 3D visualization
        - The pattern is normalized to show relative strength
        - The contour plot shows the pattern in azimuth-elevation space
        """ 