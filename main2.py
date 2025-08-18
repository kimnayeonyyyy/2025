import streamlit as st
import time, random

st.set_page_config(page_title="⏱ 빠른 클릭 게임", page_icon="🎮", layout="centered")

st.markdown("<h1 style='text-align:center; color:#00b894;'>⏱ 빠른 클릭 게임 🎯</h1>", unsafe_allow_html=True)

# --------------------------
# 세션 초기화
# --------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.waiting = False
    st.session_state.start_time = None
    st.session_state.reaction_time = None
    st.session_state.best_time = None

# --------------------------
# 게임 시작 버튼
# --------------------------
if not st.session_state.game_started:
    if st.button("▶️ 게임 시작"):
        st.session_state.game_started = True
        st.session_state.waiting = True
        st.session_state.reaction_time = None
        st.session_state.start_time = None
        st.experimental_rerun()

# --------------------------
# 빨간불 대기 상태
# --------------------------
elif st.session_state.waiting:
    st.markdown("<h2 style='text-align:center; color:red;'>🔴 준비하세요...</h2>", unsafe_allow_html=True)

    # 랜덤 시간 후 초록불로 전환
    wait_time = random.uniform(2, 5)
    time.sleep(wait_time)
    st.session_state.waiting = False
    st.session_state.start_time = time.time()
    st.experimental_rerun()

# --------------------------
# 초록불 반응 대기
# --------------------------
elif st.session_state.start_time is not None and st.session_state.reaction_time is None:
    st.markdown("<h2 style='text-align:center; color:green;'>🟢 클릭하세요!</h2>", unsafe_allow_html=True)

    if st.button("클릭!"):
        st.session_state.reaction_time = round((time.time() - st.session_state.start_time) * 1000, 2)

        # 최고 기록 저장
        if st.session_state.best_time is None or st.session_state.reaction_time < st.session_state.best_time:
            st.session_state.best_time = st.session_state.reaction_time

        st.experimental_rerun()

# --------------------------
# 결과 출력
# --------------------------
elif st.session_state.reaction_time is not None:
    st.success(f"⚡ 반응 속도: **{st.session_state.reaction_time} ms**")

    if st.session_state.best_time:
        st.info(f"🏆 최고 기록: **{st.session_state.best_time} ms**")

    if st.button("🔄 다시 도전하기"):
        st.session_state.game_started = False
        st.session_state.waiting = False
        st.session_state.start_time = None
        st.session_state.reaction_time = None
        st.experimental_rerun()

