import streamlit as st
import numpy as np
import pandas as pd
import io

# =============================
# Utility: RK4 integrator
# =============================
def rk4(f, y0, t, params):
    y = np.zeros((len(t), len(y0)), dtype=float)
    y[0] = y0
    for i in range(len(t) - 1):
        h = t[i+1] - t[i]
        k1 = f(t[i], y[i], params)
        k2 = f(t[i] + 0.5*h, y[i] + 0.5*h*k1, params)
        k3 = f(t[i] + 0.5*h, y[i] + 0.5*h*k2, params)
        k4 = f(t[i] + h, y[i] + h*k3, params)
        y[i+1] = y[i] + (h/6.0) * (k1 + 2*k2 + 2*k3 + k4)
        y[i+1] = np.maximum(y[i+1], 0.0)  # keep non-negative
    return y

# =============================
# Model definitions
# =============================
def lotka_volterra(t, y, p):
    x, v = y  # prey, predator
    a, b, g, d, logistic, K, noise = p
    # dx/dt = a*x - b*x*v (or logistic: a*x*(1 - x/K) - b*x*v)
    growth = a*x if not logistic else a*x*(1 - x/max(K, 1e-12))
    dxdt = growth - b*x*v
    dvdt = d*x*v - g*v
    if noise > 0:
        # Add small multiplicative noise (Stratonovich-ish, discretized later)
        dxdt += noise * x * np.random.normal(0, 1)
        dvdt += noise * v * np.random.normal(0, 1)
    return np.array([dxdt, dvdt])

# =============================
# Streamlit UI
# =============================
st.set_page_config(page_title="포식자-피식자 시뮬레이터", page_icon="🦊", layout="wide")

st.title("🦊🐇 포식자-피식자 시뮬레이터 (Lotka–Volterra)")
st.markdown(
    """
수학적 생태계 모델인 **Lotka–Volterra 방정식**으로 포식자-피식자 상호작용을 시뮬레이션합니다.
왼쪽 사이드바에서 매개변수를 조절해 개체수 변화와 위상공간(phase plane)을 관찰해보세요.

- 기본 모델: $$\dot x = ax - bxy,\ \ \dot y = dxy - gy$$
- 선택 옵션: 먹이(피식자)의 **로지스틱 성장**(수용력 *K*)과 **확률적 변동(노이즈)**
    """
)

with st.sidebar:
    st.header("⚙️ 매개변수 설정")
    st.caption("단위는 임의 단위")

    colA, colB = st.columns(2)
    with colA:
        a = st.slider("a (피식자 성장률)", 0.0, 3.0, 1.0, 0.01)
        g = st.slider("g (포식자 자연사망률)", 0.0, 3.0, 1.0, 0.01)
        x0 = st.number_input("초기 피식자 x₀", min_value=0.0, value=40.0, step=1.0)
    with colB:
        b = st.slider("b (포식률 계수)", 0.0, 0.3, 0.02, 0.001)
        d = st.slider("d (포식→성장 전환 효율)", 0.0, 0.3, 0.01, 0.001)
        y0 = st.number_input("초기 포식자 y₀", min_value=0.0, value=9.0, step=1.0)

    logistic = st.toggle("피식자 로지스틱 성장 사용 (수용력 K)", value=False)
    K = st.slider("K (수용력)", 10.0, 1000.0, 200.0, 1.0, disabled=not logistic)

    st.divider()
    st.subheader("⏱️ 시뮬레이션 설정")
    T = st.slider("총 시간 (T)", 10.0, 500.0, 200.0, 1.0)
    dt = st.slider("시간 간격 (Δt)", 0.001, 1.0, 0.05, 0.001)

    st.divider()
    noise = st.slider("확률적 변동 강도 (0=없음)", 0.0, 0.1, 0.0, 0.005)

    st.divider()
    default_btn = st.button("🔄 기본값으로 리셋", use_container_width=True)

if default_btn:
    st.experimental_rerun()

params = (a, b, g, d, logistic, K, noise)

# Time vector
N = int(T/dt) + 1
# Clamp to avoid excessive memory usage
N = min(N, 200_000)
t = np.linspace(0, dt*(N-1), N)

# Run simulation
np.random.seed(0)  # deterministic randomness for reproducibility inside a run
sol = rk4(lotka_volterra, y0=np.array([x0, y0]), t=t, params=params)
x, y = sol[:, 0], sol[:, 1]

# Dataframe for plotting and download
df = pd.DataFrame({"time": t, "prey": x, "predator": y})

# ===============
# Layout
# ===============
left, right = st.columns([1.1, 1])

with left:
    st.subheader("📈 개체수 시간 변화")
    st.line_chart(df.set_index("time"))

with right:
    st.subheader("🌪️ 위상공간 (x-y)")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    ax.plot(x, y, lw=1.8)
    ax.set_xlabel("피식자 x")
    ax.set_ylabel("포식자 y")
    ax.set_title("Phase Plane")

    # Nullclines & equilibrium
    if not logistic:
        # y-nullcline (dy/dt=0): x = g/d ; x-nullcline (dx/dt=0): y = a/b
        x_eq = g / max(d, 1e-12) if d > 0 else None
        y_eq = a / max(b, 1e-12) if b > 0 else None
        if x_eq is not None and y_eq is not None:
            ax.axvline(x_eq, ls='--', lw=1)
            ax.axhline(y_eq, ls='--', lw=1)
            ax.scatter([x_eq], [y_eq], s=60, zorder=5)
    else:
        # For logistic prey: x-nullcline solves a*(1 - x/K) - b*y = 0 -> y = a(1 - x/K)/b
        xs = np.linspace(0, max(max(x)*1.1, K*1.1), 200)
        if b > 0:
            ys_nc = a * (1 - xs/ max(K, 1e-12)) / b
            ax.plot(xs, ys_nc, ls='--', lw=1)
        if d > 0:
            x_nc = g / d
            ax.axvline(x_nc, ls='--', lw=1)

    st.pyplot(fig, use_container_width=True)

st.divider()

# Equilibrium info
st.subheader("🔎 균형점(평형) 정보")
if not logistic:
    if b > 0 and d > 0:
        x_star = g / d
        y_star = a / b
        st.markdown(
            f"**내부 평형점:** (x*, y*) = ( {x_star:.3f}, {y_star:.3f} )  "+
            "(고전 LV에서는 주기적 궤도 근처에서 진동)"
        )
    else:
        st.info("b와 d가 0보다 커야 내부 평형점이 존재합니다.")
else:
    if d > 0 and b > 0:
        x_star = g / d
        y_star = a * (1 - x_star / max(K,1e-12)) / b
        st.markdown(
            f"**내부 평형점(로지스틱):** (x*, y*) = ( {x_star:.3f}, {y_star:.3f} )"
        )
        if y_star < 0:
            st.warning("이 매개변수에서는 내부 평형점의 y*가 음수이므로 실질적으로 포식자 멸종 상태가 됩니다.")
    else:
        st.info("b와 d가 0보다 커야 내부 평형점이 정의됩니다.")

# =============================
# Download
# =============================
st.subheader("💾 데이터 다운로드")
buf = io.StringIO()
df.to_csv(buf, index=False)
st.download_button(
    label="CSV 다운로드",
    data=buf.getvalue(),
    file_name="lotka_volterra_simulation.csv",
    mime="text/csv",
)

# Tips
with st.expander("📚 사용 팁 & 확장 아이디어"):
    st.markdown(
        """
- **학습 포인트**: a↑ → 피식자 증가, b↑ → 포식 효율 증가(피식자 감소), d↑ → 포식이 포식자 성장으로 잘 전환, g↑ → 포식자 자연감소.
- **로지스틱 성장**을 켜면 환경 수용력 *K* 때문에 피식자 무한 증가는 억제됩니다.
- **위상공간**에서 점선(nullcline)과 점(평형점)을 기준으로 궤도의 흐름을 해석해보세요.
- **확장**: (1) 계절성(주기적으로 a, g 변화), (2) 3종 상호작용(최상위 포식자 추가), (3) 공간 확산(격자 지도) 등.
        """
    )
