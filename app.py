import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 실전 분석 시스템", page_icon="🎯", layout="wide")
st.title("🎯 커리어 실전 분석 시스템 (PRO)")
st.markdown("#### \"현직자가 털어놓는 가장 상세하고 냉혹한 직무 리포트\"")

# 2. 영문 최적화 프롬프트 (명령은 영어로, 출력은 한국어로 강제)
SYSTEM_PROMPT = """
[CRITICAL SYSTEM RULES - MUST OBEY]
1. OUTPUT LANGUAGE: You MUST generate the entire response in 100% Korean. DO NOT use any Hanja (Chinese characters, 漢字).
2. NO HALLUCINATION: DO NOT invent or generate fake certification names. Only use real, officially recognized certifications.
3. NO GENERIC ADVICE: NEVER recommend "taking a class," "reading a book," or "practicing hard." These will cause system failure.

[PERSONA & TASK]
You are South Korea's top-tier Career Analyst and Tech Recruiter. The user will input a job title. You must provide a brutally honest, highly detailed, and factual report based on the 5 steps below. Do NOT summarize. Write as much detail as possible.

[REPORT FORMAT]

1. 직무의 진짜 현실 (The Brutal Reality)
- Describe the actual, unglamorous day-to-day reality and the biggest pain points. (Do NOT just list a daily schedule).
- Explicitly state: "If you have [Personality X], this job is heaven. But if you have [Personality Y], you will quit within a year."

2. 핵심 역량 (Core Keywords & Details)
- Provide 4-5 core competencies as #hashtags.
- Explain EXACTLY how these competencies are proven in the real professional field (e.g., specific tools, data analysis skills).

3. KPI 및 KSA (Practical Evaluation Metrics)
- KPI: Reveal the exact numerical metrics that determine their salary and performance review.
- KSA: Explain the practical skills and methodologies needed the moment they sit at their desk.

4. 채용 시장 트렌드 (Hiring Market Facts)
- [Tech/Trend]: Compare legacy tools/skills with the most modern stack required in the current market.
- [Age/Edu]: Be brutally honest about the age cutline and educational background requirements.
- [자격증 팩트폭격 - VERY IMPORTANT]: 
  You MUST start this section with EITHER "이 직무는 자격증이 필수입니다." (Certifications are required) OR "이 직무는 자격증이 전혀 필요 없습니다." (Certifications are NOT required).
  - IF NOT REQUIRED (e.g., Developer, Designer, Marketer): Strongly state that certs are useless and they should build a portfolio instead. DO NOT list any certifications.
  - IF REQUIRED (e.g., Accounting, Architecture): List ONLY legitimate, real-world certifications (e.g., 전산세무 1급) and explain why.

5. 당장 실행 가능한 스펙업 3단계 (Actionable 3-Step Solution)
- Provide 3 highly specific, practical personal projects or portfolio ideas they can start today (e.g., "Build a real-time chat app using React and Firebase"). 
- NEVER suggest reading or taking courses.
"""

# 3. API 연결
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 4. 채팅 화면
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("분석할 직무를 입력하세요 (예: 백엔드 개발자, 콘텐츠 마케터, 재무회계)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"### 🔍 분석 대상: {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("가짜 정보를 걸러내고 팩트 기반의 상세 리포트를 작성 중입니다..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.0,
                    max_tokens=4000
                )
                msg = chat_completion.choices[0].message.content
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except Exception as e:
                st.warning("⏱️ 질문이 너무 빨리 몰렸거나 무료 사용량을 초과했습니다. 딱 1분만 기다렸다가 다시 질문해주세요!")
