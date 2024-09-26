import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from scipy.stats import skewnorm, t

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Interactive Distribution Visualization"),
    
    # Slider for skewness with continuous updates
    html.Div([
        html.Label("Skewness:"),
        dcc.Slider(
            id='skewness-slider',
            min=-10,
            max=10,
            step=0.1,
            value=0,
            marks={i: f'{i}' for i in range(-10, 11)},
            tooltip={"always_visible": True},  # Tooltip to show value
            updatemode='drag'  # Update while dragging
        ),
        html.Div(id='skewness-value', style={'margin-top': 20})
    ]),
    
    # Slider for kurtosis with continuous updates
    html.Div([
        html.Label("Kurtosis (Negative = Platykurtic, Positive = Leptokurtic):"),
        dcc.Slider(
            id='kurtosis-slider',
            min=-2,
            max=5,
            step=0.1,
            value=0,
            marks={i: f'{i}' for i in range(-2, 6)},
            tooltip={"always_visible": True},  # Tooltip to show value
            updatemode='drag'  # Update while dragging
        ),
        html.Div(id='kurtosis-value', style={'margin-top': 20})
    ]),

    # Graph
    dcc.Graph(id='distribution-graph')
])

# Callback to update graph and display values dynamically
@app.callback(
    [Output('distribution-graph', 'figure'),
     Output('skewness-value', 'children'),
     Output('kurtosis-value', 'children')],
    [Input('skewness-slider', 'value'),
     Input('kurtosis-slider', 'value')]
)
def update_graph(skewness_input, kurtosis_input):
    np.random.seed(42)
    
    # Generate skew-normal distribution for skewness
    data = skewnorm.rvs(a=skewness_input, loc=0, scale=1, size=1000)

    # Handle positive kurtosis (leptokurtic) using t-distribution
    if kurtosis_input > 0:
        df = max(1, 10 / (1 + kurtosis_input))  # smaller df means heavier tails (leptokurtic)
        data_kurt = t.rvs(df, loc=0, scale=1, size=1000)
        data = data + data_kurt

    # Handle negative kurtosis (platykurtic) by increasing variance (spreading data)
    elif kurtosis_input < 0:
        # Increase variance to simulate a flatter distribution (lighter tails)
        spread_factor = 1 - kurtosis_input  # Negative kurtosis results in more spread
        data = data * spread_factor

    # Determine dynamic range for the x-axis
    x_min, x_max = np.min(data), np.max(data)
    # Ensure the x-axis is symmetric around zero
    max_abs_value = max(abs(x_min), abs(x_max))
    x_range = [-max_abs_value, max_abs_value]

    # Create histogram trace
    trace = go.Histogram(x=data, nbinsx=50)

    # Create the figure with dynamic y-axis and centered x-axis
    layout = go.Layout(
        title=f'Distribution with Skewness = {skewness_input:.2f} and Adjusted Kurtosis (Negative = Platykurtic, Positive = Leptokurtic)',
        xaxis=dict(title='Value', range=x_range),  # Dynamic x-axis centered at 0
        yaxis=dict(title='Frequency'),  # Dynamic y-axis
        bargap=0.1
    )
    figure = go.Figure(data=[trace], layout=layout)

    return figure, f"Input Skewness: {skewness_input}", f"Input Kurtosis: {kurtosis_input}"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)