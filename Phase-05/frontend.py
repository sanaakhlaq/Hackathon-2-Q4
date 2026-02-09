import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="AI Agentic Manager",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Styling (Fixing the Black Text Issue)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    
    /* Sidebar Task Card Styling */
    .task-card {
        background-color: #1e293b; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #3b82f6; 
        margin-bottom: 10px;
        color: #ffffff !important; /* Text color forced to white */
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* Button Styling */
    div.stButton > button:first-child {
        background-color: #3b82f6; 
        color: white; 
        border-radius: 10px; 
        width: 100%; 
        border: none;
        font-weight: bold;
    }
    
    /* Headers color */
    h1, h2, h3 { color: #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# Backend URL
API_URL = "http://127.0.0.1:8000/chat-with-ai"

# Function to fetch tasks (Helper for Auto-Sync)
def sync_tasks():
    try:
        res = requests.post(API_URL, json={"prompt": "list all tasks", "conversation_id": 1})
        if res.status_code == 200:
            st.session_state.last_tasks = res.json().get("ai_response")
    except:
        pass

# 3. Sidebar
with st.sidebar:
    st.title("📊 Task Control")
    st.markdown("---")
    
    if st.button("🔄 Manual Sync"):
        with st.spinner("Syncing..."):
            sync_tasks()

    st.markdown("### 📝 Current Tasks")
    if "last_tasks" in st.session_state:
        # Rendering the task list inside our colorful card
        st.markdown(f'<div class="task-card">{st.session_state.last_tasks}</div>', unsafe_allow_html=True)
    else:
        st.info("No tasks synced yet.")

# 4. Main Chat Interface
st.title("⚡ Agentic Todo Assistant")
st.caption("FastAPI + Llama-3 | Real-time Database Integration")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Agent. Try adding a task or asking for your list!"}
    ]

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What should I do next?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Backend
    try:
        with st.spinner("AI Agent is working..."):
            response = requests.post(API_URL, json={"prompt": prompt, "conversation_id": 1})
            if response.status_code == 200:
                ai_reply = response.json().get("ai_response")
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                with st.chat_message("assistant"):
                    st.markdown(ai_reply)
                
                # --- AUTO-SYNC LOGIC ---
                # Task add/delete ke baad khud hi sidebar update karega
                sync_tasks()
                st.rerun() 
            else:
                st.error("API Error")
    except Exception as e:
        st.error(f"Backend Offline: {e}")