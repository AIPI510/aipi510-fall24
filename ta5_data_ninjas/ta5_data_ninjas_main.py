from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from scipy.stats import skew, kurtosis

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Interactive Normal Distribution"),
    html.Label("Mean:"),
    dcc.Slider(
        id='mean-slider',
        min=-5,
        max=5,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(-5, 6)},
        tooltip={"placement": "bottom", "always_visible": True},
        updatemode="drag"
    ),
    html.Label("Alpha:"),
    dcc.Slider(
        id='alpha-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.5,
        marks={i/10: str(i/10) for i in range(0, 11)},
        tooltip={"placement": "bottom", "always_visible": True},
        updatemode="drag"
    ),
    dcc.Graph(id='normal-dist-graph'),
    html.Div(id='stats-output')
])

# Define the callback to update the graph and display statistics
@app.callback(
    [Output('normal-dist-graph', 'figure'),
     Output('stats-output', 'children')],
    [Input('mean-slider', 'value'),
     Input('alpha-slider', 'value')]
)
def update_graph(mean, alpha):
    x = np.linspace(-5, 5, 1000)
    
    # First normal distribution (mean=0, var=1)
    y1 = (1 / np.sqrt(2 * np.pi * 1)) * np.exp(-0.5 * (x ** 2))
    
    # Second normal distribution (mean=variable, var=1)
    y2 = (1 / np.sqrt(2 * np.pi * 1)) * np.exp(-0.5 * ((x - mean) ** 2))
    
    # Merged normal distribution
    y = alpha * y1 + (1 - alpha) * y2
    
    # Calculate skewness and kurtosis
    skewness = skew(y)
    kurt = kurtosis(y)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1*alpha, mode='lines', name='N(0, 1)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=x, y=y2*(1-alpha), mode='lines', name=f'N({mean}, 1)', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Merged', line=dict(color='red', dash='dash')))
    
    fig.update_layout(title='Normal Distribution', xaxis_title='X', yaxis_title='Probability Density')
    
    stats_output = f"Skewness: {skewness:.2f}, Kurtosis: {kurt:.2f}"
    
    return fig, stats_output

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=5000)