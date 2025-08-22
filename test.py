import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="생명↔지구 시뮬레이션 v3", layout="wide")
st.title("🌍 생명 활동 ↔ 지구 환경 시뮬레이션 (그래프 설명 강화)")

# -------------------
# 사용자 입력
# -------------------
st.sidebar.header("환경/세포 설정")
base_photosynth = st.sidebar.slider("기본 광합성 효율 (%)", 50, 150, 100)
base_respiration = st.sidebar.slider("기본 세포 호흡율 (%)", 50, 150, 100)
forest_area = st.sidebar.slider("숲 면적 (%)", 10, 100, 50)
ocean_area = st.sidebar.slider("해양 흡수율 (%)", 10, 100, 50)
max_years = st.sidebar.number_input("최대 시뮬레이션 연도", 1, 100, 50)
scenario_noise = st.sidebar.slider("연도별 변동 폭 (%)", 0, 50, 10)

# -------------------
# 세션 상태 초기화
# -------------------
for key, default in {
    "year": 0,
    "co2_ppm": [415],
    "temp": [15],
    "photosynth_history": [0],
    "respiration_history": [0],
    "photosynth_eff_history": [base_photosynth],
    "respiration_eff_history": [base_respiration]
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------
# 1년 시뮬레이션
# -------------------
def simulate_one_year():
    total_cells = 1e18
    ph_eff = base_photosynth * (1 + random.uniform(-scenario_noise/100, scenario_noise/100))
    resp_eff = base_respiration * (1 + random.uniform(-scenario_noise/100, scenario_noise/100))
    ph_eff *= max(0.5, 1 - 0.001*(st.session_state.co2_ppm[-1]-415))  # CO₂ 피드백

    photosynth = total_cells * 1 * (ph_eff/100) * (forest_area/50)
    respiration = total_cells * 1 * (resp_eff/100)
    ocean_absorb = total_cells * 0.3 * (ocean_area/50)

    net_co2 = respiration - photosynth - ocean_absorb
    co2_next = st.session_state.co2_ppm[-1] + net_co2 / 1e16
    temp_next = 15 + (co2_next - 415) * 0.01

    return co2_next, temp_next, photosynth, respiration, ph_eff, resp_eff

# -------------------
# 버튼으로 연도 진행
# -------------------
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ 이전 년도") and st.session_state.year > 0:
        st.session_state.year -= 1
with col2:
    if st.button("➡️ 다음 년도") and st.session_state.year < max_years:
        if st.session_state.year == len(st.session_state.co2_ppm) - 1:
            co2, temp, photo, resp, ph_eff, resp_eff = simulate_one_year()
            st.session_state.co2_ppm.append(co2)
            st.session_state.temp.append(temp)
            st.session_state.photosynth_history.append(photo)
            st.session_state.respiration_history.append(resp)
            st.session_state.photosynth_eff_history.append(ph_eff)
            st.session_state.respiration_eff_history.append(resp_eff)
        st.session_state.year += 1

# -------------------
# 시각화
# -------------------
year_idx = st.session_state.year
years = range(year_idx+1)

fig, ax = plt.subplots(1,4, figsize=(20,5))

# 1️⃣ CO₂ 농도 변화
ax[0].plot(years, st.session_state.co2_ppm[:year_idx+1], marker='o', color='green')
ax[0].set_title("📈 대기 CO₂ 농도 변화\n세포 호흡과 광합성의 순 영향")
ax[0].set_xlabel("연도"); ax[0].set_ylabel("CO₂ (ppm)")

# 2️⃣ 지구 평균 온도
ax[1].plot(years, st.session_state.temp[:year_idx+1], marker='o', color='orange')
ax[1].set_title("🌡️ 지구 평균 온도 변화\n대기 CO₂ 증가로 인한 온도 상승")
ax[1].set_xlabel("연도"); ax[1].set_ylabel("평균 온도 (°C)")

# 3️⃣ 광합성 vs 호흡 누적
ax[2].bar(years, st.session_state.photosynth_history[:year_idx+1], label="광합성", alpha=0.6)
ax[2].bar(years, st.session_state.respiration_history[:year_idx+1], label="세포 호흡", alpha=0.6)
ax[2].set_title("🌱 연도별 누적 광합성 vs 세포 호흡\n각 연도의 총 CO₂ 흡수/배출량")
ax[2].set_xlabel("연도"); ax[2].set_ylabel("누적 단위"); ax[2].legend()

# 4️⃣ 효율 변화
ax[3].plot(years, st.session_state.photosynth_eff_history[:year_idx+1], color='green', label='광합성 효율')
ax[3].plot(years, st.session_state.respiration_eff_history[:year_idx+1], color='red', label='호흡 효율')
ax[3].set_title("⚡ 연도별 광합성/호흡 효율 변화\n연도별 변동과 CO₂ 피드백 반영")
ax[3].set_xlabel("연도"); ax[3].set_ylabel("%"); ax[3].legend()

st.pyplot(fig)
st.info(f"연도: {year_idx} | CO₂: {st.session_state.co2_ppm[year_idx]:.2f} ppm | 평균 온도: {st.session_state.temp[year_idx]:.2f} °C")
