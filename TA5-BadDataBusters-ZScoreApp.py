import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import plotly.graph_objects as go
import plotly.express as px

# Custom CSS for better styling and visibility
st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e; /* Dark background for the main content area */
            color: white; /* Set the main text color to white for contrast */
        }
        
        /* Sidebar styling */
        .css-17eq0hr { 
            background-color: #252526; /* Dark background for the sidebar */
            color: white; /* White text for better readability in sidebar */
        }

        /* General content text color */
        .css-10trblm { 
            color: white !important; /* Force the content text to be white for consistency */
        }

        /* Input fields styling */
        .css-1cpxqw2 { 
            background-color: #333333 !important; /* Dark background for input fields */
            color: white !important; /* White text within input fields */
        }

        /* Button styling */
        .st-button {
            display: inline-block;
            padding: 8px 16px;
            font-size: 1.2em;
            font-weight: bold;
            color: #fff; /* White text for buttons */
            background-color: #4e8cff; /* Blue background for buttons */
            border: none; /* Remove button border */
            border-radius: 5px; /* Rounded corners for buttons */
            cursor: pointer; /* Show a pointer cursor when hovering over buttons */
            margin: 10px; /* Add margin around buttons */
        }
    </style>
""", unsafe_allow_html=True)  # Allow raw HTML/CSS to apply custom styling

# Sidebar for interactive controls and navigation
st.sidebar.title("🎛️ Navigation & Control Panel")  # Title for the sidebar panel

# Initialize session state to track progress across modules
if 'progress' not in st.session_state:
    st.session_state.progress = 0  

# Radio buttons for navigating between different modules
module = st.sidebar.radio(
    "Navigate through the modules",  # Label for the radio button group
    (
        "📘 Module 1: Basics",  # Basic module introduction
        "📈 Module 2: Exploring Distributions",  # Focus on data distributions
        "🧮 Module 3: Z-Score Applications",  # Module to explore Z-Scores
        "📊 Module 4: Advanced Topics",  # More advanced statistical concepts
        "🎥 Module 5: Animated Normal Distributions",  # Module with animated visualizations
        "🌎 Module 6: Real-World Examples"  # Practical, real-world applications of statistics
    )
)

# Cacheable function to compute normal distribution
@st.cache_data
def compute_normal_distribution(mean, std_dev):
    """
    Computes the x and y values for a normal distribution curve based on the given mean and standard deviation.

    Args:
        mean (float): The mean of the normal distribution.
        std_dev (float): The standard deviation of the normal distribution.

    Returns:
        tuple: A tuple containing two numpy arrays, x (range of values) and y (probability density function values).
    """
    x = np.linspace(mean - 4 * std_dev, mean + 4 * std_dev, 1000)  # Generate x values within ±4 standard deviations of the mean
    y = stats.norm.pdf(x, mean, std_dev)  # Compute corresponding y values for normal distribution using PDF
    return x, y

# Module 1: Basics of Z-Scores and Normal Distributions

# This module introduces the fundamental concepts of Z-scores and normal distributions. 
# It covers the following key topics:

# 1. **Z-Scores**:
#    - A Z-score measures how many standard deviations a given data point is from the mean.
#    - The Z-score formula is presented, and its components (X, mean, and standard deviation) are explained.
   
# 2. **Normal Distribution**:
#    - Explains the properties of a normal distribution, including symmetry, the alignment of mean, median, and mode, 
#      and how the standard deviation determines the spread of the data.
#    - Visualizes the standard normal distribution with a bell curve, highlighting key points like the mean and ±1 standard deviation.
   
# 3. **Interactive Visualization**:
#    - A static visualization is generated using Plotly to show the standard normal distribution curve. 
#    - Key statistical markers such as the mean and ±1 standard deviation are also indicated on the plot.

# This module is designed to provide users with an intuitive understanding of Z-scores and the normal distribution, 
# preparing them for more advanced topics in subsequent modules.

# Progress is tracked using `st.session_state` to ensure users' progress through the modules is saved.


if module == "📘 Module 1: Basics":
    st.header("📘 Module 1: Basics of Z-Scores and Normal Distributions")  # Header for the first module

    # Subsection explaining Z-scores
    st.subheader("🔍 What is a Z-Score?")
    st.write("""
    A **Z-score** measures how many standard deviations a data point is from the mean. It's a way to standardize different datasets for easy comparison.
    The formula for Z-score is:
    """)
    
    # Latex formula for Z-score
    st.latex(r"Z = \frac{X - \mu}{\sigma}")  # Displays the Z-score formula using LaTeX
    
    # Explanation of the components in the Z-score formula
    st.write("""
    Where:
    - $X$ is the value of interest.
    - $\mu$ is the mean.
    - $\sigma$ is the standard deviation.
    """)

    # Subsection explaining normal distribution
    st.subheader("📊 What is a Normal Distribution?")
    st.write("""
    A **normal distribution** is a bell-shaped curve that shows how data spreads around the mean. 
    Some key characteristics of normal distributions include:
    
    - **Symmetry**: The left and right sides are mirror images.
    - **Mean, Median, and Mode** are the same.
    - **Standard Deviation**: Determines the spread of the data around the mean.
    """)

    # Generate and display a static visualization of the standard normal distribution
    x, y = compute_normal_distribution(0, 1)  # Compute x and y values for a standard normal distribution (mean = 0, std dev = 1)

    # Create a Plotly figure to visualize the standard normal distribution
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Standard Normal Distribution'))  # Plot the main distribution curve
    fig.add_trace(go.Scatter(x=[-1, -1], y=[0, stats.norm.pdf(-1, 0, 1)], mode='lines', name='-1σ'))  # Add marker for -1 standard deviation
    fig.add_trace(go.Scatter(x=[1, 1], y=[0, stats.norm.pdf(1, 0, 1)], mode='lines', name='+1σ'))  # Add marker for +1 standard deviation
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, stats.norm.pdf(0, 0, 1)], mode='lines', name='Mean'))  # Mark the mean at Z = 0

    # Update layout with titles and axis labels
    fig.update_layout(title='📈 Standard Normal Distribution',
                      xaxis_title='Z-Score',  # Label for x-axis
                      yaxis_title='Probability Density')  # Label for y-axis

    st.plotly_chart(fig)  # Display the Plotly chart in the Streamlit app

    # Provide a summary of the content covered
    st.write("You’ve now learned about the basics of Z-scores and the normal distribution. In the next section, we’ll dive deeper and explore how changing parameters affects the distribution.")

    # Update progress tracking to indicate Module 1 has been completed (or revisited)
    st.session_state.progress = max(st.session_state.progress, 1)  # Ensure progress is recorded without decreasing it if revisited

# Module 2: Exploring Normal Distributions with Plotly

# This module allows users to interactively explore how changing the mean (μ) and standard deviation (σ) affects 
# the shape and position of a normal distribution. The module features:

# 1. **Interactive Controls**:
#    - Users can adjust the **mean** and **standard deviation** of the normal distribution using sliders in the sidebar.
#    - The changes are reflected in real-time on an interactive Plotly graph, allowing users to see the immediate effect of these parameters.

# 2. **Normal Distribution Plot**:
#    - A normal distribution is plotted based on the user-selected values of μ and σ.
#    - The x-axis is fixed to range from -20 to 20, and the y-axis is fixed to a common probability density range (0 to 0.5) to keep the visual scale consistent.
#    - The plot is updated dynamically as the user adjusts the mean and standard deviation.

# 3. **Detailed Explanation**:
#    - Provides insights into how the **mean (μ)** shifts the center of the distribution along the x-axis while keeping the shape of the distribution unchanged.
#    - Explains the role of **standard deviation (σ)** in controlling the spread of the distribution:
#      - A smaller σ results in a narrow, tall peak (data clustered near the mean).
#      - A larger σ results in a wider, flatter curve (data more spread out).
#    - Discusses key statistical properties such as the **Empirical Rule** (68-95-99.7 rule) and how much data lies within 1, 2, or 3 standard deviations from the mean.

# 4. **Real-World Interpretation**:
#    - Offers practical examples, showing how variations in σ indicate the degree of spread or variability in datasets like exam scores, stock prices, or patient outcomes.

# Progress is updated using `st.session_state`, advancing the progress tracker to mark the completion of Module 2.


if module == "📈 Module 2: Exploring Distributions":
    st.header("📈 Module 2: Exploring Normal Distributions")

    st.subheader("🔧 Adjusting Mean and Standard Deviation")
    st.write("""
    Now, let’s interactively explore the effect of changing the **mean** and **standard deviation** of a normal distribution.
    Move the sliders below to adjust these parameters.
    """)

   # Sidebar inputs for interactive normal distribution
    mean = st.sidebar.slider("Mean (μ)", min_value=-10.0, max_value=10.0, value=st.session_state.get("mean", 0.0), step=0.1)
    std_dev = st.sidebar.slider("Standard Deviation (σ)", min_value=0.1, max_value=5.0, value=st.session_state.get("std_dev", 1.0), step=0.1)

    # Fixed x-axis for the plot
    x = np.linspace(-20, 20, 1000)

    # Calculate the y-values (probability density function)
    y = stats.norm.pdf(x, mean, std_dev)

    # Create a Plotly figure
    fig = go.Figure()

    # Add trace for the normal distribution
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'N(μ={mean:.2f}, σ={std_dev:.2f})'))

    # Update layout for fixed axes
    fig.update_layout(
        title=f'Normal Distribution (μ={mean:.2f}, σ={std_dev:.2f})',
        xaxis_title='X-axis',
        yaxis_title='Probability Density',
        xaxis=dict(range=[-20, 20]),  # Fixed range for x-axis
        yaxis=dict(range=[0, 0.5]),   # Fixed range for y-axis based on common normal distribution ranges
        showlegend=True
    )

    # Display the interactive plotly chart
    st.plotly_chart(fig)

    # Detailed insights on how mean and standard deviation affect the distribution
    st.write(f"""
    ### Detailed Insights:

    #### Mean (μ):
    - The **mean (μ)** represents the center of the distribution. 
    - As the **mean** shifts, the peak of the distribution moves **left or right** along the x-axis, but the shape of the distribution remains the same.
    - For example, with **μ = {mean:.2f}**, the distribution is centered at **{mean:.2f}**.
    - The mean is also the **balance point** of the distribution, which means that half of the data lies to the left of this value, and half lies to the right.
    
    #### Standard Deviation (σ):
    - The **standard deviation (σ)** controls the **spread** or **width** of the distribution.
    - A **smaller σ** results in a **narrow, tall** curve, meaning the data is more tightly clustered around the mean. 
    - A **larger σ** produces a **wider, flatter** curve, indicating that the data is more spread out from the mean.
    - With **σ = {std_dev:.2f}**, the curve shows that approximately:
        - **68%** of the data lies within **1σ** of the mean (from {mean - std_dev:.2f} to {mean + std_dev:.2f}).
        - **95%** of the data lies within **2σ** of the mean (from {mean - 2 * std_dev:.2f} to {mean + 2 * std_dev:.2f}).
        - **99.7%** of the data lies within **3σ** of the mean (from {mean - 3 * std_dev:.2f} to {mean + 3 * std_dev:.2f}).
    - This is known as the **Empirical Rule**, and it highlights how data is distributed across the curve.

    #### Shape of the Curve:
    - **Symmetry**: The normal distribution is symmetric around the mean, meaning that the left and right sides of the curve are mirror images.
    - The height of the peak represents the **probability density** at the mean.
    - As you change **σ**, the height and width of the curve adjust. A smaller standard deviation results in a **taller** and **narrower** peak, indicating that most of the data is concentrated around the mean.
    - As **σ** increases, the curve becomes **flatter**, indicating that data is more spread out, with higher variability.

    #### Real-World Interpretations:
    - If the standard deviation is small, it suggests that data points (e.g., exam scores, stock prices, or patient outcomes) are consistently close to the mean.
    - If the standard deviation is large, it indicates greater variation or uncertainty in the data, meaning values are more spread out from the average.
    """)

    # Update progress
    st.session_state.progress = max(st.session_state.progress, 2)


# Module 3: Z-Score Applications with Separate Sliders for Mean and Std Dev

# This module introduces practical applications of Z-scores, allowing users to calculate Z-scores based on custom inputs
# and explore their significance in terms of percentiles and outlier detection.

if module == "🧮 Module 3: Z-Score Applications":
    st.header("🧮 Module 3: Z-Score Applications")

    # Independent sliders for mean and std_dev in Module 3
    st.subheader("Set Mean and Standard Deviation for Z-Score Calculation")
    mean = st.slider("Mean (μ)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
    std_dev = st.slider("Standard Deviation (σ)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

    st.subheader("🧮 Z-Score Calculator")
    st.write("Now that you understand Z-scores, let’s calculate one based on your inputs.")
    
    input_value = st.number_input("Enter a value to calculate its Z-score", value=0.0)
    input_z_score = (input_value - mean) / std_dev
    st.success(f"The Z-Score of {input_value} is: **{input_z_score:.2f}**")

    st.subheader("Z-Scores and Percentiles")
    st.write("""
    Z-scores can be mapped to **percentiles**. For example:
    
    - A Z-score of 0 is the 50th percentile (mean of the distribution).
    - A Z-score of +1.96 is roughly the 97.5th percentile.
    - A Z-score of -1.96 is roughly the 2.5th percentile.
    """)

    st.subheader("🕵️ Outlier Detection Using Z-Scores")
    st.write("""
    A Z-score helps detect **outliers**—data points far away from the mean. Common thresholds are:
    
    - Z-scores > +2 or Z-scores < -2 may indicate **outliers**.
    - Z-scores > +3 or Z-scores < -3 are **extreme outliers**.
    """)

    # Update progress
    st.session_state.progress = max(st.session_state.progress, 3)

# Module 4: Advanced Topics (Central Limit Theorem, Applications) with Varying Sample Size

# This module demonstrates the Central Limit Theorem (CLT) in action by allowing users to explore how increasing the sample size 
# affects the distribution of sample means.

# Key Features:
# 1. **Interactive Controls**:
#    - Users can adjust the **mean** and **standard deviation** for generating a non-normal population (Exponential distribution).
#    - The **sample size** can also be varied using a slider.
   
# 2. **Central Limit Theorem Visualization**:
#    - A non-normal distribution is generated, and multiple samples are drawn to compute their means.
#    - The resulting distribution of sample means is visualized using a histogram, demonstrating how the sample means approximate a normal distribution as sample size increases.

# 3. **Insights**:
#    - Explanation of how the **sample size** affects the distribution of sample means.
#    - Highlights the core principle of CLT: regardless of the population distribution, the distribution of sample means approaches normal as the sample size increases.


if module == "📊 Module 4: Advanced Topics":
    st.header("📊 Module 4: Central Limit Theorem (CLT)")

    st.subheader("Set Mean and Standard Deviation for CLT Analysis")
    
    # Independent sliders for Module 4 (mean and standard deviation)
    mean_4 = st.sidebar.slider("Mean (μ) for Module 4", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
    std_dev_4 = st.sidebar.slider("Standard Deviation (σ) for Module 4", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

    # Slider for sample size
    sample_size = st.sidebar.slider("Sample Size", min_value=5, max_value=500, value=30, step=5)

    st.subheader("🔄 Central Limit Theorem (CLT) in Action")
    st.write(f"""
    The **Central Limit Theorem (CLT)** states that as the **sample size increases**, the distribution of the sample mean 
    approaches a **normal distribution**—even if the underlying population is not normal.
    
    Let's generate a **non-normal distribution** and demonstrate how increasing the sample size affects the distribution of the sample means.
    
    - Population Distribution: Exponential distribution with mean = {mean_4:.2f} and standard deviation = {std_dev_4:.2f}
    """)

    # Generate non-normal data (Exponential distribution) based on the mean and std_dev
    population_data = np.random.exponential(scale=std_dev_4, size=1000) + mean_4  # Exponential shifted by the mean

    # Calculate sample means with varying sample sizes
    sample_means = [np.mean(np.random.choice(population_data, sample_size, replace=True)) for _ in range(500)]

    # Plot the distribution of the sample means
    fig_clt = px.histogram(sample_means, nbins=30, title=f"Distribution of Sample Means (Sample Size = {sample_size})")
    fig_clt.update_layout(
        xaxis_title='Sample Mean',
        yaxis_title='Frequency',
        showlegend=False,
        xaxis=dict(range=[-5, 5]), 
    )
    st.plotly_chart(fig_clt)

    st.write(f"""
    ### Insights:
    - With a **sample size of {sample_size}**, you can see how the sample means start to form a distribution that looks increasingly like a **normal distribution**.
    - As you increase the sample size, the distribution of sample means becomes narrower, centered around the true mean of the population.
    - This demonstrates the core idea of the **Central Limit Theorem**: regardless of the population distribution, the **distribution of sample means** approaches a normal distribution as the sample size increases.
    """)

    # Update progress
    st.session_state.progress = max(st.session_state.progress, 4)


# Module 5: Plotly Animation of Varying Mean and Standard Deviation

# This module features an interactive animation that dynamically demonstrates how changing the **mean** (μ) and **standard deviation** (σ) affects the shape and position of a normal distribution.

# Key Features:
# 1. **Animation**:
#    - The animation shows how the normal distribution curve shifts horizontally with changes in the mean and how the curve flattens or narrows as the standard deviation changes.
   
# 2. **Interactive Plotly Chart**:
#    - The chart is animated with 50 frames to smoothly transition through varying mean and standard deviation values.
#    - The layout includes a play/pause button, allowing users to control the animation.

# 3. **Visual Insights**:
#    - Users can observe how increasing the mean shifts the distribution along the x-axis, while increasing the standard deviation makes the curve wider and flatter, indicating more variability.


if module == "🎥 Module 5: Animated Normal Distributions":
    st.header("🎥 Module 5: Animated Normal Distributions")

    st.subheader("See How Varying Mean and Standard Deviation Affects the Curve")

    st.write("""
    This animation demonstrates how varying the **mean (μ)** and **standard deviation (σ)** dynamically affects the shape of the normal distribution.
    Watch how the curve changes as these two parameters are adjusted over time.
    """)

    # Parameters to vary
    mean_values = np.linspace(-5, 5, 50)  # 50 frames for mean variation
    std_dev_values = np.linspace(0.5, 2.5, 50)  # 50 frames for std dev variation

    # Generate x-values for plotting
    x = np.linspace(-20, 20, 1000)

    # Create figure for animation
    fig = go.Figure()

    # Initial frame
    initial_mean = mean_values[0]
    initial_std_dev = std_dev_values[0]
    y_initial = stats.norm.pdf(x, initial_mean, initial_std_dev)
    fig.add_trace(go.Scatter(x=x, y=y_initial, mode='lines', name=f'μ={initial_mean}, σ={initial_std_dev}'))

    # Create animation frames
    frames = []
    for i, (mean, std_dev) in enumerate(zip(mean_values, std_dev_values)):
        y = stats.norm.pdf(x, mean, std_dev)
        frames.append(go.Frame(data=[go.Scatter(x=x, y=y)], name=f'Frame {i}'))

    # Update layout for animation
    fig.update_layout(
        title="Animation of Normal Distribution Varying Mean and Standard Deviation",
        xaxis_title="X-axis",
        yaxis_title="Probability Density",
        xaxis=dict(range=[-20, 20]),  # Fixed range for x-axis
        yaxis=dict(range=[0, 0.5]),   # Fixed range for y-axis based on common normal distribution ranges
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]),
                                   dict(label="Pause",
                                        method="animate",
                                        args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])])]
    )

    # Add frames to the figure
    fig.frames = frames

    # Display the animated plotly chart
    st.plotly_chart(fig)

    st.write("""
    As you can see:
    - **Increasing the mean (μ)** shifts the peak of the distribution to the right.
    - **Increasing the standard deviation (σ)** flattens and widens the curve, indicating more variability.
    """)

    # Update progress
    st.session_state.progress = max(st.session_state.progress, 5)

# Module 6: Real-World Examples

# This module introduces real-world examples of Z-scores in various fields, providing practical context to the theoretical concepts learned in previous modules.


if module == "🌎 Module 6: Real-World Examples":
    st.header("🌎 Module 6: Real-World Applications of Z-Scores")

    st.subheader("📈 Finance")
    st.write("""
    In finance, Z-scores are used to **standardize returns** and identify outliers or extreme values in stock price movements. 
    For example, a Z-score of +3 might indicate that a stock’s price is unusually high relative to its historical mean.
    """)

    st.subheader("⚕️ Healthcare")
    st.write("""
    Z-scores are often used in **healthcare** to assess how a patient’s test results compare to the population. 
    For example, a Z-score can help doctors identify if a patient’s cholesterol level is significantly higher or lower than average.
    """)

    st.subheader("📊 Research")
    st.write("""
    Z-scores are a key tool in **scientific research** for comparing results across different experiments or datasets, standardizing data from different populations, and detecting outliers.
    """)

    # Update progress
    st.session_state.progress = max(st.session_state.progress, 6)

### Progress Tracker in Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Your Learning Progress")

# Progress bar based on modules completed
progress = st.sidebar.progress(st.session_state.progress / 6)
st.sidebar.write(f"Modules Completed: {st.session_state.progress}/6")
