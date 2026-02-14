import streamlit as st
from banking_bot import BankingBot
import os
import sys

# Page configuration - must be first
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    </style>
""", unsafe_allow_html=True)

# Title - always show this
st.title("🏦 HBDB Banking Bot")
st.markdown("Your 24/7 Banking Assistant - Powered by Mistral AI")

# Debug: Show what we're working with
debug_mode = os.getenv("DEBUG", "false").lower() == "true"

# Get API key
api_key = None

# Try environment variable first
api_key = os.getenv("MISTRAL_API_KEY")

# Try secrets if environment variable not found
if not api_key:
    try:
        api_key = st.secrets.get("MISTRAL_API_KEY", None)
    except:
        pass

# Hardcoded fallback for testing
if not api_key:
    api_key = "hKjvYtwfSKR7Ysd7WKvmItCtPL6YfjdR"

# Check CSV file
csv_files = [
    "hbdb_banking_faqs (2) (1).csv",
    "hbdb_banking_faqs.csv"
]

csv_path = None
for csv_file in csv_files:
    if os.path.exists(csv_file):
        csv_path = csv_file
        break

if not csv_path:
    st.error("❌ **ERROR: FAQ CSV file not found!**")
    st.info("Looking for: " + " or ".join(csv_files))
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "bot" not in st.session_state:
    try:
        st.session_state.bot = BankingBot(api_key=api_key, csv_path=csv_path)
    except Exception as e:
        st.error(f"❌ **Failed to initialize bot:** {str(e)}")
        if debug_mode:
            st.error(f"Full error: {repr(e)}")
        st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about HBDB banking services..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            for chunk in st.session_state.bot.get_response(prompt):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            error_msg = f"⚠️ Error: {str(e)}"
            message_placeholder.markdown(error_msg)
            full_response = error_msg
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar
with st.sidebar:
    st.markdown("### 📚 About This Bot")
    st.markdown("""
    Banking assistant powered by Mistral AI.
    
    **Features:**
    - 📋 Instant answers
    - 🔒 Secure chats
    - 🚀 Real-time responses
    """)
    
    st.markdown("---")
    st.markdown("### ❓ Try asking:")
    
    example_qs = [
        "How do I open a savings account?",
        "What is HBDB Premier?",
        "How do I reset my password?"
    ]
    
    for q in example_qs:
        if st.button(q, key=q):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


