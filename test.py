import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# Logistic growth model
# =============================
def logistic_growth(t, N0, r, K):
    return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

# =============================
# Streamlit basic config
# =============================
st.set_page_config(page_title="Bacterial Growth Simulator", page_icon="🧫", layout="wide")

st.title("🧫 Bacterial Growth Simulator")
st.markdown(
    """
Bacterial populations often show an **S-shaped (sigmoid) growth curve** over time.  
Adjust the parameters in the sidebar and observe how the population changes.
    """
)

# =============================
# Sidebar controls
# =============================
with st.sidebar:
    st.header("⚙️ Parameters")
    N0 = st.slider("Initial population (N₀)", 1, 100, 10)
    r = st.slider("Growth rate (r)", 0.01, 1.0, 0.2, 0.01)
    K = st.slider("Carrying capacity (K)", 50, 2000, 500, 10)
    T = st.slider("Total time (t max)", 10, 200, 50, 1)
    dt = st.slider("Time step (Δt)", 0.1, 5.0, 1.0, 0.1)

    st.subheader("🌍 Environment change")
    event_time = st.slider("Change time", 0, T, int(T/2))
    event_type = st.selectbox("Change type", ["None", "Add nutrients", "Antibiotics", "Resource loss"])

# =============================
# Simulation with environment change
# =============================
t = np.arange(0, T+dt, dt)

# Split before and after event
before_mask = t <= event_time
after_mask = t > event_time

N_before = logistic_growth(t[before_mask], N0, r, K)

# Apply environmental change
N0_event = N_before[-1]
r2, K2 = r, K

if event_type == "Add nutrients":
    K2 = int(K * 1.5)
elif event_type == "Antibiotics":
    r2 = r * 0.5
    N0_event = N0_event * 0.7  # sudden drop
elif event_type == "Resource loss":
    K2 = int(K * 0.5)

N_after = logistic_growth(t[after_mask] - event_time, N0_event, r2, K2)

# Combine
N = np.concatenate([N_before, N_after])
df = pd.DataFrame({"time": t, "bacteria": N})

# =============================
# Visualization
# =============================
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📈 Population over time")
    st.line_chart(df.set_index("time"))

with col2:
    st.subheader("📊 Growth curve (Matplotlib)")
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(t, N, label="Bacterial population", color="green")

    # Mark carrying capacity line
    ax.axhline(K, color="gray", linestyle="--", linewidth=1, label="Initial K")
    if event_type != "None":
        ax.axhline(K2, color="blue", linestyle=":", linewidth=1, label="New K")
        ax.axvline(event_time, color="red", linestyle="--", linewidth=1, label="Environment change")

    # Annotate phases
    ax.text(T*0.1, K*0.2, "Exponential phase", fontsize=8, color="darkgreen")
    ax.text(T*0.6, K*0.9, "Stationary phase", fontsize=8, color="brown")

    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.set_title("Bacterial Growth Curve with Environment Change")
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
- **Environmental change** can alter K or r:
  - Nutrients added → higher K.
  - Antibiotics → lower r, sudden population drop.
  - Resource loss → smaller K.
        """
    )
