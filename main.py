import streamlit as st
import logging
import re

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/streamlit_app.log'
)

logger = logging.getLogger('streamlit_app')

st.set_page_config(layout="wide")

# Load external CSS
with open('assets/css/style.css', encoding='utf-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def init_components():
    """필요한 컴포넌트들을 초기화하고 세션 상태에 저장
    초기화되는 컴포넌트:
    - Intent Analyzer: 상담 대화에서 인텐트, 감정, 키워드 등을 분석
    - DB Manager: 데이터베이스 연결 및 쿼리 관리
    - messages: 대화 이력 저장용 빈 리스트
    - response_times: 응답 속도 저장용 DataFrame
    - button_states: 체크리스트 버튼 상태 저장
    """
    # 1. 기본 세션 상태 한 번에 초기화
    default_states = {
        # "intent_analyzer": IntentAnalyzer(),
        # "db_manager": DatabaseManager(),
        # "memberid": "",
        "messages": [],
        "chat": "",
        "current_analysis": None,
        "user_message": "",
        "speaker": "고객",
        "chat_history": [],
        # "response_times": pd.DataFrame(columns=["timestamp", "total_response_time_sec"]),
        # "show_checklist": False  # 체크리스트 표시 상태 추가
    }
    
    # 2. 세션 상태 한 번에 업데이트
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

def convert_initial_chat_to_history():
    """
    최초 입력된 대화 전문을 채팅 기록 형식으로 변환하고,
    고객 발화와 상담사 발화 사이에 시스템 메시지를 삽입합니다.
    """
    if st.session_state.chat and st.session_state.chat.strip():
        # 정규식으로 발화자 및 메시지 추출
        pattern = r"(고객|상담사[a-zA-Z0-9]?)\)\s*(.*?)(?=(?:\n(?:고객|상담사[a-zA-Z0-9]?)\)|\Z))"
        entries = re.findall(pattern, st.session_state.chat, re.DOTALL)

        # 채팅 기록이 없을 때만 초기화
        if "chat_history" not in st.session_state or not st.session_state.chat_history:
            st.session_state.chat_history = []
        
        # Display chat history
        with ChatContainer:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"<div style='text-align: right; margin: 10px;'><div style='background-color: #e3f2fd; padding: 10px; border-radius: 10px; display: inline-block;'>{message['content']}</div></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: left; margin: 10px;'><div style='background-color: #f5f5f5; padding: 10px; border-radius: 10px; display: inline-block;'>{message['content']}</div></div>", unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input("Type your message:", key="chat_input")
        if user_input:
            logger.info(f'사용자 입력: {user_input}')
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            # Add bot response (you can modify this part to get actual bot responses)
            st.session_state.chat_history.append({"role": "bot", "content": f"Echo: {user_input}"})
            logger.info('채팅 히스토리가 업데이트되었습니다')
            # Clear the input
            st.session_state.chat_input = ""

        system_message_count = 0  # 시스템 메시지 카운터
        customer_message_count = 0  # 고객 발화 카운터 추가

        # 각 메시지를 채팅 기록에 추가
        for i, (role, msg) in enumerate(entries):
            # 상담사 발화의 경우 role을 '상담사'로 통일
            if role.startswith('상담사'):
                role = '상담사'

            # 이미 존재하는 메시지인지 확인
            is_duplicate = any(
                existing_msg["role"] == role and existing_msg["content"] == msg.strip()
                for existing_msg in st.session_state.chat_history
            )

            if not is_duplicate:
                st.session_state.chat_history.append({
                    "role": role,
                    "content": msg.strip()
                })

def handle_input():
    """사용자 입력 처리 함수"""
    chat = st.session_state.chat.strip()
    if not chat:
        return
        
    with st.spinner('분석 중...'):
        # 1. 세션 상태 한 번에 가져오기
        # analyzer = st.session_state.intent_analyzer
        
        # 2. 분석 수행
        # result = analyzer.analyze_intent(chat)
        # result['chat'] = chat
        
        # 3. 세션 상태 한 번에 업데이트
        # st.session_state.current_analysis = result
        
        # 4. 대화 전문 변환
        convert_initial_chat_to_history()

def handle_chat_input():
    """채팅 입력 처리 함수"""
    if not st.session_state.user_message or not st.session_state.speaker:
        return
        
    # 1. 현재 상태 한 번에 가져오기
    current_chat = st.session_state.get('chat', '')
    speaker = st.session_state.speaker
    message = st.session_state.user_message
    
    # 2. 새로운 메시지 생성
    new_message = f"{speaker})\n{message}\n"
    
    # 3. 대화 내용 업데이트
    st.session_state.chat = f"{current_chat}\n{new_message}" if current_chat else new_message
    
    # 4. 채팅 기록 업데이트
    st.session_state.chat_history.append({
        "role": speaker,
        "content": message
    })
    
    # 5. 입력창 초기화
    st.session_state.user_message = ""
    
    # 6. 분석 수행
    handle_input()

def main():
    # Sidebar
    with st.sidebar:
        st.title("Sidebar")
        st.write("This is the sidebar content")

    # Create three containers with unique keys
    header = st.container(key="header")
    body = st.container(key="body")
    footer = st.container(key="footer")

    # Header container
    with header:
        st.title("Header Section")
        st.write("This is the header content")

    # Body container
    with body:
        st.title("Body Section")
        
        # First level columns
        col1, col2 = st.columns([3, 2])
        
        # Chat Container
        with col1:
            st.subheader("Chat")
            ChatContainer = st.container(height=500)
            chat_area = ChatContainer.container()
            with chat_area:
                # chatting = st.container(height=480)
                # with chatting:
                if not st.session_state.chat:
                    st.session_state.chat = ""
                    st.text_area("", 
                                height=450, 
                                placeholder="고객과 상담사의 대화문을 입력하세요.", 
                                key="chat",
                                on_change=convert_initial_chat_to_history)
                else:
                    for message in st.session_state.chat_history:
                        role_class = "customer" if message["role"] == "고객" else "agent" if message["role"] == "상담사" else "system"
                                # st.markdown(f"<div style='text-align: right; margin: 10px;'><div style='background-color: #e3f2fd; padding: 10px; border-radius: 10px; display: inline-block;'>{message['content']}</div></div>", unsafe_allow_html=True)
                            # else:
                            #     st.markdown(f"<div style='text-align: left; margin: 10px;'><div style='background-color: #f5f5f5; padding: 10px; border-radius: 10px; display: inline-block;'>{message['content']}</div></div>", unsafe_allow_html=True)
                    
        
        # Second column with nested container and columns
        with col2:
            st.subheader("Second Column")
            # Create a container in the second column
            container2 = st.container()
            with container2:
                # Nested columns inside the container
                subcol3, subcol4 = st.columns([2, 1])
                with subcol3:
                    st.write("Sub-column 3")
                with subcol4:
                    st.write("Sub-column 4")

    # Footer container
    with footer:
        st.markdown("<div style='text-align: center;'>Footer Section</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    init_components()
    main()
