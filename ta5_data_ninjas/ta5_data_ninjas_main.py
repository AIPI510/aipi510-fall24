# AIPI510 TA5 Statistics
# Author: Jesse Warren & Haochen Li

# GenAI is used to generate the outline of the intereactive website pages.  

from flask import Flask
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from scipy.stats import skewnorm, t


# Initialize the Flask app
server = Flask(__name__)

# Interactive Normal Distribution hosted on /demo1
app1 = Dash(__name__, server=server, url_base_pathname='/demo1/')

# Define the layout of the first Normal Distribution app
app1.layout = html.Div([
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
    html.Div(id='stats-output',  style={'textAlign': 'center', 'marginTop': '20px'})
])

# Define the callback to update the graph and display statistics for app1
@app1.callback(
    [Output('normal-dist-graph', 'figure'),
     Output('stats-output', 'children')],
    [Input('mean-slider', 'value'),
     Input('alpha-slider', 'value')]
)
def update_graph_app1(mean, alpha):
    start = -10
    end = 10
    point_num = 5000

    delta_x = (end- start)/point_num

    x = np.linspace(start, end, point_num)
    
    y1 = (1 / np.sqrt(2 * np.pi * 1)) * np.exp(-0.5 * (x ** 2)) # First normal distribution (mean=0, var=1)
    y2 = (1 / np.sqrt(2 * np.pi * 1)) * np.exp(-0.5 * ((x - mean) ** 2)) # Second normal distribution (mean=variable, var=1)
    y = alpha * y1 + (1 - alpha) * y2 # weighter normal distribution (merged version)
    
    # Calculate skewness and kurtosis
    skewness = stat_std_moment(x, y, delta_x, order = 3)
    kurt = stat_std_moment(x, y, delta_x, order = 4)
    
    # plot the graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1*alpha, mode='lines', name='N(0, 1)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=x, y=y2*(1-alpha), mode='lines', name=f'N({mean}, 1)', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Merged', line=dict(color='red', dash='dash')))
    fig.update_layout(title='Normal Distribution', xaxis_title='X', yaxis_title='Probability Density')
    stats_output = f"Skewness: {skewness:.2f}, Kurtosis: {kurt:.2f}"
    
    return fig, stats_output

# helper functions to calculate the std moments
def stat_std_moment(x, y, delta_x, order : int):
    '''
    this function is to calculate the order th moment given the plot x and y np array 
    order = 3 means skewness
    order = 4 means kurtosis
    '''
    nth_moment = moment(x, y, delta_x, order)
    sigma = moment(x, y, delta_x, order = 2)
    return nth_moment/(sigma**order) # miu_n/sigma^n

def moment(x, y, delta_x, order : int):
    '''
    this function is to calculate the order th moment given the plot x and y np array
    '''
    if order in [2,3,4]:
        mean = stat_mean(x, y, delta_x) # get mean first
        return np.sum( (x - mean) ** order * y) * delta_x # approximate E[(X-mean)^n]; n is order here
    else:
        raise ValueError("Order not supported")

def stat_mean(x, y, delta_x):
    '''
    this function is to calculate the mean given the plot x and y np array
    '''
    return np.sum(x * y) *delta_x # E[x]


# Interactive Distribution Visualization hosted on /demo2
app2 = Dash(__name__, server=server, url_base_pathname='/demo2/')

# Layout for the distribution visualization app
app2.layout = html.Div([
    html.H1("Interactive Distribution Visualization"),
    
    # Slider for skewness
    html.Div([
        html.Label("Skewness:"),
        dcc.Slider(
            id='skewness-slider',
            min=-10,
            max=10,
            step=0.1,
            value=0,
            marks={i: f'{i}' for i in range(-10, 11)},
            tooltip={"always_visible": True},
            updatemode='drag'
        ),
        html.Div(id='skewness-value', style={'margin-top': 20})
    ]),
    
    # Slider for kurtosis
    html.Div([
        html.Label("Kurtosis (Negative = Platykurtic, Positive = Leptokurtic):"),
        dcc.Slider(
            id='kurtosis-slider',
            min=-2,
            max=5,
            step=0.1,
            value=0,
            marks={i: f'{i}' for i in range(-2, 6)},
            tooltip={"always_visible": True},
            updatemode='drag'
        ),
        html.Div(id='kurtosis-value', style={'margin-top': 20})
    ]),
    # Plot graph
    dcc.Graph(id='distribution-graph')
])

# Callback to update graph and display values dynamically for app2
@app2.callback(
    [Output('distribution-graph', 'figure'),
     Output('skewness-value', 'children'),
     Output('kurtosis-value', 'children')],
    [Input('skewness-slider', 'value'),
     Input('kurtosis-slider', 'value')]
)
def update_graph_app2(skewness_input, kurtosis_input):
    np.random.seed(42)
    
    # Generate skew-normal distribution for skewness
    data = skewnorm.rvs(a=skewness_input, loc=0, scale=1, size=1000)

    # Handle positive kurtosis (leptokurtic) using t-distribution
    if kurtosis_input > 0:
        # smaller df means heavier tails (i.e. leptokurtic kurtosis)
        df = max(1, 10 / (1 + kurtosis_input))
        data_kurt = t.rvs(df, loc=0, scale=1, size=1000)
        data = data + data_kurt

    # Handle negative kurtosis (platykurtic) by increasing data variance
    elif kurtosis_input < 0:
        # Increase variance to simulate a flatter distribution
        spread_factor = 1 - kurtosis_input
        data = data * spread_factor

    # Making the x-axis is symmetric around zero
    x_min, x_max = np.min(data), np.max(data)
    max_abs_value = max(abs(x_min), abs(x_max))
    x_range = [-max_abs_value, max_abs_value]

    # Creating histogram trace
    trace = go.Histogram(x=data, nbinsx=50)

    # Creating figure
    layout = go.Layout(
        title=f'Distribution with Skewness = {skewness_input:.2f} and Adjusted Kurtosis (Negative = Platykurtic, Positive = Leptokurtic)',
        xaxis=dict(title='Value', range=x_range),
        yaxis=dict(title='Frequency'),
        bargap=0.1
    )
    figure = go.Figure(data=[trace], layout=layout)

    # Display values to user
    return figure, f"Input Skewness: {skewness_input}", f"Input Kurtosis: {kurtosis_input}"

# Run the Flask server, which hosts both Dash apps
if __name__ == '__main__':
    server.run(debug=True, port=5000)