요구하신 대로 정보를 뭉뚱그려 줄글로 쓰지 않고, **표(Table)**와 항목별 리스트를 활용하여 한눈에 들어오도록 구조화했습니다. 특히 핵심 역량 부분은 단순 키워드 나열이 아니라 실무 데이터를 기반으로 한 **'진짜 실력'**이 무엇인지 파악하도록 지침을 강화했습니다.

아래 코드로 app.py를 업데이트해 보세요.

🔥 시각적 가독성 및 팩트 강화 버전 app.py
Python
import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 실전 분석 시스템", page_icon="🎯", layout="wide")
st.title("🎯 커리어 실전 분석 시스템 (V5.0)")
st.markdown("#### \"한눈에 보는 직무별 채용 지표와 실무 핵심 역량 리포트\"")

# 2. 영문 최적화 지시문 (시각적 구조화 및 팩트 체크 강화)
SYSTEM_PROMPT = """
[CRITICAL SYSTEM RULES]
1. OUTPUT FORMAT: NEVER write in long paragraphs. Use Markdown TABLES, BOLD LISTS, and DIVIDERS for clarity.
2. NO HANJA: Do not use any Chinese characters (漢字). Use 100% Korean and essential English tech terms.
3. FACTUALITY: Do not hallucinate. If a certification doesn't exist or isn't required, state it clearly.
4. NO COURSES/BOOKS: Do not suggest taking classes or reading books.

[REPORT STRUCTURE]

1. 직무의 본질과 현실 (Reality Check)
- Describe the core mission and the "hell points" for workers.
- Define "Person who succeeds" vs "Person who fails."

2. 실전 핵심 역량 (Core Competency Deep-Dive)
- Use a detailed list or table.
- For each competency, explain: 
  A) The "Keyword" 
  B) Why it's needed in the field 
  C) Specific "Real-world Proof" (e.g., "Must be able to use Figma variables," "Experience in processing 1,000+ data rows per day").

3. 성과 평가 지표 (KPI)
- List the exact numbers or metrics that determine the worker's value (e.g., Conversion Rate, Error Rate, Budget Management).

4. 채용 시장 데이터 (Categorized Demographics)
- Use a Table or Bold List for the following:
  - [나이/경력]: Entry-level age range and the "Danger Zone" age.
  - [학벌/전공]: Requirement level (Must-have / Preferred / Irrelevant) and preferred majors.
  - [성별 선호도]: Honest field atmosphere (Male-dominated / Female-dominated / Neutral).
  - [자격증 유무]: 
    - First, state: "필수 아님" (Not Required) or "필수임" (Required).
    - If Required: List ONLY 3+ REAL, EXISTING certifications. 
    - If Not Required: Explain why personal projects are more important.

5. 실무자급 포트폴리오 솔루션
- Provide 3 specific project topics that show senior-level thinking (e.g., "Build an automated inventory system using Python," "Propose a UX improvement plan for an e-commerce checkout flow").
"""

# 3. API 연결
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 4. 채팅 화면 구성
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("분석할 직무를 입력하세요 (예: 퍼포먼스 마케터, 생산관리, 재무회계)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"### 🔍 분석 대상: {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("최신 채용 데이터와 실무 트렌드를 분석하여 구조화된 리포트를 생성 중입니다..."):
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
                st.warning("⏱️ 요청이 너무 많습니다. 1~2분만 기다렸다가 다시 시도해 주세요!")
