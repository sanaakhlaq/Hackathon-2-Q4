import streamlit as st
import requests
from datetime import datetime

# Set page config for wide mode and emoji theme
st.set_page_config(
    page_title="Agentic Todo App 🚀",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = 1

# Custom CSS for emoji theme
st.markdown("""
<style>
    .emoji-header {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .task-item {
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 0.25rem 0;
        background-color: #f0f2f6;
        border-left: 4px solid #4CAF50;
    }
    .task-completed {
        text-decoration: line-through;
        color: gray;
    }
    .refresh-button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 0.5rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

def get_ai_response(prompt):
    """Send prompt to backend API and return AI response"""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat-with-ai",
            json={
                "prompt": prompt,
                "conversation_id": st.session_state.conversation_id
            },
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return response.json()["ai_response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

def refresh_tasks():
    """Refresh the task list from the AI"""
    with st.spinner("Updating task list..."):
        task_prompt = "What are my current tasks? Please provide them in a numbered list."
        ai_response = get_ai_response(task_prompt)
        
        # Parse the response to extract tasks
        # This assumes the AI returns tasks in a numbered list format
        lines = ai_response.split('\n')
        tasks = []
        for line in lines:
            # Look for numbered list items
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '0.')):
                task_text = line.split('.', 1)[1].strip()
                tasks.append({"text": task_text, "completed": False})
        
        st.session_state.tasks = tasks
        st.success("Task list updated!")

# Sidebar for task list
with st.sidebar:
    st.markdown('<div class="emoji-header">📋 Current Task List</div>', unsafe_allow_html=True)
    
    # Refresh button
    if st.button('🔄 Refresh Tasks', key='refresh_btn', use_container_width=True):
        refresh_tasks()
    
    # Display tasks
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            task_class = "task-item"
            if task["completed"]:
                task_class += " task-completed"
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="{task_class}">{task["text"]}</div>', unsafe_allow_html=True)
            with col2:
                if st.button('✅' if not task["completed"] else '❌', key=f'toggle_{i}'):
                    st.session_state.tasks[i]["completed"] = not task["completed"]
                    st.rerun()
    else:
        st.info("No tasks yet. Chat with the AI to add tasks!")

# Main chat interface
st.markdown('<div class="emoji-header">🤖 AI Assistant</div>', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your tasks or add new ones..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_response = get_ai_response(prompt)
        st.markdown(ai_response)
    
    # Add AI response to chat
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Check if the user asked about tasks to update the sidebar
    if any(word in prompt.lower() for word in ["task", "list", "todo", "what should i"]):
        refresh_tasks()