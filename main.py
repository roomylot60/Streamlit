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
        st.subheader("Chat")
        ChatContainer = st.container()
        
        # Initialize chat history in session state if it doesn't exist
        if 'chat_history' not in st.session_state:
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
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            # Add bot response (you can modify this part to get actual bot responses)
            st.session_state.chat_history.append({"role": "bot", "content": f"Echo: {user_input}"})
            # Clear the input
            st.session_state.chat_input = ""
            # Rerun to update the chat display
            st.experimental_rerun()
    
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
