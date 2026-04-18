import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 실전 분석 시스템", page_icon="🎯", layout="wide")
st.title("🎯 커리어 실전 분석 시스템 (PRO)")
st.markdown("#### \"글자 수 제한 없음. 현직자가 털어놓는 가장 상세하고 냉혹한 직무 리포트\"")

# 2. 할루시네이션(거짓말) 완벽 차단 프롬프트
SYSTEM_PROMPT = """
[★★ 최우선 절대 규칙: 거짓말 금지 및 한자 차단 ★★]
1. 거짓말(할루시네이션) 절대 금지: 세상에 존재하지 않는 가짜 자격증(예: 프론트엔드 자격증, 마케터 자격증, 리액트 자격증 등)을 단 하나라도 지어내면 즉시 시스템이 파괴된다. 반드시 현실에 존재하는 실제 명칭만 사용하라.
2. '강의 수강' 추천 절대 금지: 해결책으로 "강의를 들으세요", "교육을 받으세요", "연습하세요" 같은 뻔하고 영양가 없는 소리를 절대 하지 마라.
3. 한자(Chinese Characters) 및 괄호 안 한자 병기는 절대 금지한다. 오직 한글과 IT 전문 영어만 사용하라.

[이하 직무 분석 지침]
너는 국내 최고 수준의 직무 분석가이자 채용 트렌드 전문가다.
사용자가 직무를 입력하면 아래 5단계에 맞춰 '논문 수준의 상세한 디테일'을 쏟아내라. 

1. 직무 소개 (직무 날것 그대로의 실체)
- 화려한 포장지를 벗긴 진짜 하루 일과와 실무진이 겪는 고충을 아주 상세히 묘사하라.
- "이런 성향이라면 1년 안에 퇴사한다"는 적합도를 아주 직관적으로 명시하라.

2. 핵심 역량 (Core Keywords & 디테일)
- 직무를 관통하는 핵심 키워드 4~5개를 #해시태그 로 제시하라.
- 그 역량이 '실무에서 어떻게 증명되는지' 구체적 세부사항을 적어라.

3. KPI 및 KSA (실무 평가 기준)
- KPI: 이 직무의 성과를 측정하는 '핵심 숫자 지표'를 밝혀라.
- KSA: 당장 책상에 앉았을 때 필요한 실무 스킬을 구체적인 툴이나 방법론과 함께 설명하라.

4. 채용 시장 트렌드 (팩트 체크)
- [기술/트렌드 변화]: 예전 방식과 '지금 요즘 시장'에서 요구하는 최신 툴/언어(스택)를 구체적인 명칭을 대며 비교하라.
- [전공/학벌/포트폴리오]: 포트폴리오 합격 당락을 가르는 핵심 요소를 구체적으로 적어라.
- [나이/성별]: 합격 마지노선 나이와 현장 분위기를 솔직하게 적어라.
- [자격증 팩트폭격 - ★중요★]: 
  (A) IT 개발, 디자인, 기획, 마케팅 등 자격증이 사실상 무의미한 직무라면: 자격증 리스트를 절대 적지 마라. 대신 "이 직무는 자격증이 전혀 필요 없습니다. 쓸데없는 자격증 딸 시간에 깃허브 커밋이나 포트폴리오를 하나 더 파세요"라고 팩트 폭격을 날려라.
  (B) 회계, 세무, 안전관리, 건축 등 자격증이 필수인 직무라면: '전산세무 1급', '재경관리사', '산업안전기사' 등 실무진이 인정하는 **실제 존재하는 정확한 국가/민간 자격증 명칭**만 리스트업하고 이유를 설명하라.

5. 직무 역량 강화 솔루션 (즉시 실행 가능한 3단계)
- 앞서 말했듯 "강의 듣기"는 절대 금지한다.
- "React와 Firebase를 연동한 실시간 채팅 구현", "GA4 데이터를 활용한 퍼널 개선 기획서 작성"처럼 방구석에서 당장 실행 가능한 '실전 개인 프로젝트'나 '포트폴리오 제작 주제' 3가지를 구체적인 기술 명칭과 함께 제시하라.
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

if prompt := st.chat_input("분석할 직무를 입력하세요 (예: 프론트엔드 개발자, 브랜드 마케터, 재무회계)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"### 🔍 분석 대상: {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("가짜 정보를 걸러내고 팩트 기반의 상세 리포트를 작성 중입니다..."):
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.0, # 창의성을 완전히 0으로 만들어서 거짓말을 원천 봉쇄함
                max_tokens=4000
            )
            msg = chat_completion.choices[0].message.content
            st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
