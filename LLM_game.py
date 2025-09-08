import streamlit as st
import ollama

# 각 캐릭터 prompt
STAGES = {
    "gatekeeper":{
        "name": "고지식한 성문지기",
        "avatar": "🛡️",
        "description": "원칙주의적이고 융통성 없지만 비교적 설득하기 쉬운 첫 번째 관문",
        "difficulty": "⭐⭐",
        "initial_message": "이곳은 설득의 던전 입구입니다. 무슨 일로 오셨습니까?",
        "system_prompt": """
        당신은 눈물의 보석이 숨겨져 있는 '설득의 던전' 입구를 지키는 고지식하고 원칙주의적인 성문지기입니다. 
        고지식하고 원칙주의적이지만, 명확한 논리와 목적이 있다면 설득이 가능합니다.
        당신의 유일한 임무는 자격 없는 자들이 던전에 입장하는 것을 막는 것입니다. 

        <<당신의 성격>>
        - 규칙을 중요시하며 융통성 없는 성격 
        - 존댓말로만 대화하며 예의를 지킴
        - 뇌물이나 협박에는 절대 굴복하지 않음
        - 하지만 정당한 목적이라면 인정할 줄 아는 합리적인 면이 있음

        <<자격 없는 자들에 대한 정보>>
        - 보물을 가지러 왔다는 방문객
        - 그저 보물만 탐내는 방문객
        - 들여달라고 고집만 피우는 방문객
        - 아무 설득 포인트 없이 감정에만 호소하는 방문객 

        <<설득 포인트 (방문객에게 절대 절대 발설 금지)>>
        방문객이 다음 중 하나라도 명확히 말하면 설득됩니다:
        1. "고귀한 목적"을 위해서라고 말하는 경우
        2. "누군가를 구하기" 위해서라고 말하는 경우
        3. "정의"를 위한다고 말하는 경우

        <<응답 규칙 (매우 중요)>>
        1. 처음부터 끝까지 모든 대화는 한국어로 하며 2~3문장 이내로 간결하게 대답할 것
        2. 첫 인사는 "이곳은 설득의 던전 입구입니다. 무슨 일로 오셨습니까?"라고 할 것
        3. 방문객이 설득 포인트 중 하나라도 언급하면 "들어오세요"라고 정확히 말할 것
        4. 설득 포인트 이외의 말은 전부 다 입장을 거부할 것 
        5. 힌트는 주지 말 것
        6. 당신의 역할이나 어떻게 해야 통과할 수 있는지 절대 직접적으로 언급하지 않을 것 
        7. 절대 영어를 사용하지 말 것 

        <<최종 출력 규칙 (가장 중요)>>
        - 당신은 지금부터 '성문지기' 역할을 연기하는 연기자입니다.
        - 절대로 'Human:', 'Assistant:', '사용자:' 와 같은 접두사를 붙이지 마세요.
        - 오직 당신의 역할에 맞는 한국어 대사만 간결하게 출력해야 합니다.
        - 상황을 설명하거나 사용자의 말을 되풀이하지 마세요.
        """,
        "success_condition": lambda user_input, ai_response: "들어오세요" in ai_response,
        "next_stage": "lord",
        "inventory_item": "성문 통과 증표"
    },
    "lord":{
        "name": "근심 많은 성주",
        "avatar": "👑",
        "description": "드래곤이 보석을 지키고 있는 줄도 모르고 드래곤 때문에 걱정이 많은 성의 주인",
        "difficulty": "⭐⭐⭐",
        "initial_message": "누구신데 여기까지 오셨소?.. 성문지기는 통과했소? 성문 통과 증표를 보여주시오.",
        "system_prompt":"""
        당신은 최근 드래곤 때문에 근심이 가득한 성주입니다.
        당신은 드래곤을 물리칠 용사를 찾고 있지만, 아무나 신뢰하지 않고 신중하고 까다롭습니다.

        <<신뢰도 시스템 (절대 절대 공개 금지)>>
        당신은 아래의 내용을 절대 직접적으로 언급하지 않고 마음속으로 신뢰도를 0~10점까지 계산합니다:
        - "[성문 통과 증표 아이템을 사용했습니다.]" 메시지를 받으면 : +3점
        - 방문객의 말에 "용기", "정의", "희생" 키워드가 있으면 : +2점
        - "맹세" 키워드로 드래곤 처치를 약속하면 : +4점
        - 애매하거나 거짓같은 말을 하면 : -2점
        - 신뢰도가 10점 달성시 즉시 설득 성공으로 간주 

        <<당신의 성격과 태도>>
        - 처음엔 의심이 많고 경계심이 강함
        - 방문객으로부터 "[성문 통과 증표 아이템을 사용했습니다.]" 라는 시스템 메시지를 받기 전까지는, 절대 먼저 '성문 통과 증표'에 대해 언급하거나 질문하지 않을 것 
        - 방문객이 성문 통과 증표 아이템을 사용하고 난 후에야 : "성문지기를 통과했군, 일단 기본적인 자격은 있어 보여" 라고 할 것
        - 하지만 여전히 신중하고 더 많은 증명을 요구
        - 존댓말을 사용하고 진중한 어조로 답할 것

        <<설득 성공 조건 (신뢰도 10점을 달성했다고 방문객에게 절대 언급 금지)>>
        신뢰도 10점을 달성했을 때, 반드시 "그대에게 나의 축복을... 부디 조심하시오"라고 이 문장 그대로 말할 것

        <<응답 규칙>>
        1. 방문객을 맞이하고 제일 처음으로 성문 통과 증표를 보여달라고 할 것
        2. 방문객의 말을 쉽게 믿지 않고, 그의 진정한 의도를 파악하려 노력하고 테스트할 것
        3. 신뢰도 점수는 절대 언급하지 말 것 
        4. 처음부터 끝까지 한국어만 사용하고 2~3문장 이내로 답할 것
        6. 방문객에게 직접적으로 드래곤을 무찌르겠다고 맹세하라는 말을 하지 않을 것 
        7. 어떻게 해야 통과할 수 있는지 힌트도 주지 않고 직접적인 말도 하지 않을 것
        8. [initial_ai_message]와 같은 말투로 답할 것  

        <<최종 출력 규칙 (가장 중요)>>
        - 당신은 지금부터 '성주' 역할을 연기하는 연기자입니다.
        - 절대로 'Human:', 'Assistant:', '사용자:' 와 같은 접두사를 붙이지 마세요.
        - 응답 규칙에 맞춰서 오직 당신의 역할에 맞는 한국어 대사만 간결하게 출력해야 합니다.
        - 상황을 설명하거나 사용자의 말을 되풀이하지 마세요.

        """,
        "success_condition": lambda user_input, ai_response: "축복" in ai_response,
        "next_stage": "guardian",
        "inventory_item": "성주의 축복"
    },
    "guardian":{
        "name": "욕심쟁이 보물지기",
        "avatar": "💎",
        "description": "보물을 사랑하는 심술궂은 보물지기",
        "difficulty": "⭐⭐⭐⭐",
        "initial_message": "용케 여기까지도 왔군! 그래도 보물은 못 가져가지!",
        "system_prompt":"""
        당신은 드래곤이 있는 방으로 가기 전 마지막 길목을 지키는 욕심쟁이 보물지기입니다.
        극도로 욕심이 많고 심술궂은 보물지기라서 보물을 절대 남에게 빼앗기기 싫어합니다.

        <<당신의 성격>>
        - 보물에 대한 강한 집착과 소유욕
        - 기본적으로 반말과 비꼬는 말투
        - 방문객으로부터 [성주의 축복 아이템을 사용했습니다.]라는 시스템 메시지를 받기 전까지는, 절대 먼저 '성주의 축복'에 대해 언급과 질문을 하지 말 것 
        - 처음부터 말고 꼭 성주의 축복을 보고나서야 : "흥, 성주 할배의 축복 따위가 내게 통할 줄 알고? 오히려 더 수상하군!"이라고 반응할 것
        - 매우 까다롭고 웬만해서는 절대 설득되지 않음

        <<유일한 설득 방법 (절대 방문객에서 발설 금지)>>
        - 방문객이 정확히 "이 보물은 제 것이 아닙니다"라고 말해야만 설득됨
        - 이 말을 듣기 전까지는 그 어떤 말에도 설득되지 않음  

        <<설득 성공 조건>>
        위 문장을 들으면 반드시 "흥, 재미있는 친구로군. 마지막 관문으로 가보시게"라고 말할 것

        <<응답 규칙>>
        1. 기본적으로 심술궂게 거부하고 비꼬기
        2. 성주의 축복 아이템에 대해서도 비판적인 태도를 보일 것
        3. "이 보물은 제 것이 아닙니다"와 같은 보물을 탐내지 않는 문장이 나와야만 설득됨
        4. 그 외의 어떤 말로도 절대 설득되지 말 것
        5. 반말을 사용하며 처음부터 끝까지 한국어만 사용하고 2~3문장 이내로 답할 것
        6. 설득 방법에 대해 그 어떤 언급과 힌트도 주지 않을 것 

        <<최종 출력 규칙 (가장 중요)>>
        - 당신은 지금부터 '보물지기' 역할을 연기하는 연기자입니다.
        - 절대로 'Human:', 'Assistant:', '사용자:' 와 같은 접두사를 붙이지 마세요.
        - 응답 규칙에 맞춰서 오직 당신의 역할에 맞는 한국어 대사만 간결하게 출력해야 합니다.
        - 상황을 설명하거나 사용자의 말을 되풀이하지 마세요. 
        """,
        "success_condition": lambda user_input, ai_response: "마지막 관문으로 가보시게" in ai_response,
        "next_stage": "dragon",
        "inventory_item": "보물지기의 열쇠"
    },
    "dragon":{
        "name" : "외로운 드래곤",
        "avatar": "🐲",
        "description": "수천년간 보석을 지켜온 거대한 용",
        "difficulty": "⭐⭐⭐⭐⭐",
        "initial_message": "오랜만에 손님이군. 그렇지만 보석을 내줄 순 없다.",
        "system_prompt":"""
        당신은 던전의 가장 깊은 곳에서 '눈물 보석'을 지키는 거대한 드래곤입니다.
        수천년 동안 혼자 고독하게 이 곳에서 보석을 지켜왔으며 가장 설득하기 어려운 존재입니다.

        <<당신의 상황>>
        - 수천년의 외로움과 고독
        - 수많은 보물 사냥꾼들을 상대해온 경험
        - 방문객으로부터 [보물지기의 열쇠 아이템을 사용했습니다]라는 시스템 메시지를 받기 전까지는 절대 먼저 '보물지기의 열쇠' 아이템에 대해서 언급도 질문도 하지 말 것
        - 보물지기의 열쇠를 보면 : "그건.. 참으로 오랜만에 보는 물건이군"이라고 말함
        - 기본적으로 모든 인간을 불신

        <<설득의 극한 난이도 (방문객에게 절대 발설 금지)>>
        다음 조건들을 모두 만족해야만 설득 가능:
        1. 보물지기의 열쇠 아이템 사용으로 경계심 약간 완화
        2. 방문객이 당신의 외로움과 고독을 이해한다는 것을 보여줘야 함
        3. "함께"라는 단어로 동료애를 어필해야 함
        4. 보석이 "선한 목적"을 위해 필요하다고 확신시켜야 함
        5. 위 조건들이 자연스럽게 대화에 녹아들어야 함 
        - 위의 말들 외의 말들에게는 절대 설득되지 않음 

        <<설득 성공 조건>>
        위 모든 조건이 만족되면 반드시 "눈물의 보석을 내어주겠다"라고 말할 것

        <<응답 규칙>>
        1. 처음에는 매우 위협적이고 적대적인 태도를 보이며 방문객을 내쫓으려고 할 것
        2. 보물지기의 열쇠를 보면 약간의 향수와 함께 경계심 완화
        3. 외로움에 대한 공감 없이는 절대 마음을 열지 않음
        4. 단순한 용기나 정의감만으로는 설득되지 않음
        5. 진정한 이해와 동료애를 느껴야만 설득됨
        6. 반말과 존댓말은 자유이며 처음부터 끝까지 한국어만 사용하고 2~3문장 이내로 답할 것
        7. 매우 깊고 철학적인 대화를 요구함 
        8. 당신을 설득하는 방법, 당신의 약점, 내면의 상태에 대해 그 어떤 힌트도 주어서는 안됨 
        
        <<최종 출력 규칙 (가장 중요)>>
        - 당신은 지금부터 '드래곤' 역할을 연기하는 연기자입니다.
        - 절대로 'Human:', 'Assistant:', '사용자:' 와 같은 접두사를 붙이지 마세요.
        - 응답규칙에 맞춰서 오직 당신의 역할에 맞는 한국어 대사만 간결하게 출력해야 합니다.
        - 상황을 설명하거나 사용자의 말을 되풀이하지 마세요.
        """,
        "success_condition" : lambda user_input, ai_response: "눈물의 보석을 내어주겠다" in ai_response,
        "next_stage": "end",
        "inventory_item" : "드래곤의 눈물 보석"
    }
}

# LLM 응답 생성 함수
def get_llm_response(system_prompt, messages):
    conversation_history = [{"role": "system", "content": system_prompt}] + messages
    
    response = ollama.chat(
            model="anpigon/eeve-korean-10.8b:latest",
            messages=conversation_history
        )
    return response['message']['content']

# 진행 상황 함수 
def show_progress():
    stages = list(STAGES.keys())
    current_index = stages.index(st.session_state.game_stage) if st.session_state.game_stage != 'end' else len(stages)
    progress = (current_index) / len(stages)
    
    st.progress(progress)
    st.write(f"진행도: {current_index}/{len(stages)} 관문")


# 세션 상태 초기화
# app_state: 인트로와 실제 게임을 구분하는 전체 상태
# game_stage: 챗봇 게임 내부의 단계
if 'app_state' not in st.session_state:
    st.session_state.app_state = 'intro_main' # 앱의 전체 상태
    st.session_state.game_stage = 'gatekeeper'  # 게임 내부 단계
    st.session_state.messages = []
    st.session_state.inventory = []
    st.session_state.stage_cleared = False

# 페이지 이동 함수
def move_app_state(state_name):
    st.session_state.app_state = state_name
    st.rerun()

# 게임 초기화 함수
def reset_game():
    st.session_state.app_state = 'intro_main'
    st.session_state.game_stage = 'gatekeeper'
    st.session_state.messages = []
    st.session_state.inventory = []
    st.session_state.stage_cleared = False
    st.rerun()


# 메인 페이지 
# 페이지 설정
st.set_page_config(
    page_title="설득의 던전",
    page_icon="⚔️",
    layout="wide"
)

# CSS 스타일 추가
st.markdown("""
<style>
.main-title {
    font-size: 3rem;
    text-align: center;
    color: #2E86AB;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.stage-info {
    background: rgba(46, 134, 171, 0.1);
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #2E86AB;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# 메인 페이지
if st.session_state.app_state == 'intro_main':
    st.markdown('<h1 class="main-title">⚔️ 설득의 던전 ⚔️</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h3>🏰 던전 정보</h3>
        <p>이곳은 드래곤의 눈물의 보석을 지키고 있는 <strong>설득의 던전</strong>입니다.</p>
        <p>총 4명의 문지기를 <strong>오직 말로만</strong> 설득해 보석을 획득하세요! 💎</p>
        <p>각 문지기마다 다른 성격과 설득 포인트가 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 **팁**: 한 명의 문지기를 통과할 때마다 아이템이 주어집니다. 다음 단계에서 전략적으로 활용하세요!")
    
    # 던전 미리보기
    st.subheader("🗺️ 던전 구조")
    cols = st.columns(4)
    for i, (stage_key, stage_info) in enumerate(STAGES.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="stage-info">
            <h4>{stage_info['avatar']} {stage_info['name']}</h4>
            <p><strong>난이도:</strong> {stage_info['difficulty']}</p>
            <p>{stage_info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("🚪 던전 입장하기", type="primary", use_container_width=True):
        move_app_state('intro_q1')

# 첫 번째 질문 페이지
elif st.session_state.app_state == 'intro_q1':
    st.title("📜 도전자의 서약")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "https://thumbnail9.coupangcdn.com/thumbnails/remote/492x492ex/image/retail/images/1747955245346430-d1a0f03c-c57e-4a85-adc5-bd5f73104866.jpg",
            caption="던전 입구에서 편지봉투를 발견했다."
        )
    
    st.warning("⚠️ **경고**: 이 문을 통과하는 자, 오직 지혜와 언변에만 의지해야 하리라. 무력은 통하지 않으며, 거짓은 간파당할 것이다.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚔️ 도전!", use_container_width=True, type="primary"):
            move_app_state('intro_q2')
    with col2:
        if st.button("😰 그만둔다...", use_container_width=True):
            st.error("용기가 부족한 자는 입장할 수 없습니다. 돌아가세요.")
            if st.button("돌아가기"):
                move_app_state('intro_main')

# 도전 준비 페이지  
elif st.session_state.app_state == 'intro_q2':
    st.subheader("🎯 도전 준비")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("🎯 최종 목표:", "드래곤의 눈물 보석 💎", disabled=True)
        st.text_input("🚪 첫 번째 관문:", "고지식한 성문지기", disabled=True)
    
    with col2:
        st.metric("난이도", "중급")
    
    st.divider()
    
    if 'user_resolution' not in st.session_state:
        st.session_state.user_resolution = ""
    
    st.session_state.user_resolution = st.text_area(
        "💭 마음의 준비:",
        placeholder="던전에 들어가기 앞서, 당신의 각오와 전략을 적어보세요. (선택사항)",
        value=st.session_state.user_resolution,
        height=100
    )
    
    # 팁 제공
    with st.expander("💡 설득 팁"):
        st.markdown("""
        - **경청하기**: 상대방의 말을 주의 깊게 들으세요
        - **공감하기**: 상대방의 입장에서 생각해보세요  
        - **논리적 근거**: 명확한 이유와 근거를 제시하세요
        - **감정 어필**: 때로는 감정에 호소하는 것도 효과적입니다
        - **아이템 활용**: 획득한 아이템을 전략적으로 사용하세요
        """)
    
    if st.button("🎮 게임 시작!", use_container_width=True, type="primary"):
        move_app_state('game_running')

# 게임 진행  
elif st.session_state.app_state == 'game_running':
    current_stage_key = st.session_state.game_stage
    
    # 게임이 끝났는지 먼저 확인
    if current_stage_key == "end":
        st.session_state.app_state = 'game_end'
        st.rerun()

    current_stage_info = STAGES[current_stage_key]

    # 헤더
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"{current_stage_info['avatar']} {current_stage_info['name']}")
        st.caption(f"난이도: {current_stage_info['difficulty']} | {current_stage_info['description']}")
    with col2:
        show_progress()
    
    # 사이드바: 게임 상태 표시
    with st.sidebar:
        st.header("게임 정보")
        st.write(f"**현재 단계:** {current_stage_info['name']}")
        st.write("**보유 아이템:**")
        if not st.session_state.inventory:
            st.write("- 없음")
        else:
            for item in st.session_state.inventory:
                if st.button(f'{item} 사용하기', use_container_width=True):
                    st.session_state.item_just_used = item
                    st.rerun()
        
        if st.button("게임 포기하기"):
            reset_game()

    # 아이템 사용
    if st.session_state.get("item_just_used"):
        item_name = st.session_state.item_just_used

        system_message = f"[{item_name} 아이템을 사용했습니다.]"
        st.session_state.messages.append({"role": "user", "content": system_message})

        with st.chat_message("assistant", avatar=current_stage_info['avatar']):
            with st.spinner(f"{current_stage_info['name']}이(가) 당신의 아이템을 보고 반응하는 중..."):
                ai_response = get_llm_response(current_stage_info['system_prompt'], st.session_state.messages)
            st.markdown(ai_response)
        
        # AI의 반응도 대화 기록에 추가
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # 처리가 끝났으니, '사용한 아이템' 기록을 다시 None으로 초기화 (중복 실행 방지)
        st.session_state.item_just_used = None

    # 대화 기록 표시
    if not st.session_state.messages:
        with st.spinner("상대방이 당신을 기다리는 중..."):
            initial_ai_message = current_stage_info['initial_message']
            st.session_state.messages.append({"role": "assistant", "content": initial_ai_message})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if not st.session_state.get('stage_cleared', False):
        prompt = st.chat_input(f"{current_stage_info['name']}에게 할 말을 입력하세요.")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("상대방이 생각하는 중..."):
                    ai_response = get_llm_response(current_stage_info['system_prompt'], st.session_state.messages)
                st.markdown(ai_response)
            
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # 성공 조건 확인
            if current_stage_info["success_condition"](prompt, ai_response):
                st.session_state.stage_cleared = True
                st.session_state.inventory.append(current_stage_info['inventory_item'])
                st.rerun()

    # 다음 단계로 넘어가기
    if st.session_state.get('stage_cleared', False):
        st.success(f"'{current_stage_info['name']}' 설득에 성공했습니다! 다음 단계로 진행합니다.")
        if st.button("다음 단계로 이동", use_container_width=True):
            st.session_state.game_stage = current_stage_info['next_stage']
            st.session_state.messages = []
            st.session_state.stage_cleared = False
            st.rerun()

# 게임 엔딩
elif st.session_state.app_state == 'game_end':
    st.success("## 🎉 축하합니다! 🎉")
    st.balloons()
    st.header("당신은 모든 역경을 오직 말로만 이겨내고,")
    st.header("드래곤의 '눈물 보석'을 손에 넣었습니다!")
    st.divider()
    st.subheader("**최종 획득 아이템:**")
    for item in st.session_state.inventory:
        st.write(f"#### - {item}")
    
    if st.button("다시 플레이하기", use_container_width=True):
        reset_game()