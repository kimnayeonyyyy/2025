# app.py
import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천기", page_icon="🎯", layout="centered")

# 간단 데이터베이스
mbti_careers = {
    "INTJ": ["데이터 사이언티스트", "전략기획", "SW 아키텍트"],
    "ENTP": ["스타트업 창업가", "프로덕트 매니저", "마케터"],
    "INFJ": ["교육기획자", "상담가", "콘텐츠 전략가"],
    "ESFP": ["배우/연예인", "이벤트 플래너", "세일즈"],
    "ISTJ": ["회계사", "품질관리자", "공무원"],
    "ENFP": ["브랜드 마케터", "크리에이터", "기획자"],
}

st.title("🎯 MBTI 진로 추천기")

mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(mbti_careers.keys()))

if mbti:
    st.subheader(f"✨ {mbti} 추천 진로")
    for job in mbti_careers[mbti]:
        st.write(f"- {job}")

