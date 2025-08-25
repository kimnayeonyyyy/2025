import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# Logistic Growth Model Function
# =====================================
def logistic_growth(t, N0, r, K):
    """
    Logistic growth function.
    Parameters:
        t  (array): Time values
        N0 (float): Initial population size
        r  (float): Growth rate
        K  (float): Carrying capacity
    Returns:
        array: Population at each time t
    """
    return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

# =====================================
# Streamlit App Configuration
# =====================================
st.set_page_config(page_title="세균 성장 시뮬레이터", page_icon="🧫", layout="wide")

st.title("🧫 세균 성장 시뮬레이터")
st.markdown(
    """
세균 집단은 시간에 따라 보통 **S자 모양(시그모이드) 성장 곡선**을 보입니다.  
사이드바에서 매개변수를 조절하고 세균 수가 어떻게 변하는지 살펴보세요.
    """
)

# =====================================
# Sidebar: User Controls
# =====================================
with st.sidebar:
    st.header("⚙️ 매개변수 설정")
    N0 = st.slider("초기 개체수 (N₀)", 1, 100, 10)
    r = st.slider("성장률 (r)", 0.01, 1.0, 0.2, 0.01)
    K = st.slider("수용력 (K)", 50, 2000, 500, 10)
    T = st.slider("총 시간 (t max)", 10, 200, 50, 1)
    dt = st.slider("시간 간격 (Δt)", 0.1, 5.0, 1.0, 0.1)

    st.subheader("🌍 환경 변화")
    event_time = st.slider("환경 변화 시점", 0, T, int(T/2))
    event_type = st.selectbox("변화 종류", ["없음", "영양분 추가", "항생제 투여", "자원 손실"])

# =====================================
# Simulation Logic
# =====================================
# Time array
t = np.arange(0, T+dt, dt)

# Population before event
before_mask = t <= event_time
N_before = logistic_growth(t[before_mask], N0, r, K)

# Parameters after environmental change
N0_event = N_before[-1]  # new initial population after event
r2, K2 = r, K

if event_type == "영양분 추가":
    K2 = int(K * 1.5)
elif event_type == "항생제 투여":
    r2 = r * 0.5
    N0_event = N0_event * 0.7  # sudden drop
elif event_type == "자원 손실":
    K2 = int(K * 0.5)

# Population after event
after_mask = t > event_time
N_after = logistic_growth(t[after_mask] - event_time, N0_event, r2, K2)

# Combine before/after
total_population = np.concatenate([N_before, N_after])

# DataFrame for plotting
df = pd.DataFrame({"시간": t, "세균 개체수": total_population})

# =====================================
# Visualization
# =====================================
col1, col2 = st.columns([1.2, 1])

# 1) Streamlit default line chart (raw data)
with col1:
    st.subheader("📈 시간에 따른 세균 개체수")
    st.line_chart(df.set_index("시간"))

# 2) Matplotlib graph with scientific interpretation
with col2:
    st.subheader("📊 Growth curve (Matplotlib)")
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(t, total_population, label="Bacterial population", color="green")

    # Carrying capacity lines
    if event_type == "없음" or np.isclose(K2, K):
        ax.axhline(K, color="gray", linestyle="--", linewidth=1, label="K (carrying capacity)")
    else:
        ax.hlines(K, xmin=t[0], xmax=event_time, colors="gray", linestyles="--", linewidth=1, label="Initial K")
        ax.hlines(K2, xmin=event_time, xmax=t[-1], colors="blue", linestyles=":", linewidth=1, label="New K")
        ax.axvline(event_time, color="red", linestyle="--", linewidth=1, label="Environment change")

    # Growth phases annotation
    ax.text(T*0.1, K*0.2, "Exponential phase", fontsize=8, color="darkgreen")
    ax.text(T*0.6, K*0.9, "Stationary phase", fontsize=8, color="brown")

    # Labels and legend
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.set_title("Bacterial growth curve with environmental change")
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# =====================================
# Data Download Section
# =====================================
st.divider()
st.subheader("💾 데이터 다운로드")
st.download_button(
    label="CSV 다운로드",
    data=df.to_csv(index=False),
    file_name="bacteria_growth.csv",
    mime="text/csv",
)

# =====================================
# Learning Points Section
# =====================================
with st.expander("📚 학습 포인트"):
    st.markdown(
        """
- **지수 성장기 (Exponential phase)**: 자원이 충분하여 빠르게 증가하는 시기
- **정체기 (Stationary phase)**: 자원이 부족해져 개체수가 일정해지는 시기
- **수용력 (K, Carrying capacity)**: 환경이 지탱할 수 있는 최대 개체수
- **환경 변화**에 따라 K 또는 r이 달라질 수 있음:
  - 영양분 추가 → K 증가
  - 항생제 투여 → r 감소, 개체수 급격히 감소
  - 자원 손실 → K 감소
        """
    )
