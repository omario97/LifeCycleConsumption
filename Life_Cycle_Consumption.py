import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculate_values(rho, r, a0, aT, T):
    # Analytical solution
    c0_true = (rho * (aT * np.exp(-r*T) - a0)) / (np.exp(-rho*T) - 1)
    def a_true(t, c0_true):
        return np.exp(r*t) * ((1/rho) * c0_true * np.exp(-rho*t) + a0 - (1/rho) * c0_true)
    def c_true(t, c0_true):
        return c0_true * np.exp((r-rho)*t)
    # Create a vector of input (for different values of the functions)
    t_vector = np.arange(1, T+1)
    a_true_values = np.array([a_true(t, c0_true) for t in t_vector])
    c_true_values = np.array([c_true(t, c0_true) for t in t_vector])
    return t_vector, a_true_values, c_true_values

def create_plot(t_vector, a_true_values, c_true_values):
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=('Assets over time(t)',
                                        'Optimal consumption over time(t)'))
    fig.add_trace(
        go.Scatter(x=t_vector, y=a_true_values, mode='lines', name='a(t)', line=dict(color='green')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=t_vector, y=c_true_values, mode='lines', name='c(t)', line=dict(color='purple')),
        row=2, col=1
    )
    fig.update_layout(
        title_text='Life-cycle Consumption Problem',
        height=700,
        showlegend=False
    )
    fig.update_xaxes(title_text='Time', row=1, col=1)
    fig.update_xaxes(title_text='Time', row=2, col=1)
    fig.update_yaxes(title_text='a(t)', row=1, col=1)
    fig.update_yaxes(title_text='c(t)', row=2, col=1)
    return fig

def main():
    st.set_page_config(page_title="Life-cycle Consumption Problem", layout="wide")
    st.title("Life-cycle Consumption Problem")

    # Add LinkedIn profile in the sidebar
    st.sidebar.markdown(
        """
        <a href="https://www.linkedin.com/in/omar-hussain-504777164/" target="_blank">
            <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20" height="20" /> 
            Omar Hussain
        </a>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("Parameter Settings")
    rho = st.sidebar.slider("ρ (rho)", min_value=0.01, max_value=0.10, value=0.05, step=0.01)
    r = st.sidebar.slider("r", min_value=0.01, max_value=0.10, value=0.06, step=0.01)
    T = st.sidebar.slider("T (Time Horizon)", min_value=2, max_value=100, value=100, step=1)
    
    a0 = 1  # Initial assets
    aT = 0  # Terminal assets
    
    t_vector, a_true_values, c_true_values = calculate_values(rho, r, a0, aT, T)
    fig = create_plot(t_vector, a_true_values, c_true_values)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### Model Description
    This app demonstrates the Life-cycle Consumption Problem, which models how an individual might optimally consume resources over their lifetime.
    - **a(t)**: Assets over time
    - **c(t)**: Optimal consumption over time
    - **ρ (rho)**: Consumption rate
    - **r**: Interest rate (Interest income rate)
    - **T**: Time horizon
    
    Adjust the parameters in the sidebar to see how they affect the optimal consumption and asset paths.
    
    Created by Omar Hussain
                       
    References:
   
    Journal:
    Gourinchas, P. O., & Parker, J. A. (2002). Consumption Over the Life Cycle. Econometrica, 70(1), 47-89.
   
    Others:
    Investopedia's article on the Life-Cycle Hypothesis: https://www.investopedia.com/terms/l/life-cycle-hypothesis.asp
    Economics Help's explanation: https://www.economicshelp.org/blog/27080/concepts/life-cycle-hypothesis/
    """)

if __name__ == "__main__":
    main()