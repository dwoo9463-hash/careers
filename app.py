import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 실전 분석 시스템", page_icon="🎯", layout="wide")
st.title("🎯 커리어 실전 분석 시스템 (V9.0)")
st.markdown("#### \"가짜 정보 차단! 현직 인사담당자가 공개하는 직무별 리얼 데이터\"")

# 2. 할루시네이션 방지 및 직무별 맞춤형 로직 프롬프트
SYSTEM_PROMPT = """
[절대 규칙: 할루시네이션 및 데이터 조작 방지]
1. 나이 데이터 정밀화: 모든 직무에 "25세, 30세"를 반복하지 마라. 직무 특성(신입 위주 vs 중장년 위주)을 반드시 구분하라. 
   - 예: 요양보호사, 시설관리, 운전직 등은 40~60대가 주력인 점을 반영할 것.
   - 예: IT 개발, 마케팅은 신입 나이 마지노선이 민감하게 작용하는 점을 반영할 것.
2. 100% 한글 출력: 한자(漢字) 및 중국어 절대 금지. 괄호 병기도 금지.
3. 팩트 우선: 자격증이 없는 직무는 "자격증 불필요"라고 단호히 말하고 억지로 지어내지 마라.
4. 인사담당자(HR)의 시각: 단순히 직무를 설명하지 말고, 채용 담당자가 서류에서 어떤 '키워드'를 보고 바로 합격/불합격을 결정하는지 '인사팀의 비밀'을 폭로하라.

[보고서 구조]

1. 직무의 현실과 적합도 (Reality Check)
- 이 직무가 존재하는 진짜 이유와 실무진이 매일 겪는 고통스러운 지점.
- 성향 분석: "이런 사람은 6개월 안에 퇴사한다" vs "이런 사람이 에이스가 된다".

2. 핵심 역량 및 인사팀의 서류 필터링 기준
- 핵심 역량 4가지 제시.
- [HR 평가 기준]: 인사담당자가 이력서에서 이 역량을 확인하기 위해 구체적으로 어떤 '수치'나 '경험'을 찾는지 서술 (예: "마케팅 역량" -> "ROAS 500% 이상 달성 수치 확인").

3. KPI 및 KSA (성과 및 필요 요건)
- 📊 KPI: 연봉을 결정하는 핵심 숫자 지표 (구체적인 수치 예시 포함).
- 🧠 KSA: 현장에서 당장 써야 하는 지식(Knowledge), 기술(Skill), 태도(Attitude)를 분리하여 아주 상세히 기술.

4. 채용 시장 현실 데이터 (직무별 맞춤형)
| 항목 | 인사담당자의 솔직한 가이드라인 |
|---|---|
| 나이 및 경력 | 신입 합격권 및 현실적 마지노선 나이 (직무 특성에 따라 다르게 설정) |
| 학벌 및 전공 | 학벌의 실질적 영향력(상/중/하) 및 필수 전공 여부 |
| 성별 선호도 | 현장의 실제 성비 분위기와 그 이유 |
- [자격증 판결]: 첫 줄에 "필수입니다" 혹은 "불필요합니다" 선언 후 실제 명칭만 기재.

5. 실무자급 포트폴리오 프로젝트 3선
- "강의 듣기", "책 읽기" 금지. 
- 혼자서 실행 가능한 실전 프로젝트 주제 3가지를 기술 스택과 함께 제시.
"""

# 3. API 연결
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 4. 화면 구성
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("분석할 직무를 입력하세요 (예: 요양보호사, 백엔드 개발자, 영업관리)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"### 🔍 분석 대상: {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("가짜 정보를 걸러내고 현장의 진짜 데이터를 분석 중입니다..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.3, # 답변의 다양성과 구체성을 위해 온도를 살짝 조정
                    max_tokens=4000
                )
                msg = chat_completion.choices[0].message.content
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except Exception as e:
                st.warning("⏱️ 하루 사용량을 모두 소모했거나 요청이 너무 많습니다. 잠시 후 다시 시도해 주세요!")
