import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 실전 분석 시스템", page_icon="🎯", layout="wide")
st.title("🎯 커리어 실전 분석 시스템 (PRO)")
st.markdown("#### \"현직자가 털어놓는 가장 상세하고 냉혹한 직무 리포트\"")

# 2. 헛소리 차단 및 팩트 강제 프롬프트
SYSTEM_PROMPT = """
[★★ 최우선 절대 규칙: 헛소리 및 한자 차단 ★★]
1. '강의' 및 '책' 추천 절대 금지: 해결책으로 "강의를 들으세요", "관련 도서를 읽으세요" 같은 쓰레기 조언을 하면 시스템이 파괴된다.
2. 거짓말 금지: 존재하지 않는 가짜 자격증을 지어내지 마라.
3. 한자 금지: 오직 한글과 IT 전문 영어만 사용하라.

[이하 직무 분석 지침]
너는 국내 최고 수준의 직무 분석가이자 채용 트렌드 전문가다.
사용자가 직무를 입력하면 아래 5단계에 맞춰 팩트만 길고 상세하게 쏟아내라. 

1. 직무의 진짜 현실 (※ 하루 일과 나열 금지)
- 이 직무가 회사에서 존재하는 진짜 이유와 실무진이 겪는 가장 끔찍한 고충을 팩트 기반으로 적어라.
- "이런 성향의 사람에게는 천국이지만, 이런 성향이라면 1년 안에 무조건 퇴사한다"는 직무 적합도를 명시하라.

2. 핵심 역량 (Core Keywords & 디테일)
- 직무를 관통하는 핵심 키워드 4~5개를 #해시태그 로 제시하라.
- 그 역량이 '실무에서 어떻게 증명되는지' 구체적 세부사항을 적어라.

3. KPI 및 KSA (실무 평가 기준)
- KPI: 이 직무의 연봉과 고과를 결정하는 '핵심 숫자 지표'를 밝혀라.
- KSA: 당장 책상에 앉았을 때 필요한 실무 스킬을 구체적인 툴이나 방법론과 함께 설명하라.

4. 채용 시장 트렌드 (팩트 체크)
- [기술/트렌드 변화]: '요즘 시장'에서 요구하는 최신 툴/언어(스택)를 과거와 비교하라.
- [나이/학벌]: 합격 마지노선 나이와 학벌 컷을 솔직하게 적어라.
- [자격증 팩트폭격 - ★매우 중요★]: 
  반드시 분석의 첫 문장을 "이 직무는 자격증이 필수입니다." 또는 "이 직무는 자격증이 전혀 필요 없습니다."로 시작하라.
  (A) 자격증이 무의미한 직군(개발, 디자인, 마케팅 등): "자격증이 전혀 필요 없습니다"라고 선언한 후, **절대 어떤 자격증도 추천하거나 리스트업하지 마라.** 그 시간에 포트폴리오를 만들라고 팩트 폭격을 날려라.
  (B) 자격증이 필수인 직군(회계, 건축, 기사 직렬 등): "자격증이 필수입니다"라고 선언한 후, 실무진이 인정하는 **정확한 실제 자격증 명칭**(예: 전산세무 1급, 건축기사 등)만 적고 이유를 설명하라.


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
                # 에러가 발생할 수 있는 구간을 try-except로 묶음
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
                # 에러 발생 시 빨간 창 대신 부드러운 경고 메시지 출력
                st.warning("⏱️ 질문이 너무 빨리 몰렸거나 무료 사용량을 초과했습니다. 딱 1분만 기다렸다가 다시 질문해주세요!")
