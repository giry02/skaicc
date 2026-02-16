import streamlit as st
import shutil
import os
import time
from dotenv import load_dotenv # Added to load .env
load_dotenv() # Load environment variables from .env

from utils.logger import logger
from workflow.orchestrator import Orchestrator
from agents.roles import *

# Function to initialize session state
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "orchestrator" not in st.session_state:
         # Initialize Orchestrator only once
         st.session_state.orchestrator = Orchestrator(input_handler=None) # No input handler needed for automated flow

# Callback function to stream logs to Streamlit
def streamlit_log_callback(entry):
    # Determine the role for the avatar/name
    role = entry.get('role', 'System')
    sender = entry.get('sender', role)
    content = entry.get('content', '')
    msg_type = entry.get('type', 'message')

    # Filter out internal thoughts if needed, or show them as collapsible
    # For now, let's show everything but style it differently
    if msg_type == 'thought':
        # Don't show thoughts in main chat to keep it clean, or show as expanded
        with st.expander(f"💭 {sender}의 생각"):
            st.write(content)
        # Also append to history for persistence
        st.session_state.messages.append({"role": "assistant", "content": f"💭 **{sender}**: {content}", "type": "thought"})
    elif msg_type == 'system':
        # System messages
        if "Error" in content or "오류" in content:
             st.error(f"🚨 {content}")
             st.session_state.messages.append({"role": "system", "content": content, "type": "error"})
        else:
             # Regular system logs (phases, etc.)
             st.info(f"ℹ️ {content}")
             st.session_state.messages.append({"role": "system", "content": content, "type": "info"})
    elif msg_type == 'action':
        # Actions
        st.caption(f"🎬 {sender}: {content}")
        st.session_state.messages.append({"role": "assistant", "content": f"🎬 **{sender}**: {content}", "type": "action"})
    else:
        # Standard messages
        with st.chat_message("assistant", avatar="🤖"):
            st.write(f"**{sender}**: {content}")
        st.session_state.messages.append({"role": "assistant", "content": f"**{sender}**: {content}", "type": "message"})

# Main App Layout
st.set_page_config(page_title="Multi-Agent Dev Team", page_icon="🤖", layout="wide")

st.title("🤖 Multi-Agent Dev Team (Web Interface)")
st.markdown("""
**Captain Jack(PM)**과 그의 팀원들(Planner, Designer, Developer)이 당신의 아이디어를 현실로 만들어 드립니다.
""")

# Sidebar for configuration
with st.sidebar:
    st.header("설정")
    st.info("현재 모델: Gemini-1.5-Flash (무료/고속)")
    if st.button("대화 내용 초기화"):
        st.session_state.messages = []
        st.rerun()

# Initialize
init_session_state()

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        if msg.get("type") == "thought":
            with st.expander(msg["content"].split(":", 1)[0]): # Approximate title
                st.write(msg["content"])
        elif msg.get("type") == "action":
            st.caption(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(msg["content"])
    elif msg["role"] == "system":
        if msg.get("type") == "error":
             st.error(msg["content"])
        else:
             st.info(msg["content"])

# Chat Input
if prompt := st.chat_input("무엇을 만들어 드릴까요? (예: 투두리스트 앱 만들어줘)"):
    # 1. Display User Message
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Run Orchestrator
    # Register callback to write directly to the stream
    logger.register_callback(streamlit_log_callback)
    
    with st.spinner("에이전트 팀이 작업 중입니다..."):
        try:
             # Run the waterfall process
             final_code, test_report = st.session_state.orchestrator.run_waterfall(prompt)
             
             # 3. Display Final Result
             st.success("작업 완료!")
             st.subheader("📝 최종 결과물 (Code)")
             st.code(final_code, language='html')
             
             st.subheader("🧪 테스트 리포트")
             st.text(test_report)
             
             # Save to session history
             st.session_state.messages.append({"role": "assistant", "content": "작업이 완료되었습니다. 결과물을 확인해주세요."})
             
        except Exception as e:
             st.error(f"오류 발생: {e}")
             logger.log_system(f"Critical Error: {e}")
