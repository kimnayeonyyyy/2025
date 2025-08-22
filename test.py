import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time

# 초기 설정
POP_SIZE = 10
GENOME_LENGTH = 5
MUTATION_RATE = 0.2
TARGET = np.array([0.5, 0.5, 0.5, 0.5, 0.5])

# 세대 저장용
if "history" not in st.session_state:
    st.session_state.history = []

# 개체 이름 생성
def random_name():
    syllables = ["ka", "zo", "mi", "ra", "lo", "ni", "ta", "se", "vu", "gi"]
    return "".join(random.choice(syllables) for _ in range(3))

# 적합도 계산
def fitness(genome):
    return -np.linalg.norm(genome - TARGET)

# 초기 개체 생성
def create_individual():
    return {
        "genome": np.random.rand(GENOME_LENGTH),
        "name": random_name()
    }

# 다음 세대 생성
def next_generation(population):
    population = sorted(population, key=lambda x: fitness(x["genome"]), reverse=True)
    new_pop = population[:2]  # 상위 2개 복제 (엘리트 선택)
    while len(new_pop) < POP_SIZE:
        p1, p2 = random.sample(population[:5], 2)
        cross = np.array([(g1+g2)/2 for g1, g2 in zip(p1["genome"], p2["genome"])])
        # 돌연변이
        if random.random() < MUTATION_RATE:
            idx = random.randint(0, GENOME_LENGTH - 1)
            cross[idx] = random.random()
        new_pop.append({"genome": cross, "name": random_name()})
    return new_pop

# 세대 시각화
def plot_generation(gen, gen_idx):
    fig, ax = plt.subplots()
    fitnesses = [fitness(ind["genome"]) for ind in gen]
    names = [ind["name"] for ind in gen]
    ax.bar(names, fitnesses)
    ax.set_ylim(-2, 0)
    ax.set_ylabel("적합도 (fitness)")
    ax.set_title(f"{gen_idx}세대")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# UI 시작
st.title("🧬 진화 가상 실험실")

if not st.session_state.history:
    st.session_state.history.append([create_individual() for _ in range(POP_SIZE)])

# 버튼 UI
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ 애니메이션 재생"):
        for i in range(len(st.session_state.history), len(st.session_state.history) + 10):
            next_gen = next_generation(st.session_state.history[-1])
            st.session_state.history.append(next_gen)
            plot_generation(next_gen, i)
            time.sleep(0.5)
        st.stop()

with col2:
    if st.button("⬅ 이전 세대 보기"):
        if len(st.session_state.history) > 1:
            st.session_state.history.pop()
        else:
            st.warning("이전 세대가 없습니다.")

# 마지막 세대 시각화
last_gen = st.session_state.history[-1]
plot_generation(last_gen, len(st.session_state.history) - 1)
