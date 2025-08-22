import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="생명↔지구 시뮬레이션", layout="wide")
st.title("🌍 생명 활동과 지구 환경 연결 시뮬레이션")

# -------------------
# 사용자 입력
# -------------------
st.sidebar.header("세포/환경 설정")
photosynthesis_eff = st.sidebar.slider("광합성 효율 (%)", 50, 150, 100)
respiration_eff = st.sidebar.slider("세포 호흡율 (%)", 50, 150, 100)
forest_area = st.sidebar.slider("숲 면적 비율 (%)", 10, 100, 50)
ocean_area = st.sidebar.slider("해양 흡수율 (%)", 10, 100, 50)
years_to_simulate = st.sidebar.number_input("시뮬레이션 기간 (년)", 1, 100, 50)

# -------------------
# 초기값 설정
# -------------------
if "year" not in st.session_state:
    st.session_state.year = 0
    st.session_state.co2_ppm = [415]  # 초기 CO₂ 농도 ppm
    st.session_state.temp = [15]      # 초기 평균 기온 °C

# -------------------
# 시뮬레이션 함수
# -------------------
def simulate_one_year(co2_current):
    # 단순 모델:
    # CO₂ 변화 = 세포 호흡 - 광합성 + 기타 흡수(숲/해양)
    total_cells = 1e18  # 지구 전체 세포 수 (단순화)
    photosynthesis = total_cells * 1 * (photosynthesis_eff/100) * (forest_area/50)
    respiration = total_cells * 1 * (respiration_eff/100)
    ocean_absorption = total_cells * 0.3 * (ocean_area/50)

    net_co2 = respiration - photosynthesis - ocean_absorption
    co2_next = co2_current + net_co2 / 1e16  # 스케일 조정
    # CO₂ 농도 증가 1ppm → 온도 0.01°C 상승
    temp_next = 15 + (co2_next - 415) * 0.01
    return co2_next, temp_next

# -------------------
# 버튼 클릭 시 1년 진행
# -------------------
col1, col2 = st.columns(2)
with col1:
    if st.button("➡️ 다음 년도"):
        co2, temp = simulate_one_year(st.session_state.co2_ppm[-1])
        st.session_state.co2_ppm.append(co2)
        st.session_state.temp.append(temp)
        st.session_state.year += 1
with col2:
    if st.button("⬅️ 이전 년도") and st.session_state.year > 0:
        st.session_state.year -= 1

# -------------------
# 현재 년도 시각화
# -------------------
year_idx = st.session_state.year
st.subheader(f"연도: {year_idx}")

fig, ax = plt.subplots(1,2, figsize=(12,5))

# CO2 농도 그래프
ax[0].plot(range(year_idx+1), st.session_state.co2_ppm[:year_idx+1], marker='o')
ax[0].set_xlabel("Year")
ax[0].set_ylabel("대기 CO₂ (ppm)")
ax[0].set_title("대기 CO₂ 변화")

# 온도 그래프
ax[1].plot(range(year_idx+1), st.session_state.temp[:year_idx+1], color='orange', marker='o')
ax[1].set_xlabel("Year")
ax[1].set_ylabel("지구 평균 온도 (°C)")
ax[1].set_title("지구 평균 온도 변화")

st.pyplot(fig)
st.info(f"CO₂: {st.session_state.co2_ppm[year_idx]:.2f} ppm | 온도: {st.session_state.temp[year_idx]:.2f} °C")
