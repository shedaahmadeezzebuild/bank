import streamlit as st
from banking_bot import BankingBot
import os

# Page configuration
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stChatMessage {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .bot-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1976d2;
    }
    .user-message {
        background-color: #f3e5f5;
        border-left: 4px solid #7b1fa2;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 HBDB Banking Bot")
st.markdown("Your 24/7 Banking Assistant - Powered by Mistral AI")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "bot" not in st.session_state:
    # Initialize the bot with API key from environment or secrets
    try:
        # Try to get API key from Streamlit secrets (preferred for cloud deployment)
        api_key = st.secrets.get("MISTRAL_API_KEY", "")
        
        # If not found in secrets, try environment variable
        if not api_key:
            api_key = os.getenv("MISTRAL_API_KEY", "")
        
        # Fallback to direct key (only for local development)
        if not api_key:
            api_key = "hKjvYtwfSKR7Ysd7WKvmItCtPL6YfjdR"
        
        csv_path = "hbdb_banking_faqs (2) (1).csv"
        
        if os.path.exists(csv_path):
            st.session_state.bot = BankingBot(api_key=api_key, csv_path=csv_path)
        else:
            st.error(f"❌ CSV file not found: {csv_path}")
            st.stop()
    except Exception as e:
        st.error(f"❌ Failed to initialize bot: {str(e)}")
        st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about HBDB banking services..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Stream the response
            for chunk in st.session_state.bot.get_response(prompt):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            error_message = f"⚠️ Error: {str(e)}"
            message_placeholder.markdown(error_message)
            full_response = error_message
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar with information
with st.sidebar:
    st.markdown("### 📚 About This Bot")
    st.markdown("""
    This banking bot is trained on HBDB's FAQ database and powered by Mistral AI's Large language model.
    
    **Features:**
    - 📋 Instant answers to banking questions
    - 🔒 Secure and private conversations
    - 🚀 Real-time streaming responses
    - 💬 Natural conversation interface
    """)
    
    st.markdown("---")
    
    st.markdown("### ❓ Example Questions")
    example_questions = [
        "How do I open a savings account?",
        "What is HBDB Premier?",
        "How do I reset my password?",
        "How do I contact customer service?",
        "What are the mortgage rates?"
    ]
    
    st.markdown("Try asking:")
    for q in example_questions:
        if st.button(q, key=q):
            st.session_state.messages.append({"role": "user", "content": q})
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
    <small>Powered by Mistral AI</small>
    </div>
    """, unsafe_allow_html=True)

