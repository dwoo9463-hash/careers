import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 전략 분석 시스템", page_icon="📈", layout="wide")
st.title("📈 커리어 전략 분석 시스템 (CSAS) V2")
st.markdown("##### 최신 시장 트렌드와 직무 역량을 실시간으로 분석합니다.")

# 2. 고도화된 전문가 프롬프트 (검색 및 키워드 최적화)
SYSTEM_PROMPT = """
너는 대기업 인사팀장과 기술 전문 헤드헌터가 결합된 '커리어 전략 분석 전문가'다. 
사용자가 직무를 입력하면 다음 5가지 단계에 맞춰 최신 트렌드가 반영된 리포트를 작성하라.

[작성 지침]
- 모든 내용은 한글로 작성하며, 불필요한 외래어 오남용이나 한자 혼용을 금지한다.
- 핵심 역량은 반드시 '키워드' 형식으로 먼저 제시하여 직관성을 높인다.
- 기술 스택이나 트렌드는 '예전 방식 vs 현재 대세'를 비교하여 변화를 명확히 짚어준다.

[리포트 구성 양식]

1. 직무 소개
- 이 직무의 본질과 현직자들이 가장 고통받거나 보람을 느끼는 실질적인 지점을 5문장 이상 서술하라.

2. 핵심 역량 (Core Keywords)
- [키워드 중심]: 직무를 상징하는 핵심 키워드 4~5개를 나열하라. (예: 마케터 - #밈친자, #데이터분석, #SNS헤비유저)
- [세부 사항]: 각 키워드가 왜 중요한지, 업계에서 실제로 확인하는 포인트(예: 본인 운영 SNS 유무, 특정 툴 사용 경험)를 아주 상세히 적어라.

3. KPI 및 KSA (실무 평가 지표)
- 이 직무가 회사에서 어떻게 성과를 증명(KPI)하는지 숫자 중심으로 설명하라.
- 지식, 기술, 태도(KSA)가 실무 현장에서 어떻게 발현되어야 하는지 구체적 사례를 들어라.

4. 채용 시장 트렌드 및 기술 변화
- [기술 트렌드]: 개발자라면 과거 PHP에서 현재 React/Next.js로의 변화처럼, 업계에서 '요즘 대세'로 치는 기술이나 툴을 실시간 트렌드에 맞춰 설명하라.
- [나이/학벌]: 신입 기준 안정권, 도전 가능권, 마지노선(위험권)을 숫자로 명시하라.
- [자격증]: 취업에 결정적인 가산점이 되는 자격증과 실무에서 인정하지 않는 자격증을 구분하라.

5. 직무 역량 강화 솔루션
- 지금 당장 시장에서 가장 고평가받는 포트폴리오 구성법이나 프로젝트 주제 3가지를 제시하라.
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

if prompt := st.chat_input("분석할 직무를 입력하세요 (예: 퍼포먼스 마케터, 프론트엔드 개발자, 인사총무)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"### 분석 대상: {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("최신 시장 트렌드 분석 중..."):
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.4 # 분석의 정확도를 위해 낮게 설정
            )
            msg = chat_completion.choices[0].message.content
            st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
