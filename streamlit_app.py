import streamlit as st
from banking_bot import BankingBot
import os

# Page configuration - must be first
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 HBDB Banking Bot")
st.markdown("Your 24/7 Banking Assistant - Powered by Mistral AI")

# Get API key - try multiple sources
api_key = None

# 1. Try environment variable (for cloud/Docker)
api_key = os.getenv("MISTRAL_API_KEY")
if api_key:
    st.sidebar.success("✓ API Key from environment")

# 2. Try Streamlit secrets (for Cloud)
if not api_key:
    try:
        api_key = st.secrets.get("MISTRAL_API_KEY")
        if api_key:
            st.sidebar.success("✓ API Key from secrets")
    except:
        pass

# 3. Hardcoded fallback for testing
if not api_key:
    api_key = "hKjvYtwfSKR7Ysd7WKvmItCtPL6YfjdR"
    st.sidebar.info("ℹ️ Using default API key")

# Check CSV file exists
csv_path = "hbdb_banking_faqs (2) (1).csv"
if not os.path.exists(csv_path):
    st.error(f"❌ CSV file not found: {csv_path}")
    st.stop()

# Initialize bot
@st.cache_resource
def init_bot():
    try:
        bot = BankingBot(api_key=api_key, csv_path=csv_path)
        return bot
    except Exception as e:
        st.error(f"❌ Failed to initialize bot: {str(e)}")
        st.stop()

bot = init_bot()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask me about HBDB banking services...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get and display bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Generate response with timeout protection
            for chunk in bot.get_response(user_input):
                if chunk:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
            
            # Final display without cursor
            if full_response:
                message_placeholder.markdown(full_response)
            else:
                message_placeholder.markdown("I apologize, I could not generate a response. Please try again.")
                full_response = "Error: No response generated"
                
        except Exception as e:
            error_msg = f"⚠️ Error: {str(e)}"
            message_placeholder.markdown(error_msg)
            full_response = error_msg
    
    # Add response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar
with st.sidebar:
    st.markdown("### 📚 About")
    st.markdown("Banking assistant powered by Mistral AI")
    
    st.markdown("---")
    st.markdown("### ❓ Quick Questions")
    
    questions = [
        "How do I open a savings account?",
        "What is HBDB Premier?",
        "How do I reset my password?"
    ]
    
    for q in questions:
        if st.button(q, key=f"btn_{q}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Status:** ✓ Ready")


