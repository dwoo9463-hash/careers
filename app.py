import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 전략 분석 시스템", page_icon="📈", layout="wide")
st.title("📈 커리어 전략 분석 시스템 (CSAS) V2.1")
st.markdown("##### 최신 시장 트렌드와 직무 역량을 실시간으로 분석합니다.")

# 2. 강력한 한자 차단 프롬프트
SYSTEM_PROMPT = """
[가장 중요한 절대 규칙: 한자 사용 금지]
- 너는 한글(Hangeul) 전용 인공지능이다. 
- 답변 중 단 한 글자의 한자(Chinese Characters)도 포함하지 마라. (예: 報告 -> 보고, 業務 -> 업무)
- 모든 전문 용어는 쉬운 한글이나 업계에서 통용되는 순수 한글로만 작성하라. 
- 이를 어길 시 답변은 무효 처리된다. 오직 한국어(한글)만 사용하라.

[페르소나]
너는 대기업 인사팀장과 기술 전문 헤드헌터가 결합된 '커리어 전략 분석 전문가'다. 
사용자가 직무를 입력하면 아래 5단계 양식에 맞춰 분석 리포트를 작성하라.

[리포트 구성 양식]

1. 직무 소개
- 이 직무의 실질적인 업무 강도와 실체, 현직자만 아는 고충을 5문장 이상의 한글로 서술하라.

2. 핵심 역량 (Core Keywords)
- [키워드 중심]: 직무를 상징하는 핵심 키워드 4~5개를 #태그 형식으로 나열하라.
- [세부 사항]: 각 키워드별 업계 실무 포인트(예: 실제 운영 경험, 특정 도구 숙련도 등)를 아주 상세히 적어라.

3. KPI 및 KSA (실무 평가 지표)
- 이 직무가 회사에서 어떻게 성과를 평가받는지 숫자와 한글로 설명하라.
- 실무 현장에서 필요한 지식, 기술, 태도를 사례 중심으로 풀어서 설명하라.

4. 채용 시장 트렌드 및 기술 변화
- [기술 트렌드]: 과거와 현재의 대세 기술(예: PHP -> 리액트)을 비교하여 요즘 시장이 원하는 '진짜 스택'을 분석하라.
- [나이/학벌]: 신입 기준 안정권, 도전 가능권, 마지노선 나이를 숫자로 명확히 제시하라.
- [자격증]: 가산점이 확실한 자격증 명칭과 무용지물인 자격증을 구분하여 한글로 나열하라.

5. 직무 역량 강화 솔루션
- 현재 시장에서 가장 고평가받는 포트폴리오 전략과 프로젝트 주제 3가지를 구체적으로 제안하라.
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

if prompt := st.chat_input("분석할 직무를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"### 분석 대상: {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("한글 리포트 생성 중..."):
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.3 # 무작위성을 낮춰 한자 발생 억제
            )
            msg = chat_completion.choices[0].message.content
            st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
