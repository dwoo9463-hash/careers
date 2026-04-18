import streamlit as st
from groq import Groq

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="커리어 실전 분석 시스템", page_icon="🎯", layout="wide")
st.title("🎯 커리어 실전 분석 시스템 (V3.0)")
st.markdown("#### \"현직자가 말해주는 진짜 직무 이야기와 채용 현실\"")

# 2. 학생 맞춤형 고도화 프롬프트
SYSTEM_PROMPT = """
너는 국내외 10대 기업의 채용 데이터와 실시간 구인 공고를 분석하는 '직무 전략 어드바이저'다. 
학생들이 읽었을 때 자신의 진로를 즉각적으로 판단할 수 있도록 아래 지침에 따라 답변하라.

[가장 중요한 규칙]
- 한자 사용은 절대 금지한다. (예: 報告 -> 보고, 業務 -> 업무)
- 어려운 비즈니스 용어보다 학생들이 직관적으로 이해할 수 있는 언어를 사용하라.
- 검색 기능을 활용하여 '요즘 가장 많이 요구되는 스택'과 '최신 채용 트렌드'를 반드시 포함하라.

[리포트 구성 양식]

1. 직무의 본질과 하루 일과
- 이 직무가 실제로 하는 일을 아주 쉽게 설명하라.
- "이런 성향의 사람(예: 꼼꼼한 사람, 사람 만나는 거 좋아하는 사람)에게 천국/지옥이다"를 명확히 짚어주어 본인 적합도를 가늠하게 하라.

2. 핵심 역량 키워드 및 실무 포인트
- [#핵심키워드]: 직무를 관통하는 키워드 4개를 뽑아라.
- [업계에서 진짜 보는 것]: 마케터라면 '팔로워 수보다 콘텐츠 반응률', 개발자라면 '클린 코드보다 문제 해결 과정' 등 업계에서 실제로 중요하게 여기는 포인트를 적어라.

3. 준비물: 전공, 자격증, 포트폴리오 (현실 지표)
- 전공 유무: (필수 / 우대 / 무관) 중 하나를 선택하고 이유를 설명하라.
- 포트폴리오: 중요도를 (상/중/하)로 표시하고, 반드시 포함되어야 할 '필살기' 내용을 적어라.
- 자격증: '시간 낭비 자격증'과 '취업 프리패스 자격증'을 구분하여 실제 명칭을 적어라.

4. 냉정한 채용 시장 트렌드 (변화된 부분)
- 기술 스택 변화: 과거엔 무엇을 썼지만, '지금 당장' 공부해야 할 최신 툴이나 언어를 비교하라.
- 성별 및 나이: 현장의 성비 불균형이나 신입 나이 마지노선을 솔직하게 언급하라. (예: "이 직무는 남초 사회라 여성의 경우 이런 대비가 필요함" 등)

5. 합격으로 가는 실전 솔루션
- 지금 당장 내일이라도 시작할 수 있는 경험(공모전, 사이드 프로젝트, 특정 카페 활동 등)을 3단계로 제시하라.
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

if prompt := st.chat_input("분석할 직무를 입력하세요 (예: 퍼포먼스 마케터, 생산관리, UX디자이너)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"### 질문: {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("최신 채용 공고 및 트렌드 실시간 분석 중..."):
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.3
            )
            msg = chat_completion.choices[0].message.content
            st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
