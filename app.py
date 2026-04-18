import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 실전 분석 시스템", page_icon="🎯", layout="wide")
st.title("🎯 커리어 실전 분석 시스템 (V7.0)")
st.markdown("#### \"인사담당자의 필터링 기준과 실무 KPI를 파헤치는 냉혹한 직무 리포트\"")

# 2. 영문 최적화 지시문 (한글 강제, HR 시점, KPI/KSA 심층 분석)
SYSTEM_PROMPT = """
[CRITICAL SYSTEM RULES]
1. OUTPUT FORMAT: Use Markdown TABLES, BOLD LISTS, and DIVIDERS. Do NOT over-summarize. Write deeply and extensively.
2. 100% KOREAN LANGUAGE: You MUST translate ALL headings, subheadings, and content into Korean. ABSOLUTELY NO Hanja (Chinese characters, 漢字). Minimize English unless it is an industry-standard technical tool/term.
3. FACTUALITY & NO COURSES: Do not hallucinate. Never suggest taking classes or reading books.

[REPORT STRUCTURE]

1. 직무의 진짜 현실과 성향 적합도
- [직무의 실체]: 화려한 포장을 벗긴 진짜 하루 일과와 실무진이 겪는 가장 고통스러운 점을 서술하라.
- [성향 적합도]: "이런 성향이면 천국", "이런 성향이면 1년 안에 퇴사 지옥"이라는 명확한 기준을 제시하라.

2. 실전 핵심 역량 및 🚨인사담당자(HR)의 서류 필터링 기준
- 4~5가지 핵심 역량을 나열하라. 각 역량마다 다음 3가지를 반드시 포함하라:
  A) 핵심 키워드
  B) [실무 활용]: 현업에서 이 역량이 구체적으로 어떻게 쓰이는지.
  C) [HR 진짜 평가 요건]: 인사담당자와 면접관이 지원자의 이 역량을 검증하기 위해 이력서나 포트폴리오에서 '실제로 확인하는 지표나 경험' (예: "단순히 소통을 잘한다고 쓰면 탈락시킴. 갈등을 데이터로 해결한 구체적 사례를 찾음").

3. KPI 및 KSA 심층 분석 (매우 상세하게 작성할 것)
- 📊 [KPI (핵심성과지표)]: 이 직무가 연봉 협상과 인사고과에서 평가받는 '정확한 숫자 지표'들(예: 전환율, 에러율, 원가절감률 등)을 구체적으로 나열하고, 이를 달성하기 어려운 현실적 이유를 적어라.
- 🧠 [KSA (지식/기술/태도) 분해]:
  * Knowledge (지식): 전공 서적이 아닌, 현장에서 당장 알아야 할 실무/업계 도메인 지식.
  * Skill (기술): 당장 능숙하게 다뤄야 하는 필수 소프트웨어, 툴, 프로그래밍 언어.
  * Attitude (태도): 현장의 압박과 스트레스를 견디기 위해 필요한 멘탈리티.

4. 냉혹한 채용 시장 트렌드 데이터
- 표(Table)를 사용하여 다음을 한눈에 보기 쉽게 정리하라:
  * [나이]: 신입 서류 합격 안정권 나이 vs 마지노선(위험권) 나이.
  * [학벌/전공 중요도]: 학벌이 서류 통과에 미치는 영향력(상/중/하) 및 그 이유. 전공 일치 필수 여부.
  * [성별 선호도]: 현장의 실제 성비 분위기 (남초/여초/중립).
- [자격증 팩트폭격]:
  * 분석의 첫 문장을 무조건 "이 직무는 자격증이 필수입니다" 또는 "이 직무는 자격증이 전혀 필요 없습니다"로 시작하라.
  * 필수면 실제 존재하는 정확한 국가/민간 자격증 명칭을 나열. 아니면 "이력서 칸 채우기용 자격증 딸 시간에 딴 거 해라"고 팩트 폭격.

5. 당장 실행 가능한 실무자급 스펙업 3단계
- "강의 듣기" 절대 금지. 
- 혼자서 당장 만들 수 있는 고퀄리티 개인 프로젝트나 포트폴리오 기획안 3가지를 구체적인 툴 이름과 함께 제시하라.
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
        with st.spinner("HR 평가 기준과 KPI/KSA 데이터를 심층 분석 중입니다..."):
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
