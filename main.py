import streamlit as st

st.set_page_config(layout="wide")

# Load external CSS
with open('assets/css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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
        st.subheader("채팅")
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            st.session_state.initial_input = True
        
        if st.session_state.initial_input:
            st.subheader("대화 전문 입력")
            conversation_text = st.text_area("대화를 한 줄씩 입력하세요:", height=200)
            if st.button("대화 시작"):
                if conversation_text:
                    st.session_state.chat_history = []
                    lines = conversation_text.strip().split('\n')
                    current_speaker = "user1"
                    for line in lines:
                        if line.strip():
                            st.session_state.chat_history.append({
                                "role": current_speaker,
                                "content": line.strip()
                            })
                            current_speaker = "user2" if current_speaker == "user1" else "user1"
                    st.session_state.initial_input = False
                    st.rerun()
        else:
            # 채팅창 컨테이너 (다크모드 지원)
            chat_container = st.container()
            with chat_container:
                chat_html = "<div style='height: 400px; overflow-y: auto; border: 1px solid #444; border-radius: 5px; padding: 10px; background-color: #18191a;'>"
                for message in st.session_state.chat_history:
                    if message["role"] == "user1":
                        chat_html += f"<div style='text-align: right; margin: 10px;'><div style='background-color: #263a53; color: #fff; padding: 10px; border-radius: 10px; display: inline-block;'>{message['content']}</div></div>"
                    else:
                        chat_html += f"<div style='text-align: left; margin: 10px;'><div style='background-color: #333; color: #fff; padding: 10px; border-radius: 10px; display: inline-block;'>{message['content']}</div></div>"
                chat_html += "</div>"
                st.markdown(chat_html, unsafe_allow_html=True)
            
            # 입력창, 화자 선택, 전송 버튼 한 줄 배치
            st.subheader("새 메시지 입력")
            chat_col1, chat_col2, chat_col3 = st.columns([1, 4, 1])
            with chat_col1:
                speaker = st.selectbox("화자 선택", ["화자1", "화자2"], label_visibility="collapsed")
            with chat_col2:
                if "new_message" not in st.session_state:
                    st.session_state.new_message = ""
                new_message = st.text_input("메시지 입력", value=st.session_state.new_message, key="new_message", label_visibility="collapsed")
            with chat_col3:
                if st.button("전송"):
                    if st.session_state.new_message:
                        role = "user1" if speaker == "화자1" else "user2"
                        st.session_state.chat_history.append({
                            "role": role,
                            "content": st.session_state.new_message
                        })
                        st.session_state.new_message = ""  # 입력창 비우기
                        st.rerun()
    
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
