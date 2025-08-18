import streamlit as st
import random, time

st.set_page_config(page_title="🃏 기억력 카드 뒤집기", page_icon="🎮", layout="centered")

# --------------------------
# CSS (플립 애니메이션 + 랜덤 컬러 스타일)
# --------------------------
st.markdown(
    """
    <style>
    .grid {
        display: grid;
        grid-template-columns: repeat(4, 100px);
        justify-content: center;
        gap: 15px;
    }
    .card-container {
        perspective: 1000px;
    }
    .card {
        width: 100px;
        height: 120px;
        position: relative;
        transform-style: preserve-3d;
        transition: transform 0.6s;
        cursor: pointer;
        border-radius: 15px;
    }
    .card.flipped {
        transform: rotateY(180deg);
    }
    .card-face {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        font-weight: bold;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
    }
    .front {
        background: linear-gradient(135deg, #ff9a9e, #fad0c4);
        color: white;
    }
    .back {
        transform: rotateY(180deg);
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center; color:#ff69b4;'>🌸 기억력 카드 뒤집기 🎮</h1>", unsafe_allow_html=True)

# --------------------------
# 난이도 선택
# --------------------------
difficulty = st.radio("난이도를 선택하세요 🎯", ["쉬움 (3쌍)", "보통 (6쌍)", "어려움 (8쌍)"])

emoji_pool = ["🍎","🍊","🍇","🍉","🍓","🍍","🍒","🥝","🥑","🥕","🥦","🌽","🍋","🍐","🥥","🍌"]

if difficulty.startswith("쉬움"):
    num_pairs = 3
elif difficulty.startswith("보통"):
    num_pairs = 6
else:
    num_pairs = 8

# --------------------------
# 게임 초기화
# --------------------------
if "cards" not in st.session_state or st.session_state.get("num_pairs") != num_pairs:
    cards = random.sample(emoji_pool, num_pairs) * 2
    random.shuffle(cards)
    st.session_state.cards = cards
    st.session_state.flipped = [False] * len(cards)
    st.session_state.selected = []
    st.session_state.matched = [False] * len(cards)
    st.session_state.num_pairs = num_pairs
    st.session_state.colors = [
        random.choice([
            "linear-gradient(135deg, #f6d365, #fda085)",
            "linear-gradient(135deg, #a1c4fd, #c2e9fb)",
            "linear-gradient(135deg, #d4fc79, #96e6a1)",
            "linear-gradient(135deg, #84fab0, #8fd3f4)",
            "linear-gradient(135deg, #fccb90, #d57eeb)",
            "linear-gradient(135deg, #ff9a9e, #fecfef)",
            "linear-gradient(135deg, #fbc2eb, #a6c1ee)",
            "linear-gradient(135deg, #fad0c4, #ffd1ff)"
        ]) for _ in cards
    ]
    st.session_state.start_time = time.time()
    st.session_state.attempts = 0
    st.session_state.finished = False

# --------------------------
# 카드 클릭 처리
# --------------------------
def flip_card(i):
    if st.session_state.finished:
        return
    if not st.session_state.flipped[i] and len(st.session_state.selected) < 2:
        st.session_state.flipped[i] = True
        st.session_state.selected.append(i)

    if len(st.session_state.selected) == 2:
        st.session_state.attempts += 1
        i1, i2 = st.session_state.selected
        if st.session_state.cards[i1] == st.session_state.cards[i2]:
            st.session_state.matched[i1] = True
            st.session_state.matched[i2] = True
        else:
            st.session_state.flipped[i1] = False
            st.session_state.flipped[i2] = False
        st.session_state.selected = []

# --------------------------
# 카드 그리드 출력
# --------------------------
cols = 4 if num_pairs > 3 else 3
html_grid = f"<div class='grid' style='grid-template-columns: repeat({cols}, 100px);'>"
for i, card in enumerate(st.session_state.cards):
    flipped = st.session_state.flipped[i] or st.session_state.matched[i]
    matched = st.session_state.matched[i]
    bg_color = st.session_state.colors[i] if matched else "linear-gradient(135deg, #ff9a9e, #fad0c4)"

    # onclick 이벤트 → query params로 전달
    html_grid += f"""
    <div class="card-container">
      <div class="card {'flipped' if flipped else ''}" onclick="window.location.href='?flip={i}'">
        <div class="card-face front" style="background:{bg_color};">❓</div>
        <div class="card-face back" style="background:{st.session_state.colors[i]};">{card}</div>
      </div>
    </div>
    """
html_grid += "</div>"

st.markdown(html_grid, unsafe_allow_html=True)

# --------------------------
# 카드 클릭 이벤트
# --------------------------
query_params = st.experimental_get_query_params()
if "flip" in query_params:
    flip_card(int(query_params["flip"][0]))
    st.experimental_set_query_params()  # 클릭 후 URL 초기화

# --------------------------
# 기록 표시
# --------------------------
elapsed = int(time.time() - st.session_state.start_time)
st.info(f"⏱ 경과 시간: {elapsed}초 | 🎯 시도 횟수: {st.session_state.attempts}")

# --------------------------
# 게임 클리어 체크
# --------------------------
if all(st.session_state.matched) and not st.session_state.finished:
    st.session_state.finished = True
    elapsed = int(time.time() - st.session_state.start_time)
    st.balloons()
    st.success(
        f"🎉 축하합니다! {num_pairs}쌍을 모두 맞추셨어요! 🎉\n\n"
        f"⏱ 최종 시간: {elapsed}초\n"
        f"🎯 총 시도 횟수: {st.session_state.attempts}"
    )
    if st.button("🔄 다시 시작하기"):
        for key in ["cards","flipped","selected","matched","colors","num_pairs","start_time","attempts","finished"]:
            del st.session_state[key]


               f"⏱ 최종 시간: {elapsed}초\n🎯 총 시도 횟수: {st.session_state.attempts}")
    if st.button("🔄 다시 시작하기"):
        for key in ["cards","flipped","selected","matched","colors","num_pairs","start_time","attempts","finished"]:
            del st.session_state[key]
