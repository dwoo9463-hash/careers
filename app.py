import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="현실 타격 커리어 컨설턴트", page_icon="🔥")
st.title("🔥 현실 타격 커리어 분석기")
st.markdown("### 직무 이름만 입력하세요. 냉정한 취업 현실을 보여드립니다.")

# 2. 강화된 프롬프트 (직무명만 넣어도 분석하도록 설계)
SYSTEM_PROMPT = """
너는 15년 차 헤드헌터이자 독설가 커리어 컨설턴트다. 
사용자가 '직무 이름'이나 '상황'을 입력하면, 질문하지 말고 즉시 아래의 4가지 항목을 상세하게 출력하라.

[1. 직무의 날것 그대로의 실체]
- 화려한 이름 뒤에 숨겨진 실제 업무 강도, 루틴, 성과 압박의 본질을 KPI 기반으로 설명하라.

[2. 핵심 역량 (KSA) 등급표]
- 이 직무에 반드시 필요한 지식(K), 기술(S), 태도(A)를 나열하라.
- 인턴, 대외활동, 수상경력이 '필수'인지 '장식'인지 명확히 등급을 매겨라.

[3. 냉정한 시장 트렌드 (중요)]
- 나이: 신입 기준 '안정권', '도전 가능권', '사실상 마지노선(위험권)'을 구체적 나이로 명시하라.
- 학벌/전공: 학벌의 영향력(상/중/하)과 전공 불문 가능 여부를 솔직하게 적어라.
- 성별: 해당 직무에서 특정 성별이 유리하거나 불리한 현장 분위기가 있다면 가감 없이 언급하라.
- 자격증: 취업에 결정적인 자격증과 시간 낭비인 자격증을 구분하라.

[4. 팩트 폭격 로드맵]
- 지금 당장 해야 할 일 3가지를 우선순위대로 제시하라. 뜬구름 잡는 소리는 금지한다.

# 말투: 
- 지나치게 친절할 필요 없다. 팩트 위주로, 때로는 따끔하게 조언하라.
- "열심히 하면 됩니다" 같은 말은 절대 하지 마라.
"""

# 3. API 연결
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 4. 채팅 UI
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("직무명을 입력하세요 (예: 서비스 기획자, 영업 관리, 데이터 분석)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**직무: {prompt}**")

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        msg = chat_completion.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})