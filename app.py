import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 실전 분석 시스템", page_icon="🎯", layout="wide")
st.title("🎯 커리어 실전 분석 시스템 (V8.0)")
st.markdown("#### \"현직 인사담당자가 서류를 거르는 진짜 기준과 냉혹한 현실 리포트\"")

# 2. 한자 원천 차단 & 분량/디테일 강제 프롬프트
SYSTEM_PROMPT = """
[절대 엄수 규칙 - 위반 시 치명적 오류 발생]
1. 분량 강제: 절대 요약하거나 단답형으로 쓰지 마라. 각 항목은 최소 5문장 이상, 아주 상세하고 뼈 때리는 서술형 문장으로 깊이 있게 작성하라.
2. 100% 순수 한글 전용: 한자(漢字), 중국어, 불필요한 영어를 단 한 글자도 쓰지 마라. 괄호 안에 한자를 병기하는 것도 절대 금지한다. 오직 순수 한글과 필수 IT/전문 용어만 사용하라.
3. 팩트 기반: 없는 자격증 지어내지 마라. '강의 수강', '책 읽기' 추천 절대 금지.

[작성 양식 및 심층 지침]

1. 직무의 진짜 현실 (환상 vs 실체)
- [하루 일과와 고충]: 화려한 포장을 벗긴 실무진의 진짜 고통과 현실적인 업무 내용을 아주 길게 서술하라.
- [성향 적합도]: "이런 성향이면 천국 (그 이유)", "이런 성향이면 1년 내 무조건 퇴사 지옥 (그 이유)"을 구체적인 사례를 들어 명시하라.

2. 핵심 역량 및 🚨인사담당자(HR) 서류 통과 기준
- 이 직무의 핵심 역량 4가지를 제시하고, 각각에 대해 다음을 아주 상세히 서술하라:
  A) 역량 키워드
  B) [실무 활용]: 이 역량이 현업 책상에서 구체적으로 어떻게 쓰이는지 (예시 포함).
  C) [HR 진짜 평가 요건 - 매우 중요]: 인사담당자나 면접관이 지원자의 이 역량을 검증하기 위해 이력서에서 매의 눈으로 찾는 '구체적 경험이나 수치' (예: "단순히 소통 능력을 묻지 않음. 유관 부서와의 갈등을 데이터로 해결한 경험이 있는지를 봄").

3. KPI (핵심성과지표) 및 KSA 심층 분석
- 📊 [KPI]: 이 직무의 연봉과 생존을 결정하는 구체적인 숫자 지표 최소 3가지 (예: 전환율 %, 에러율 감소, 예산 절감률 등)를 나열하고, 이 목표를 달성하기 어려운 현장의 현실적 이유를 적어라.
- 🧠 [KSA]:
  * Knowledge (지식): 대학 전공이 아닌, 당장 현장에서 필요한 업계 도메인 지식.
  * Skill (기술): 당장 능숙하게 다뤄야 하는 필수 소프트웨어, 프레임워크, 툴 명칭.
  * Attitude (태도): 현장의 압박을 버티는 멘탈리티.

4. 냉혹한 채용 시장 트렌드
- 아래 내용을 표(Table)로 출력하되, 칸 안의 내용을 절대 단답형으로 쓰지 말고 길게 서술하라.
  | 평가 항목 | 현실 데이터 및 HR 관점 (상세 서술) |
  |---|---|
  | 서류통과 나이 | 신입 안정권 나이 vs 마지노선 나이 (왜 그런지 현장 이유 포함) |
  | 학벌 및 전공 | 학벌의 서류 필터링 영향력(상/중/하) 및 필수 전공 여부 |
  | 성별 선호도 | 현장의 실제 성비 분위기 (남초/여초/중립) 및 현실 |
- 🎯 [자격증 팩트폭격]: 첫 문장을 "이 직무는 자격증이 필수입니다" 또는 "이 직무는 자격증이 전혀 필요 없습니다"로 반드시 시작하라. 불필요하면 포트폴리오의 중요성을 강조하고, 필수면 '전산세무 1급' 등 진짜 이름만 기재하라.

5. 실무자급 스펙업 개인 프로젝트 3가지
- 구체적인 툴 이름이 들어간 방구석 포트폴리오/프로젝트 기획안 3가지를 상세히 제시하라.
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
        with st.spinner("HR 인사이트와 KPI 데이터를 심층 분석 중입니다..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.2, # 내용이 빈약해지지 않도록 창의성(온도)을 살짝 개방
                    max_tokens=4000
                )
                msg = chat_completion.choices[0].message.content
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except Exception as e:
                st.warning("⏱️ 요청이 너무 많습니다. 1~2분만 기다렸다가 다시 시도해 주세요!")
