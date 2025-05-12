import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.signal import chebwin
import plotly.express as px
import random
import colorsys
from src.config.constants import (
    DEFAULT_N, DEFAULT_D, DEFAULT_BETA, DEFAULT_THETA_STEER,
    DEFAULT_R_DB, DEFAULT_WAVELENGTH, PLOT_TYPES
)
from src.plots.radiation_pattern import RadiationPattern
from src.plots.beam_steering import BeamSteering
from src.plots.chebyshev_array import ChebyshevArray
from src.plots.array_factor_3d import ArrayFactor3D
from src.plots.grating_lobe_check import GratingLobeCheck
from src.utils.plot_utils import get_next_color, format_legend_name

def initialize_session_state():
    """Initialize all session state variables."""
    if 'comparison_plots' not in st.session_state:
        st.session_state.comparison_plots = []
    
    # Initialize current parameters
    if 'current_params' not in st.session_state:
        st.session_state.current_params = {
            'N': DEFAULT_N,
            'd': DEFAULT_D,
            'beta': DEFAULT_BETA,
            'theta_steer_deg': DEFAULT_THETA_STEER,
            'R_dB': DEFAULT_R_DB,
            'wavelength': DEFAULT_WAVELENGTH
        }

def get_sidebar_controls():
    """Get the sidebar controls and return the selected parameters."""
    with st.sidebar:
        st.title("📡 Antenna Array Controls")
        
        # Common parameters
        st.subheader("Common Parameters")
        N = st.slider(
            "Number of Elements (N)", 
            2, 20, 
            value=st.session_state.current_params['N'],
            help="Number of antenna elements in the array"
        )
        d = st.slider(
            "Element Spacing (d/λ)", 
            0.1, 1.0, 
            value=st.session_state.current_params['d'],
            help="Spacing between elements in wavelengths"
        )
        
        # Visualization type selector
        viz_type = st.radio(
            "Select Visualization Type",
            PLOT_TYPES,
            help="Choose the type of antenna array pattern to visualize"
        )
    
    return N, d, viz_type

def handle_comparison_buttons(viz_type, N, d):
    """Handle the comparison buttons and return whether to rerun."""
    if viz_type == "3D Array Factor":
        return False
        
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("➕ Add to Comparison", key="compare_button"):
            # Get existing colors
            existing_colors = [plot['color'] for plot in st.session_state.comparison_plots]
            
            plot_data = {
                'type': viz_type,
                'N': N,
                'd': d,
                'color': get_next_color(existing_colors),
                'name': f"Plot {len(st.session_state.comparison_plots) + 1}"
            }
            
            # Get plot-specific parameters
            if viz_type == "Basic Radiation Pattern":
                plot_data['beta'] = st.session_state.current_params['beta']
            elif viz_type == "Beam Steering":
                plot_data['theta_steer_deg'] = st.session_state.current_params['theta_steer_deg']
            elif viz_type == "Chebyshev Array":
                plot_data['R_dB'] = st.session_state.current_params['R_dB']
            elif viz_type == "Grating Lobe Check":
                plot_data['wavelength'] = st.session_state.current_params['wavelength']
            
            st.session_state.comparison_plots.append(plot_data)
            
            # Reset current values to defaults
            st.session_state.current_params = {
                'N': DEFAULT_N,
                'd': DEFAULT_D,
                'beta': DEFAULT_BETA,
                'theta_steer_deg': DEFAULT_THETA_STEER,
                'R_dB': DEFAULT_R_DB,
                'wavelength': DEFAULT_WAVELENGTH
            }
            return True

    with col2:
        if st.button("🗑️ Reset Comparisons", key="reset_button"):
            st.session_state.comparison_plots = []
            return True
    
    return False

def create_plot(viz_type, N, d):
    """Create and return the appropriate plot based on visualization type."""
    if viz_type == "Basic Radiation Pattern":
        plot = RadiationPattern()
    elif viz_type == "Beam Steering":
        plot = BeamSteering()
    elif viz_type == "Chebyshev Array":
        plot = ChebyshevArray()
    elif viz_type == "3D Array Factor":
        plot = ArrayFactor3D()
    else:  # Grating Lobe Check
        plot = GratingLobeCheck()
    
    controls = plot.get_controls()
    return plot, controls

def add_comparison_plots(plot, fig, viz_type):
    """Add comparison plots to the main figure if they exist."""
    if st.session_state.comparison_plots:
        for plot_data in st.session_state.comparison_plots:
            if plot_data['type'] == viz_type:
                fig.add_trace(go.Scatter(
                    x=np.degrees(np.linspace(0, np.pi, 1000)),
                    y=plot.plot(
                        plot_data['N'], 
                        plot_data['d'], 
                        **{k: v for k, v in plot_data.items() if k not in ['N', 'd', 'type', 'color', 'name']}
                    ).data[0].y,
                    mode='lines',
                    name=format_legend_name(plot_data),
                    line=dict(color=plot_data['color'], width=2, dash='dash')
                ))

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="Antenna Array Pattern Visualizer",
        page_icon="📡",
        layout="wide"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stApp {
            max-width: 100%;
            margin: 0;
            padding: 0;
        }
        .stSidebar {
            padding: 1rem;
        }
        .main .block-container {
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 100%;
        }
        .compare-button {
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Get parameters from sidebar
    N, d, viz_type = get_sidebar_controls()

    # Main content area
    st.title("📡 Antenna Array Pattern Visualizer")

    # Handle comparison buttons
    if handle_comparison_buttons(viz_type, N, d):
        st.experimental_rerun()

    # Create and display the appropriate plot
    plot, controls = create_plot(viz_type, N, d)
    
    if viz_type == "3D Array Factor":
        fig_3d, fig_contour = plot.plot(N, d, **controls)
        
        # Display both plots side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_3d, use_container_width=True)
        with col2:
            st.plotly_chart(fig_contour, use_container_width=True)
    else:
        fig = plot.plot(N, d, **controls)
        add_comparison_plots(plot, fig, viz_type)
        st.plotly_chart(fig, use_container_width=True)
    
    # Show about section
    plot.show_about()

    # Update current parameters
    st.session_state.current_params.update({
        'N': N,
        'd': d,
        **controls
    })

if __name__ == "__main__":
    main() 