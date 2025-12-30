import streamlit as st
from team.dsa_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio

# Page config for better UI
st.set_page_config(
    page_title="AlgoGenie - DSA Solver",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for bigger fonts and better styling
st.markdown("""
    <style>
    /* Main content font size */
    .main {
        font-size: 1.2rem;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Input box font size */
    .stTextInput > div > div > input {
        font-size: 1.2rem;
    }
    
    /* Chat messages font size */
    .stChatMessage {
        font-size: 1.2rem;
    }
    
    /* Button font size */
    .stButton > button {
        font-size: 1.3rem;
        font-weight: bold;
    }
    
    /* Sidebar font size */
    .css-1d391kg {
        font-size: 1.1rem;
    }
    
    /* All markdown text */
    .stMarkdown {
        font-size: 1.2rem;
    }
    
    /* Code blocks */
    code {
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🧠 AlgoGenie - DSA Problem Solver</p>', unsafe_allow_html=True)
st.write("Welcome to AlgoGenie, your personal DSA problem solver! Here you can ask solutions to various data structures and algorithms problems.")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About AlgoGenie")
    st.info("AlgoGenie uses AI agents to solve DSA problems and executes code in a secure Docker environment.")
    st.markdown("---")
    st.markdown("**Features:**")
    st.markdown("- 🤖 Multi-agent problem solving")
    st.markdown("- 🐳 Secure Docker execution")
    st.markdown("- 💾 Auto-save solutions")
    st.markdown("- 📊 Real-time streaming")

task = st.text_input("Enter your DSA problem or question:", value='Write a function to add two numbers')

async def run_task(team, docker, task):
    messages = []
    try:
        await start_docker_container(docker)
        
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                msg = f"{message.source} : {message.content}"
                print(msg)
                messages.append({"type": "text", "source": message.source, "content": message.content})
                
            elif isinstance(message, TaskResult):
                msg = f"Stop Reason: {message.stop_reason}"
                print(msg)
                messages.append({"type": "result", "reason": message.stop_reason})
        
        print("Task Completed")
        messages.append({"type": "completed"})
        
    except Exception as e:
        print(f"Error: {e}")
        messages.append({"type": "error", "content": str(e)})
        
    finally:
        print("Stopping Docker container...")
        await stop_docker_container(docker)
        print("Docker container stopped.")
    
    return messages

if st.button("🚀 Run", type="primary", use_container_width=True):
    with st.spinner('⏳ Running the Task...'):
        team, docker = get_dsa_team_and_docker()
        
        # Run async function and get all messages
        messages = asyncio.run(run_task(team, docker, task))
    
    st.success("✅ Task Completed!")
    st.markdown("---")
    
    # Display all messages
    for msg in messages:
        if msg["type"] == "text":
            source = msg["source"]
            content = msg["content"]
            
            if source == "user":
                with st.chat_message('user', avatar='👤'):
                    st.markdown(f"**Question:**")
                    st.markdown(content)
                    
            elif "DSA_Problem_Solver" in source:
                with st.chat_message('assistant', avatar='🧑‍💻'):
                    st.markdown(f"**Solution:**")
                    st.markdown(content)
                    
            elif "Executor" in source or "CodeExecutor" in source:
                with st.chat_message('assistant', avatar='▶️'):
                    st.markdown(f"**Execution Output:**")
                    # Try to display as code if it's output
                    if content.strip():
                        st.code(content, language="text")
                    
        elif msg["type"] == "result":
            # Just show completed status without reason
            st.success("✅ Task Completed Successfully!")
            
        elif msg["type"] == "error":
            st.error(f"❌ Error: {msg['content']}")
    
    # Footer with download option
    st.markdown("---")
    st.info("💡 **Tip:** Your solution has been saved to `solution.py` in the coding directory.")