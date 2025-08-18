# app.py
import streamlit as st

st.set_page_config(page_title="🌈 MBTI 진로 추천기", page_icon="🎯", layout="centered")

st.markdown("<h1 style='text-align: center; color: pink;'>🌸 MBTI 진로 추천기 🌸</h1>", unsafe_allow_html=True)
st.write("✨ 당신의 MBTI를 선택하고, 강점/약점/추천 진로를 카드 형식으로 확인해보세요! ✨")

# -------------------------
# MBTI 16유형 데이터 + 색상 팔레트
# -------------------------
mbti_info = {
    "INTJ 🦉": {
        "strengths": ["🔮 전략적 사고", "📊 논리적 분석", "🧭 미래 비전"],
        "weaknesses": ["😶 감정 표현 어려움", "🙃 완벽주의", "🌀 융통성 부족"],
        "careers": ["📊 데이터 사이언티스트", "🧠 전략 컨설턴트", "🛠️ 시스템 설계자"],
        "colors": ["#6c5ce7", "#a29bfe", "#341f97"]  # 보라 계열
    },
    "INTP 🐉": {
        "strengths": ["🧪 분석력", "💡 독창적 사고", "📚 지적 호기심"],
        "weaknesses": ["🌀 우유부단", "😅 실행력 부족", "🙃 사회성 부족"],
        "careers": ["👨‍💻 연구원", "💻 프로그래머", "🧠 철학자"],
        "colors": ["#00cec9", "#81ecec", "#0984e3"]  # 청록/블루
    },
    "ENTJ 🦁": {
        "strengths": ["⚡ 추진력", "📈 리더십", "🧭 조직 능력"],
        "weaknesses": ["😤 독단적", "🌀 성급함", "🙃 타인 무시"],
        "careers": ["🏢 CEO", "📊 경영 컨설턴트", "⚖️ 변호사"],
        "colors": ["#d63031", "#ff7675", "#e17055"]  # 레드/오렌지
    },
    "ENTP 🦊": {
        "strengths": ["💡 창의성", "🎤 유머 감각", "⚡ 에너지"],
        "weaknesses": ["🌀 마무리 부족", "⏰ 꾸준함 부족", "📦 산만함"],
        "careers": ["🎤 크리에이터", "📢 마케터", "💡 아이디어 기획자"],
        "colors": ["#00cec9", "#74b9ff", "#55efc4"]  # 청록/하늘
    },
    "INFJ 🕊️": {
        "strengths": ["💖 공감능력", "🌱 이상주의", "🧩 깊은 통찰"],
        "weaknesses": ["😓 과도한 자기희생", "🌀 현실 도피", "🙃 고집"],
        "careers": ["📚 작가", "👩‍⚕️ 심리상담가", "🌍 NGO 활동가"],
        "colors": ["#6c5ce7", "#a29bfe", "#b2bec3"]  # 퍼플/그레이
    },
    "INFP 🦋": {
        "strengths": ["🌸 따뜻한 마음", "🎨 창의력", "🌈 이상주의"],
        "weaknesses": ["🌀 비현실적", "😅 우유부단", "🙃 자기비판"],
        "careers": ["🎨 예술가", "📖 작가", "👩‍⚕️ 상담가"],
        "colors": ["#55efc4", "#00cec9", "#81ecec"]  # 민트 계열
    },
    "ENFJ 🌞": {
        "strengths": ["🌟 카리스마", "💖 타인 배려", "🤝 협력 능력"],
        "weaknesses": ["😅 과도한 책임감", "🌀 갈등 회피", "🙃 과도한 이상주의"],
        "careers": ["📢 강연가", "👩‍🏫 교사", "🌍 리더십 코치"],
        "colors": ["#e84393", "#fd79a8", "#fab1a0"]  # 핑크/코랄
    },
    "ENFP 🐬": {
        "strengths": ["🎉 활발함", "💡 창의적 아이디어", "🌈 긍정 에너지"],
        "weaknesses": ["📦 루틴 싫음", "🌀 집중력 부족", "😅 스코프 확장"],
        "careers": ["🎭 배우/예술가", "📢 브랜드 마케터", "✨ 창의적 기획자"],
        "colors": ["#fdcb6e", "#ffeaa7", "#fab1a0"]  # 노랑/오렌지
    },
    "ISTJ 🦌": {
        "strengths": ["📋 책임감", "🧩 꼼꼼함", "⚖️ 원칙주의"],
        "weaknesses": ["🌀 융통성 부족", "🙃 변화 싫어함", "😅 고집"],
        "careers": ["👮 경찰", "📊 회계사", "⚙️ 관리자"],
        "colors": ["#2d3436", "#636e72", "#b2bec3"]  # 그레이 계열
    },
    "ISFJ 🐰": {
        "strengths": ["💖 헌신적", "🌸 따뜻함", "🧩 꼼꼼함"],
        "weaknesses": ["😓 자기희생", "🙃 갈등 회피", "🌀 스트레스"],
        "careers": ["👩‍⚕️ 간호사", "📚 교사", "🏠 사회복지사"],
        "colors": ["#ffb6b9", "#fae3d9", "#fcd5ce"]  # 파스텔 핑크
    },
    "ESTJ 🦅": {
        "strengths": ["⚡ 추진력", "📊 조직능력", "🧭 실용성"],
        "weaknesses": ["🙃 고집", "🌀 융통성 부족", "😤 독단적"],
        "careers": ["🏢 관리자", "⚖️ 변호사", "📊 경영자"],
        "colors": ["#e17055", "#d35400", "#e67e22"]  # 오렌지 계열
    },
    "ESFJ 🦋": {
        "strengths": ["🤝 친절함", "🌸 협동심", "💖 배려심"],
        "weaknesses": ["🌀 타인 의존", "🙃 갈등 회피", "😅 과민함"],
        "careers": ["👩‍⚕️ 간호사", "📚 교사", "👩‍🍳 서비스업"],
        "colors": ["#fab1a0", "#ff7675", "#e84393"]  # 핑크/레드
    },
    "ISTP 🐺": {
        "strengths": ["⚙️ 실용적", "🛠️ 문제 해결", "⚡ 위기 대응"],
        "weaknesses": ["🙃 충동적", "🌀 감정 표현 부족", "😅 무계획"],
        "careers": ["🔧 엔지니어", "🚗 정비사", "🏍️ 모험가"],
        "colors": ["#636e72", "#2d3436", "#74b9ff"]  # 다크+블루
    },
    "ISFP 🦢": {
        "strengths": ["🎨 예술적 감각", "🌸 따뜻한 마음", "🧘 평화로움"],
        "weaknesses": ["🌀 소극적", "🙃 갈등 회피", "😅 우유부단"],
        "careers": ["🎨 아티스트", "👩‍🍳 요리사", "🌱 환경 운동가"],
        "colors": ["#fab1a0", "#ffeaa7", "#55efc4"]  # 파스텔 믹스
    },
    "ESTP 🐯": {
        "strengths": ["⚡ 모험심", "🎉 사교성", "🛠️ 실용적"],
        "weaknesses": ["🌀 충동적", "🙃 인내 부족", "😅 즉흥적"],
        "careers": ["💼 세일즈", "🎬 배우", "🚀 기업가"],
        "colors": ["#0984e3", "#74b9ff", "#00cec9"]  # 비비드 블루
    },
    "ESFP 🐼": {
        "strengths": ["🎉 활발함", "🌈 낙천적", "🎭 예술적 감각"],
        "weaknesses": ["🌀 충동적", "🙃 깊이 부족", "😅 책임 회피"],
        "careers": ["🎤 연예인", "🎭 배우", "📢 이벤트 플래너"],
        "colors": ["#fd79a8", "#fab1a0", "#ffeaa7"]  # 핑크/옐로우
    },
}

# -------------------------
# 카드 함수
# -------------------------
def card(title, items, color):
    html = f"""
    <div style="
        background-color:{color};
        border-radius:15px;
        padding:15px;
        margin:10px 0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    ">
        <h4 style="color:white; text-align:center;">{title}</h4>
        <ul style="color:white; font-size:16px; list-style:none;">
            {''.join([f"<li>{i}</li>" for i in items])}
        </ul>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# -------------------------
# 선택 & 출력
# -------------------------
mbti = st.selectbox("🌈 MBTI를 선택하세요:", list(mbti_info.keys()))

if mbti:
    info = mbti_info[mbti]
    colors = info["colors"]

    st.markdown(f"<h2 style='text-align: center; color: violet;'>✨ {mbti} 추천 분석 ✨</h2>", unsafe_allow_html=True)

    card("🌟 강점 (Strengths)", info["strengths"], colors[0])
    card("⚠️ 약점 (Weaknesses)", info["weaknesses"], colors[1])
    card("💼 추천 진로 (Careers)", info["careers"], colors[2])

    st.markdown("<h3 style='text-align: center; color: pink;'>🌸 오늘도 당신의 가능성을 응원해요! 🌸</h3>", unsafe_allow_html=True)

