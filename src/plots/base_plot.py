from abc import ABC, abstractmethod
import streamlit as st
from src.utils.plot_utils import get_plot_layout

class BasePlot(ABC):
    def __init__(self):
        self.title = ""
        self.xaxis_title = "Angle θ (degrees)"
        self.yaxis_title = "Normalized Array Factor"
    
    @abstractmethod
    def plot(self, **kwargs):
        """Generate the plot with the given parameters."""
        pass
    
    @abstractmethod
    def get_controls(self):
        """Get the Streamlit controls for this plot type."""
        pass
    
    def get_about_text(self):
        """Get the about text for this plot type."""
        return """
        ### About this Plot
        
        This is a base plot class. Override this method in your plot class to provide specific information.
        """
    
    def show_about(self):
        """Show the about section for this plot type."""
        with st.expander("About this Visualization"):
            st.markdown(self.get_about_text())
    
    def get_layout(self):
        """Get the common layout settings for this plot type."""
        return get_plot_layout(self.title, self.xaxis_title, self.yaxis_title) 