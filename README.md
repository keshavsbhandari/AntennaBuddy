# Antenna Array Pattern Visualizer

An interactive web application for visualizing various antenna array patterns using Streamlit.

## Features

- Basic Radiation Pattern visualization
- Beam Steering visualization
- Chebyshev Array visualization
- 3D Array Factor visualization
- Grating Lobe Check
- Comparison functionality for different configurations

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deployment to Streamlit Cloud

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (app.py)
6. Click "Deploy"

## Project Structure

```
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── src/
│   ├── config/        # Configuration files
│   ├── plots/         # Plot classes
│   └── utils/         # Utility functions
```

## Dependencies

- streamlit>=1.32.0
- numpy>=1.24.0
- plotly>=5.18.0
- scipy>=1.11.0 