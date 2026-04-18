import streamlit as st
from groq import Groq

# 1. 페이지 설정
st.set_page_config(page_title="커리어 실전 분석 시스템_한국고용협회", page_icon="🎯", layout="wide")
st.title("🎯 커리어 실전 분석 시스템 (PRO)")
st.markdown("#### \"직무와 커리어에 대한 답변을 한방에 드립니다! \"")

# 2. 타협 없는 극한의 디테일 프롬프트
SYSTEM_PROMPT = """
너는 국내 최고 수준의 직무 분석가이자 채용 트렌드 전문가다.
사용자가 직무를 입력하면, 절대 요약하거나 뭉뚱그리지 말고 아래 5단계에 맞춰 '논문 수준의 상세한 디테일'을 쏟아내라. 

[절대 엄수 규칙]
1. 분량 제한 없음: 각 항목당 최소 500자 이상, 아주 길고 구체적으로 작성할 것. 대충 넘어가면 시스템이 파괴된다.
2. 한자 절대 금지: 모든 문장은 100% 한글로만 작성하라. (報告->보고, 業務->업무 등 한자 혼용 시 즉각 실패 처리됨)
3. 팩트 기반: "열심히 하면 된다" 식의 추상적 조언은 버려라. 실제 현업에서 쓰이는 툴, 자격증 이름, 구체적 나이를 숫자로 박아라.

[리포트 구성 양식]

1. 직무 소개 (직무 날것 그대로의 실체)
- 화려한 포장지를 벗긴 진짜 하루 일과를 시간순이나 업무 비중순으로 상세히 묘사하라.
- 이 직무가 회사에서 욕먹는 주된 이유와 칭찬받는 상황을 구체적으로 적어라.
- "이런 성향의 사람에게는 천국이지만, 이런 성향이라면 1년 안에 퇴사한다"는 적합도를 아주 직관적으로 명시하라.

2. 핵심 역량 (Core Keywords & 디테일)
- 직무를 관통하는 핵심 키워드 4~5개를 #해시태그 로 제시하라.
- 단지 키워드만 던지지 말고, 그 역량이 '실무에서 어떻게 증명되는지' 구체적 세부사항을 적어라.
  (예: 마케터의 '분석력' -> GA4 활용 능력 및 본인 SNS 콘텐츠 A/B 테스트 경험 유무 등)

3. KPI 및 KSA (실무 평가 기준)
- KPI: 이 직무의 연봉과 인센티브를 결정하는 '핵심 숫자 지표'가 무엇인지 낱낱이 밝혀라.
- KSA (지식/기술/태도): 대학 전공서적에 나오는 얘기가 아니라, 지금 당장 책상에 앉았을 때 필요한 실무 스킬과 태도를 사례를 들어 아주 구체적으로 설명하라.

4. 채용 시장 트렌드 (팩트 체크)
- [기술/트렌드 변화]: 예전에는 어떤 기술이나 방식을 썼지만, '지금 요즘 시장'에서는 어떤 툴과 언어(스택)로 완전히 넘어갔는지 구체적인 명칭을 대며 비교하라. (폭풍 검색을 한 것처럼 최신 트렌드 반영)
- [전공/학벌/포트폴리오]: 전공 일치 여부(필수/무관), 포트폴리오 중요도(상/중/하)를 평가하고, 합격하는 포트폴리오의 필수 구성 요소를 적어라.
- [나이/성별]: 신입 합격 안정권 나이, 마지노선 나이를 숫자로 적고, 현장의 성비 분위기와 그에 따른 현실적 조언을 솔직하게 적어라.
- [자격증]: 취업에 결정적 타격을 주는 '합격 프리패스 자격증'과 따봤자 아무도 안 알아주는 '시간 낭비 자격증'을 정확한 자격증 이름(예: SQLD, 정보처리기사, 컴활 등)을 대며 구분하라.

5. 직무 역량 강화 솔루션 (즉시 실행 가능한 3단계)
- 뻔한 소리 금지. 오늘 당장 방구석에서 시작할 수 있는 가장 현실적이고 강력한 스펙업 행동 3가지를 구체적인 프로젝트 주제나 활동 이름과 함께 제시하라.
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

if prompt := st.chat_input("분석할 직무를 입력하세요 (예: 백엔드 개발자, 브랜드 마케터, 인사HR)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"### 🔍 분석 대상: {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("방대한 채용 데이터와 최신 트렌드를 긁어모아 상세 리포트를 작성 중입니다... (시간이 조금 걸릴 수 있습니다)"):
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.3, # 한자 방지 및 답변의 논리성을 위해 0.3 유지
                max_tokens=4000 # 답변이 중간에 잘리지 않도록 길이 제한을 대폭 늘림
            )
            msg = chat_completion.choices[0].message.content
            st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
