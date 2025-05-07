import streamlit as st
import re

st.set_page_config(layout="wide")

# 외부 CSS 파일 로드
with open('assets/css/style.css') as f:
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
        "current_speaker": "고객",  # 현재 선택된 발화자
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
    if not st.session_state.user_message or not st.session_state.current_speaker:
        return
        
    # 1. 현재 상태 가져오기
    speaker = st.session_state.current_speaker
    message = st.session_state.user_message
    
    # 2. 채팅 기록 업데이트
    st.session_state.chat_history.append({
        "role": speaker,
        "content": message
    })
    
    # 3. 입력창 초기화
    st.session_state.user_message = ""

def main():
    # 사이드바
    with st.sidebar:
        st.title("Sidebar")
        st.write("This is the sidebar content")

    # 고유 키를 가진 세 개의 컨테이너 생성
    header = st.container(key="header")
    body = st.container(key="body")
    footer = st.container(key="footer")

    # 헤더 컨테이너
    with header:
        st.title("Header Section")
        st.write("This is the header content")

    # 본문 컨테이너
    with body:
        st.title("Body Section")
        
        # 첫 번째 레벨 컬럼
        col1, col2 = st.columns([3, 2])
        
        # 채팅 컨테이너
        with col1:
            st.subheader("Chat")
            
            if not st.session_state.chat:
                st.text_area("", 
                            height=600, 
                            placeholder="고객과 상담사의 대화문을 입력하세요.", 
                            key="chat",
                            on_change=convert_initial_chat_to_history)
            else:
                # 채팅 메시지 렌더링 (모든 메시지를 하나의 HTML로 합침)
                chat_html = "<div style='height: 600px; overflow-y: auto; border: 1px solid #444; border-radius: 5px; padding: 10px; background-color: #18191a; display: flex; flex-direction: column; gap: 10px;'>"
                for message in st.session_state.chat_history:
                    if message["role"] == "고객":
                        chat_html += f"<div style='display: flex; justify-content: flex-end; margin: 5px 0;'><div style='background-color: #263a53; color: #fff; padding: 10px 15px; border-radius: 10px; max-width: 70%; word-wrap: break-word;'>{message['content']}</div></div>"
                    else:
                        chat_html += f"<div style='display: flex; justify-content: flex-start; margin: 5px 0;'><div style='background-color: #333; color: #fff; padding: 10px 15px; border-radius: 10px; max-width: 70%; word-wrap: break-word;'>{message['content']}</div></div>"
                chat_html += "</div>"
                st.markdown(chat_html, unsafe_allow_html=True)
            
            # 새 메시지 입력 영역
            st.subheader("새 메시지 입력")
            chat_col1, chat_col2, chat_col3 = st.columns([1, 4, 1])
            with chat_col1:
                speaker = st.selectbox("화자 선택", ["고객", "상담사"], label_visibility="collapsed")
            with chat_col2:
                message = st.text_input("메시지 입력", key="new_message", label_visibility="collapsed")
            with chat_col3:
                if st.button("전송"):
                    if message:
                        st.session_state.chat_history.append({
                            "role": speaker,
                            "content": message
                        })
        
        # 두 번째 컬럼 (중첩된 컨테이너와 컬럼)
        with col2:
            st.subheader("Second Column")
            # 두 번째 컬럼에 컨테이너 생성
            container2 = st.container()
            with container2:
                # 컨테이너 내부의 중첩된 컬럼
                subcol3, subcol4 = st.columns([2, 1])
                with subcol3:
                    st.write("Sub-column 3")
                with subcol4:
                    st.write("Sub-column 4")

    # 푸터 컨테이너
    with footer:
        st.markdown("<div style='text-align: center;'>Footer Section</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    init_components()
    main()