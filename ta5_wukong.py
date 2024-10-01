import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio  # Added to display the graph

# Perform a one-sample t-test
def one_sample_t_test(sample_data, population_mean, alpha=0.05, test_type='two-sided'):
    t_stat, p_value = stats.ttest_1samp(sample_data, population_mean)  # Perform the t-test

    # Adjust p-value and result based on the test type
    if test_type == 'two-sided':
        result = p_value < alpha
    elif test_type == 'left-tailed':
        p_value /= 2  # Left-tailed test
        result = p_value < alpha and t_stat < 0
    elif test_type == 'right-tailed':
        p_value /= 2  # Right-tailed test
        result = p_value < alpha and t_stat > 0
    else:
        raise ValueError("Unsupported test type. Choose 'two-sided', 'left-tailed', or 'right-tailed'.")

    return {
        't_stat': t_stat,
        'p_value': p_value,
        'result': "Reject the null hypothesis (H0)" if result else "Fail to reject the null hypothesis (H0)"
    }

# Visualize t-test results using Plotly
def visualize_interactive(sample_data, population_mean, t_stat, test_type='two-sided', alpha=0.05):
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Sample Data Distribution', 't-Distribution'))

    # Histogram for sample data
    fig.add_trace(
        go.Histogram(
            x=sample_data,
            nbinsx=15,  # Number of bins
            marker_color='lightblue',
            opacity=0.75,
            name='Sample Data',
        ),
        row=1, col=1
    )

    # Add vertical lines for sample mean and population mean
    max_y_hist = max(np.histogram(sample_data, bins=15)[0]) + 5  # Extend the vertical lines to full height
    fig.add_trace(
        go.Scatter(
            x=[np.mean(sample_data)] * 2, y=[0, max_y_hist],
            mode='lines', line=dict(color='red', dash='dash'),
            name=f'Sample mean: {np.mean(sample_data):.2f}'
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=[population_mean] * 2, y=[0, max_y_hist],
            mode='lines', line=dict(color='blue', dash='dash'),
            name=f'Population mean: {population_mean}'
        ),
        row=1, col=1
    )

    # t-distribution and critical regions
    df = len(sample_data) - 1  # Degrees of freedom
    x = np.linspace(-4, 4, 500)
    y = stats.t.pdf(x, df)

    # Plot t-distribution
    fig.add_trace(
        go.Scatter(
            x=x, y=y,
            mode='lines', line=dict(color='blue'),
            name=f't-distribution (df={df})'
        ),
        row=1, col=2
    )

    # Critical regions based on the test type
    if test_type == 'two-sided':
        crit_value = stats.t.ppf(1 - alpha / 2, df)  # Two-tailed critical value
        crit_range_left = x[x <= -crit_value]
        crit_range_right = x[x >= crit_value]

        # Shaded critical regions
        fig.add_trace(
            go.Scatter(
                x=crit_range_left, y=stats.t.pdf(crit_range_left, df),
                fill='tozeroy', mode='lines',
                line=dict(color='red'),
                name=f'Left Critical region (≤ -{crit_value:.2f})'
            ),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(
                x=crit_range_right, y=stats.t.pdf(crit_range_right, df),
                fill='tozeroy', mode='lines',
                line=dict(color='red'),
                name=f'Right Critical region (≥ {crit_value:.2f})'
            ),
            row=1, col=2
        )
    elif test_type == 'left-tailed':
        crit_value = stats.t.ppf(alpha, df)  # Left-tailed critical value
        crit_range = [x[x <= crit_value]]

        fig.add_trace(
            go.Scatter(
                x=crit_range[0], y=stats.t.pdf(crit_range[0], df),
                fill='tozeroy', mode='lines',
                line=dict(color='red'),
                name=f'Critical region (≤ {crit_value:.2f})'
            ),
            row=1, col=2
        )
    elif test_type == 'right-tailed':
        crit_value = stats.t.ppf(1 - alpha, df)  # Right-tailed critical value
        crit_range = [x[x >= crit_value]]

        fig.add_trace(
            go.Scatter(
                x=crit_range[0], y=stats.t.pdf(crit_range[0], df),
                fill='tozeroy', mode='lines',
                line=dict(color='red'),
                name=f'Critical region (≥ {crit_value:.2f})'
            ),
            row=1, col=2
        )

    # Add a line for the calculated t-statistic
    fig.add_trace(
        go.Scatter(
            x=[t_stat] * 2, y=[0, max(y)],  # Vertical line for t-statistic
            mode='lines', line=dict(color='green', dash='dash'),
            name=f't-statistic: {t_stat:.2f}'
        ),
        row=1, col=2
    )

    # Set overall layout and return the figure
    fig.update_layout(
        title_text='Interactive One-Sample t-Test Visualization',
        showlegend=True,
        height=600,
        width=1000
    )

    return fig  # Return the figure object

# Main execution section
if __name__ == "__main__":
    # Example data for testing
    sample_data = np.array([1, 2, 3, 4, 5, 6, 7, 7, 8, 8, 8])
    population_mean = 5  
    alpha = 0.05 

    # Perform the one-sample t-test
    result = one_sample_t_test(sample_data, population_mean, alpha=alpha, test_type='two-sided')

    print("T-statistic:", result['t_stat'])
    print("P-value:", result['p_value'])
    print("Result:", result['result'])

    # Visualize the results
    fig = visualize_interactive(sample_data, population_mean, result['t_stat'])
    pio.show(fig) 