import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# 세균 증식 모델 (로지스틱 성장식)
# =============================
def logistic_growth(t, N0, r, K):
    """
    로지스틱 성장 모델
    N(t) = K / (1 + ((K - N0)/N0) * exp(-r*t))
    """
    return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

# =============================
# Streamlit 기본 설정
# =============================
st.set_page_config(page_title="세균 증식 시뮬레이터", page_icon="🧫", layout="wide")

st.title("🧫 세균 증식 시뮬레이터")
st.markdown(
    """
세균 집단은 시간이 지남에 따라 **S자형(sigmoid) 성장 곡선**을 보입니다.  
사이드바에서 초기 개체수, 성장률, 환경 수용력을 조절해보고 집단 크기 변화를 확인하세요.
    """
)

# =============================
# 사이드바: 매개변수 입력
# =============================
with st.sidebar:
    st.header("⚙️ 매개변수 설정")
    N0 = st.slider("초기 개체수 (N₀)", 1, 100, 10)   # 초기값
    r = st.slider("성장률 (r)", 0.01, 1.0, 0.2, 0.01) # 세균 증식 속도
    K = st.slider("환경 수용력 (K)", 50, 2000, 500, 10) # 최대 개체수
    T = st.slider("총 시간 (t max)", 10, 200, 50, 1)   # 시뮬레이션 시간
    dt = st.slider("시간 간격 (Δt)", 0.1, 5.0, 1.0, 0.1) # 시간 해상도

# =============================
# 시뮬레이션 실행
# =============================
t = np.arange(0, T+dt, dt)        # 시간 벡터
N = logistic_growth(t, N0, r, K)  # 세균 개체수 계산

# DataFrame으로 변환 (그래프 & 다운로드용)
df = pd.DataFrame({"time": t, "bacteria": N})

# =============================
# 결과 시각화
# =============================
col1, col2 = st.columns([1.2, 1])

# Streamlit 내장 line_chart
with col1:
    st.subheader("📈 세균 개체수 시간 변화")
    st.line_chart(df.set_index("time"))

# Matplotlib 그래프
with col2:
    st.subheader("📊 성장 곡선 (Matplotlib)")
    fig, ax = plt.subplots(figsize=(5,4))
    ax.plot(t, N, label="세균 개체수", color="green")
    ax.set_xlabel("시간")
    ax.set_ylabel("개체수")
    ax.set_title("세균 증식 곡선")
    ax.legend()
    st.pyplot(fig, use_container_width=True)

# =============================
# 데이터 다운로드 기능
# =============================
st.divider()
st.subheader("💾 데이터 다운로드")
st.download_button(
    label="CSV 다운로드",
    data=df.to_csv(index=False),
    file_name="bacteria_growth.csv",
    mime="text/csv",
)

# =============================
# 학습 포인트 설명
# =============================
with st.expander("📚 학습 포인트"):
    st.markdown(
        """
- **지수적 증가기**: 초기에는 빠르게 증가 (자원이 충분).
- **정체기**: 개체 수가 커질수록 성장률 감소.
- **환경 수용력(K)**에 가까워질수록 성장이 멈춤.
- 실제 세균 배양 실험에서도 유사한 곡선을 관찰할 수 있습니다.
        """
    )
