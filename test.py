import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="진화 가상 실험실", layout="wide")

st.title("🧬 진화 가상 실험실")
st.write("환경 조건에 따라 개체들이 세대를 거듭하며 적응하는 모습을 관찰할 수 있습니다!")

# -------------------
# 환경 조건 선택
# -------------------
st.sidebar.header("🌍 환경 조건 설정")
temp = st.sidebar.slider("🌡️ 환경 온도 (저온=0 ~ 고온=100)", 0, 100, 50)
food = st.sidebar.slider("🥗 먹이 풍부함 (적음=0 ~ 많음=100)", 0, 100, 50)
predator = st.sidebar.slider("🦁 포식자 압력 (낮음=0 ~ 높음=100)", 0, 100, 50)

# -------------------
# 개체 초기화
# -------------------
num_individuals = 50
num_generations = st.sidebar.slider("세대 수", 1, 50, 20)

# 개체 특성: [털 두께, 체구 크기, 민첩성]
population = np.random.rand(num_individuals, 3) * 100

def fitness(ind):
    """적합도 함수: 환경 조건과 개체 특성의 잘 맞는 정도 계산"""
    fur, size, agility = ind
    score = 0

    # 온도 → 털 두께 중요
    score -= abs(fur - temp)

    # 먹이 부족 → 작은 체구 유리
    if food < 50:
        score -= abs(size - 30)
    else:
        score -= abs(size - 70)

    # 포식자 많을수록 민첩성 중요
    score -= abs(agility - (100 - predator))

    return -score  # 높은 점수일수록 적합

def evolve(population, generations=10):
    """세대를 거듭하며 진화"""
    for _ in range(generations):
        # 적합도 계산
        fitness_scores = np.array([fitness(ind) for ind in population])

        # 상위 절반 선택
        survivors = population[np.argsort(fitness_scores)][-len(population)//2:]

        # 다음 세대 생성 (교배 + 변이)
        children = []
        while len(children) < len(population):
            parents = random.sample(list(survivors), 2)
            child = (parents[0] + parents[1]) / 2
            child += np.random.normal(0, 5, size=3)  # 변이
            children.append(child)
        population = np.array(children)

    return population

# -------------------
# 진화 실행
# -------------------
final_population = evolve(population, num_generations)

# -------------------
# 결과 시각화
# -------------------
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(final_population[:,0], final_population[:,1],
           c=final_population[:,2], cmap="viridis", s=80, alpha=0.8)

ax.set_xlabel("털 두께")
ax.set_ylabel("체구 크기")
ax.set_title("최종 세대 개체 분포 (색=민첩성)")
st.pyplot(fig)

st.subheader("📊 해석")
st.write(f"""
- 환경 온도({temp})에 맞춰 털 두께가 조정됨  
- 먹이({food}) 상황에 따라 체구 크기 변화  
- 포식자 압력({predator})이 높으면 민첩성이 발달  
""")

