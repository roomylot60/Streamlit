# app/main.py
# 1. Module import
import os
import pandas as pd
import requests
import streamlit as st
import logging
from typing import List, Tuple
from preprocess import ChatPreprocessor
from core import generate_summary


########################################################
# 2. Define functions
########################################################
# 세션 상태 초기화
def init_session_state():
    if "convert_text_to_chat" not in st.session_state: # bool: 대화 내용을 채팅으로 변환할지 여부
        st.session_state.convert_text_to_chat = True
    if "convert_summary" not in st.session_state: # bool: 요약 결과를 보여줄지 여부
        st.session_state.convert_summary = True
    if "processed_conversation" not in st.session_state: # str: 전처리된 대화 내용
        st.session_state.processed_conversation = ""
    if "split_speaker_sentence" not in st.session_state: # List[Tuple[utterance_id, sentence, speaker]]: 대화 순서, 화자, 문장으로 구분된 대화 내용
        st.session_state.split_speaker_sentence = []
    if "chat_index" not in st.session_state: # int: 채팅 인덱스
        st.session_state.chat_index = 0
    if "current_message" not in st.session_state: # Tuple[int, str, str]: 현재 메시지
        st.session_state.current_message = None

# 채팅 UI 생성: 전체 대화 내용을 출력
def chat_ui_total(messages: List[Tuple[int, str, str]]) -> None:
    chat_content = st.container(height=450)
    chat_area = chat_content.container()
    with chat_area:
        for message in messages:
            _, sentence, speaker = message
            if speaker == '상담사':
                _, col_agent = st.columns([1, 5])
                with col_agent:
                    st.markdown(f"""
                                <div style='text-align: right; 
                                background-color: rgb(250,226,213); 
                                padding: 10px; border-radius: 10px; 
                                width: fit-content; margin-left: auto; margin-bottom: 10px;'>
                                <strong>상담사</strong><br>{sentence}</div>""", unsafe_allow_html=True)
            else:
                col_user, _ = st.columns([5, 1])
                with col_user:
                    st.markdown(f"""
                                <div style='text-align: left; 
                                background-color: rgb(226,232,240); 
                                padding: 10px; border-radius: 10px; 
                                width: fit-content; margin-right: auto; margin-bottom: 10px;'>
                                <strong>고객</strong><br>{sentence}</div>""", unsafe_allow_html=True)

# 채팅 UI 생성: 대화 순서대로 출력
def chat_ui_sequential(messages: List[Tuple[int, str, str]]) -> None:
    chat_content = st.container(height=450)
    chat_area = chat_content.container()

    # 누적 출력
    with chat_area:
        for i in range(st.session_state.chat_index + 1):
            if i < len(messages):
                message = messages[i]
                idx, sentence, speaker = message
                if speaker == '상담사':
                    _, col_agent = st.columns([1, 5])
                    with col_agent:
                        st.markdown(f"""
                            <div style='text-align: right; background-color: rgb(250,226,213); 
                            padding: 10px; border-radius: 10px; width: fit-content; 
                            margin-left: auto; margin-bottom: 10px;'>
                            <strong>상담사</strong><br>{sentence}</div>""", unsafe_allow_html=True)
                else:
                    col_user, _ = st.columns([5, 1])
                    with col_user:
                        st.markdown(f"""
                            <div style='text-align: left; background-color: rgb(226,232,240); 
                            padding: 10px; border-radius: 10px; width: fit-content; 
                            margin-right: auto; margin-bottom: 10px;'>
                            <strong>고객</strong><br>{sentence}</div>""", unsafe_allow_html=True)

    # 다음 버튼 눌렸을 때 인덱스 증가
    if next_button:
        if st.session_state.chat_index < len(messages) - 1:
            st.session_state.chat_index += 1
            st.session_state.current_message = messages[st.session_state.chat_index]
            
# 키워드 강조 함수
def highlight_keywords(text: str, keywords: list[str]) -> str:
    """
    키워드를 굵은 빨간색으로 강조한 HTML 반환
    """
    for keyword in sorted(keywords, key=len, reverse=True):  # 긴 키워드부터 처리
        escaped_keyword = keyword.replace(" ", "&nbsp;")  # 공백 포함 시 처리
        styled_keyword = f'<b><span style="color:red;">{escaped_keyword}</span></b>'
        text = text.replace(keyword, styled_keyword)
    return text

# Markdown 테이블을 생성: 일단 보류(너비 유지 불가)
def generate_markdown_item_value_table(items: list) -> str:
    """
    항목 목록을 받아 각 항목을 행으로 가지는 Markdown 테이블 문자열을 생성한다.
    각 항목의 값은 기본적으로 빈 문자열("")로 초기화된다.

    Parameters:
        items (list): 항목명 리스트

    Returns:
        str: Markdown 테이블 문자열
    """
    header = "| 항목 | 값 |"
    divider = "|------|----|"
    rows = [f"| {item} |  |" for item in items]
    return "\n".join([header, divider] + rows)

########################################################
# 3. Main
########################################################
# 3.1. 페이지 설정
# Web title 설정: Model name 표시
try:
    # llm_model_name = os.getenv("LLM_MODEL")
    llm_model_name = "gemma3:12b-it-fp16"
    # Web title 설정
    page_title = f"GSN - 쿠팡 실시간 인텐트 분류 데모 v2.0({llm_model_name})"
except Exception as e:
    page_title = f"GSN - 쿠팡 실시간 인텐트 분류 데모 v2.0"
    logging.error(f"[ERROR] 모델 이름 요청 실패: {e}")

# 페이지 설정
st.set_page_config(
    page_title=page_title,
    layout="wide" # 더 많은 공간 최적화를 위한 CSS
)

# 로깅 설정
logging.basicConfig(
    filename='./logs/streamlit_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 전처리 객체 생성
preprocessor = ChatPreprocessor()

# 초기 세션 상태 설정
init_session_state()

# 3.2. 영역 생성
# 3.2.1. Header 영역 생성
header_container = st.container()
# 3.2.2. Sidebar 영역 생성
sidebar_container = st.sidebar
# 3.2.3. Main 영역 생성
main_container = st.container()
# 3.2.4. Footer 영역 생성
footer_container = st.container()

# 3.3. 영역 내용 생성
# 3.3.1. Header 영역 내용 생성
with header_container:
    st.title("Chatting Demo")

# 3.3.2. Sidebar 영역 내용 생성
with sidebar_container:
    st.markdown("#### 디버깅 정보")
    st.write(st.session_state.current_message)
    # st.subheader("전처리된 대화")
    # if st.session_state.processed_conversation:
    #     st.markdown(st.session_state.processed_conversation)
    # else:
    #     st.write("전처리된 대화가 없습니다.")
    
# 3.3.3. Main 영역 내용 생성
with main_container:
    chat_col, summary_col = st.columns([4, 3])
    with chat_col:
        st.subheader("고객 상담 채팅")

        # 채팅창 영역 empty placeholder 생성
        chat_placeholder = st.empty()

        # 버튼 동작
        if st.button("요약하기"):
            st.session_state.convert_text_to_chat = not st.session_state.convert_text_to_chat
            st.session_state.convert_summary = not st.session_state.convert_summary

        # 다음 채팅 출력하는 버튼 생성
        next_button = st.button("다음", key="next_button", disabled=st.session_state.convert_text_to_chat)

        # 조건에 따라 placeholder에 다른 요소를 렌더링
        if st.session_state.convert_text_to_chat:
            with chat_placeholder:
                conversation = st.text_area(
                    label="conversation_text",
                    height=450,
                    key="conversation_text",
                    placeholder="상담사, 고객으로 구분된 대화 내용을 입력하세요",
                    label_visibility="collapsed")
                if conversation: # 대화 내용이 있는 경우, 전처리 후 session_state 업데이트
                    processed_conversation, split_speaker_sentence = preprocessor.process_conversation(conversation)
                    st.session_state.processed_conversation = processed_conversation
                    st.session_state.split_speaker_sentence = split_speaker_sentence
        else:
            with chat_placeholder:
                messages = st.session_state.split_speaker_sentence
                # chat_ui_total(messages) # 전체 대화 내용을 출력
                chat_ui_sequential(messages) # 대화 순서대로 출력

    with summary_col:
        st.subheader("요약 결과")

        # 요약 결과 영역 empty placeholder 생성
        summary_placeholder = st.empty()
        
        if st.session_state.convert_summary:
            keys = ["Intent 당 평균 응답속도", "총 응답속도", "상품명", "Intent", " Request", "Utterance", "요약", "고객문제", "고객요청", "고객불만", "상담사응대"]
            values = ["", "", "", "", "", "", "", "", "", "", ""]
            # markdown_table = generate_markdown_item_value_table(items)
            # st.markdown(markdown_table)
            df = pd.DataFrame({"항목": keys, "값": values})
            st.dataframe(df, height=450, hide_index=True, use_container_width=True)
        else:
            with summary_placeholder:
                if st.session_state.current_message[2] == "고객":
                    query = st.session_state.current_message[2] + ") " + st.session_state.current_message[1]
                    api_url = "http://192.168.0.90:43307/llm_intent_select2"
                    response = requests.post(api_url, json={"query": query})
                    meta_data = response.json()["selected_intent_data"]
                    intent_response_time = response.json()["intent_response_time"]
                    intent = response.json()["Intent"]
                    request = response.json()["Request"]
                    summary = generate_summary(query, {})

                st.write("요약 결과")
                keys = ["Intent 당 평균 응답속도", "총 응답속도", "상품명", "Intent", "Request", "Utterance", "요약", "고객문제", "고객요청", "고객불만", "상담사응대"]
                values = [intent_response_time, "", "", intent, request, "", summary, "", "", "", ""]
                df = pd.DataFrame({"항목": keys, "값": values})
                st.dataframe(df, height=450, hide_index=True, use_container_width=True)

# 3.3.4. Footer 영역 내용 생성
with footer_container:
    # 전처리된 대화 표시 (더 보기 좋게)
        st.subheader("전처리된 대화")
        if st.session_state.processed_conversation:
            st.markdown("```\n" + st.session_state.processed_conversation + "\n```")
        else:
            st.write("전처리된 대화가 없습니다.")

