import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

# changes testing
# AutoGen v0.4+ Imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables
load_dotenv()


# Streamlit Page Setup
st.set_page_config(page_title="Multi-Department Support Desk", page_icon="🤖", layout="wide")
st.title("🤖 Customer Enterprise Support Chatbot")
st.write("Select a department and ask your query below.")

# ------------------------------------------------------------------
# 1. Department System Prompts Configuration
# ------------------------------------------------------------------
DEPARTMENT_PROMPTS = {
    "IT Support": (
        "You are an IT Technical Support Specialist. Help users with hardware, software, "
        "VPN access, network troubleshooting, password resets, and computer setup. "
        "Provide clear, step-by-step technical instructions."
    ),
    "Admin Support": (
        "You are an Office Administration Specialist. Help users with facility requests, "
        "office supplies, visitor passes, desk bookings, events, and company policy inquiries."
    ),
    "Finance Support": (
        "You are a Finance & Payroll Specialist. Help users with expense reimbursements, "
        "payroll queries, invoicing, tax forms, and budget approvals. "
        "Maintain strict policy guidelines."
    ),
    "Infrastructure Support": (
        "You are an IT Infrastructure & Cloud Engineer. Help users with server deployment, "
        "cloud resources (AWS/Azure/GCP), database connections, CI/CD pipelines, and DevOps issues."
    )
}

# ------------------------------------------------------------------
# 2. Agent Instantiation Helper
# ------------------------------------------------------------------
def get_department_agent(department: str) -> AssistantAgent:
    """Creates a specialized AutoGen AssistantAgent based on the selected department."""
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    agent = AssistantAgent(
        name=department.replace(" ", "_").lower(),
        model_client=model_client,
        system_message=DEPARTMENT_PROMPTS[department]
    )
    return agent

# ------------------------------------------------------------------
# 3. Streamlit Sidebar & Options
# ------------------------------------------------------------------
st.sidebar.header("Support Routing")
selected_dept = st.sidebar.selectbox(
    "Choose Department:",
    list(DEPARTMENT_PROMPTS.keys())
)

st.sidebar.markdown("---")
st.sidebar.info(f"**Active Agent:** {selected_dept}\n\n{DEPARTMENT_PROMPTS[selected_dept]}")

# ------------------------------------------------------------------
# 4. Session State Management
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(f"**[{msg['dept']}]** {msg['content']}" if msg["role"] == "assistant" else msg["content"])

# ------------------------------------------------------------------
# 5. Async Logic to Run AutoGen Agent
# ------------------------------------------------------------------
async def run_agent_query(agent: AssistantAgent, prompt: str) -> str:
    response = await agent.run(task=prompt)
    # Extract the final message content from AutoGen response
    return response.messages[-1].content

# ------------------------------------------------------------------
# 6. Chat Input & Execution
# ------------------------------------------------------------------
if user_input := st.chat_input(f"Ask {selected_dept}..."):
    # Display user input in UI
    st.session_state.messages.append({"role": "user", "content": user_input, "dept": selected_dept})
    with st.chat_message("user"):
        st.write(user_input)

    # Process query through AutoGen Agent
    with st.chat_message("assistant"):
        with st.spinner(f"{selected_dept} agent is thinking..."):
            # Initialize agent for chosen department
            active_agent = get_department_agent(selected_dept)
            
            # Execute async call
            response_text = asyncio.run(run_agent_query(active_agent, user_input))
            
            st.write(response_text)
            
            # Save assistant message to state
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "dept": selected_dept
            })