import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="진화 가상 실험실", layout="wide")
st.title("🧬 진화 가상 실험실 - 버튼 탐색 버전")

# 환경 설정
temp = st.sidebar.slider("🌡️ 온도", 0, 100, 50)
food = st.sidebar.slider("🥗 먹이", 0, 100, 50)
predator = st.sidebar.slider("🦁 포식자", 0, 100, 50)
gens = st.sidebar.slider("세대 수", 1, 30, 10)

# 초기 세팅
if "gen" not in st.session_state:
    N = 30
    st.session_state.gen = 0
    st.session_state.history = []
    init_pop = np.random.rand(N, 3) * 100
    init_names = [f"Indiv_{i+1}" for i in range(N)]
    st.session_state.history.append((init_pop, init_names))

def fitness(ind):
    fur, size, agi = ind
    return -(abs(fur - temp) + abs(size - (30 if food < 50 else 70)) + abs(agi - (100 - predator)))

def evolve_step(pop, names):
    N = len(pop)
    scores = np.array([fitness(ind) for ind in pop])
    idx = np.argsort(scores)[-N//2:]
    surv, surv_names = pop[idx], [names[i] for i in idx]
    kids, kid_names = [], []
    while len(kids) < N:
        p1, p2 = random.sample(list(surv), 2)
        cut = random.randint(0, 2)
        c = np.array([*p1[:cut], *p2[cut:]])
        if random.random() < 0.3: c += np.random.normal(0, 10, 3)
        kids.append(np.clip(c, 0, 100))
        kid_names.append(random.choice(surv_names) + "_child")
    return np.array(kids), kid_names

# 버튼 영역
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ 이전 세대로") and st.session_state.gen > 0:
        st.session_state.gen -= 1
with col2:
    if st.button("➡️ 다음 세대로") and st.session_state.gen < gens:
        # 아직 계산 안 된 세대라면 새로 진화시켜 history에 추가
        if st.session_state.gen == len(st.session_state.history) - 1:
            pop, names = st.session_state.history[-1]
            new_pop, new_names = evolve_step(pop, names)
            st.session_state.history.append((new_pop, new_names))
        st.session_state.gen += 1

# 현재 세대 시각화
pop, nms = st.session_state.history[st.session_state.gen]
fig, ax = plt.subplots()
sc = ax.scatter(pop[:,0], pop[:,1], c=pop[:,2], cmap="viridis", s=80)
for i, nm in enumerate(nms): ax.text(pop[i,0]+1, pop[i,1]+1, nm, fontsize=6)
ax.set_title(f"{st.session_state.gen} 세대 (색=민첩성)")
plt.colorbar(sc, ax=ax, label="민첩성")
st.pyplot(fig)

# 상태 표시
st.info(f"현재 세대: {st.session_state.gen} / 최대 {gens}")
if st.session_state.gen == gens:
    st.success("✅ 모든 세대 진화 완료!")


- 먹이({food}) 상황에 따라 체구 크기 변화  
- 포식자 압력({predator})이 높으면 민첩성이 발달  
""")

