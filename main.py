# app.py
import streamlit as st

st.set_page_config(page_title="🌈 MBTI 진로 추천기", page_icon="🎯", layout="centered")

st.markdown("<h1 style='text-align: center;'>🌸 MBTI 진로 추천기 🌸</h1>", unsafe_allow_html=True)
st.write("✨ 당신의 MBTI를 선택하고, 어울리는 진로를 확인해보세요! ✨")

# MBTI 16유형 + 추천 직업 (귀여운 이모지 포함)
mbti_careers = {
    "INTJ 🦉": ["🔮 전략 컨설턴트", "📊 데이터 사이언티스트", "🧭 프로젝트 매니저"],
    "INTP 🐍": ["🔬 연구원", "💻 알고리즘 엔지니어", "🧪 발명가"],
    "ENTJ 🦁": ["🏢 CEO/리더", "📈 경영 전략가", "🚀 스타트업 창업자"],
    "ENTP 🦊": ["💡 아이디어 기획자", "🎤 크리에이터", "📢 마케터"],
    "INFJ 🦄": ["📚 교육자", "💬 상담가", "🌱 사회혁신가"],
    "INFP 🐱": ["✍️ 작가", "🎨 디자이너", "💌 콘텐츠 기획자"],
    "ENFJ 🦋": ["🤝 HR/리더", "🎤 강사/코치", "🌍 NGO 활동가"],
    "ENFP 🐬": ["🎭 배우/예술가", "📢 브랜드 마케터", "✨ 창의적 기획자"],
    "ISTJ 🐢": ["📊 회계사", "🛠️ 품질관리자", "📑 행정 공무원"],
    "ISFJ 🐰": ["👩‍⚕️ 간호사", "📚 교사", "🏠 사회복지사"],
    "ESTJ 🐯": ["📦 운영 매니저", "📈 세일즈 리더", "🏭 생산관리자"],
    "ESFJ 🐼": ["👩‍💼 HR 담당자", "🤝 커뮤니티 매니저", "🎉 이벤트 플래너"],
    "ISTP 🐍": ["🔧 엔지니어", "🕹️ 게임 개발자", "🔍 보안 전문가"],
    "ISFP 🐹": ["🎨 그래픽 디자이너", "📸 사진작가", "🌸 플로리스트"],
    "ESTP 🐯": ["🎤 세일즈 전문가", "⚡ 퍼포먼스 마케터", "🎪 이벤트 매니저"],
    "ESFP 🐥": ["🎤 연예인/배우", "🎉 이벤트 플래너", "🛍️ 쇼핑 호스트"],
}

mbti = st.selectbox("🌈 MBTI를 선택하세요:", list(mbti_careers.keys()))

if mbti:
    st.markdown(f"<h2 style='text-align: center;'>✨ {mbti} 추천 진로 ✨</h2>", unsafe_allow_html=True)
    st.write("💖 어울리는 직업 리스트에요! 💖")
    for job in mbti_careers[mbti]:
        st.markdown(f"- {job}")
    st.markdown("---")
    st.markdown("🌟 즐겁게 진로 탐색하세요! 🌟")

