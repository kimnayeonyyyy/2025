import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# Bacterial growth model (Logistic growth)
# =============================
def logistic_growth(t, N0, r, K):
    """
    Logistic growth model
    N(t) = K / (1 + ((K - N0)/N0) * exp(-r*t))
    """
    return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

# =============================
# Streamlit basic config
# =============================
st.set_page_config(page_title="Bacterial Growth Simulator", page_icon="🧫", layout="wide")

st.title("🧫 Bacterial Growth Simulator")
st.markdown(
    """
Bacterial populations often show an **S-shaped (sigmoid) growth curve** over time.  
Adjust the initial population, growth rate, and carrying capacity in the sidebar and observe how the population changes.
    """
)

# =============================
# Sidebar controls
# =============================
with st.sidebar:
    st.header("⚙️ Parameters")
    N0 = st.slider("Initial population (N₀)", 1, 100, 10)   # initial value
    r = st.slider("Growth rate (r)", 0.01, 1.0, 0.2, 0.01) # growth rate
    K = st.slider("Carrying capacity (K)", 50, 2000, 500, 10) # maximum population
    T = st.slider("Total time (t max)", 10, 200, 50, 1)   # simulation time
    dt = st.slider("Time step (Δt)", 0.1, 5.0, 1.0, 0.1) # resolution

# =============================
# Simulation
# =============================
t = np.arange(0, T+dt, dt)        # time vector
N = logistic_growth(t, N0, r, K)  # bacterial population

# DataFrame for plotting and download
df = pd.DataFrame({"time": t, "bacteria": N})

# =============================
# Visualization
# =============================
col1, col2 = st.columns([1.2, 1])

# Streamlit built-in line_chart
with col1:
    st.subheader("📈 Population over time")
    st.line_chart(df.set_index("time"))

# Matplotlib graph
with col2:
    st.subheader("📊 Growth curve (Matplotlib)")
    fig, ax = plt.subplots(figsize=(5,4))
    ax.plot(t, N, label="Bacterial population", color="green")
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.set_title("Bacterial Growth Curve")
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# =============================
# Download data
# =============================
st.divider()
st.subheader("💾 Download data")
st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False),
    file_name="bacteria_growth.csv",
    mime="text/csv",
)

# =============================
# Learning points
# =============================
with st.expander("📚 Learning points"):
    st.markdown(
        """
- **Exponential phase**: rapid growth at the beginning (resources are abundant).
- **Stationary phase**: growth slows down due to limited resources.
- **Carrying capacity (K)**: population size levels off near K.
- Real bacterial cultures often show a very similar curve.
        """
    )
