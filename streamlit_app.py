import streamlit as st
from banking_bot import BankingBot
import os

# Page configuration - must be first
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional 3D CSS styling
st.markdown("""
    <style>
    /* Root colors and backgrounds */
    :root {
        --primary: #1e3a8a;
        --primary-light: #3b82f6;
        --accent: #f59e0b;
        --success: #10b981;
        --bg: #f8fafc;
        --card-shadow: 0 10px 30px rgba(0,0,0,0.1);
        --card-hover: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
    }
    
    /* Title styling */
    h1 {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 2.8rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 0.5rem !important;
    }
    
    /* Subtitle */
    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
    }
    
    /* Chat messages - 3D card effect */
    .stChatMessage {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #3b82f6;
        transition: all 0.3s ease;
    }
    
    .stChatMessage:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* User message styling */
    [data-testid="chatAvatarIcon-user"] ~ div {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        border-radius: 8px !important;
    }
    
    /* Assistant message styling */
    [data-testid="chatAvatarIcon-assistant"] ~ div {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-radius: 8px !important;
    }
    
    /* Chat input area */
    .stChatInputContainer {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    
    /* Input text */
    .stChatInputContainer input {
        font-size: 1rem;
        border: none !important;
        padding: 8px 4px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #2563eb 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Sidebar section headers */
    [data-testid="stSidebar"] h3 {
        color: #fff;
        font-weight: 700;
        font-size: 1.2rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 2px solid rgba(255,255,255,0.2);
        padding-bottom: 0.5rem;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p {
        color: #e0e7ff;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Buttons - enhanced 3D effect */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Dark buttons for sidebar */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #de8e27 0%, #b45309 100%);
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.4);
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
    }
    
    /* Info message */
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    
    /* Divider */
    hr {
        border: none;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent);
        height: 2px;
        margin: 1.5rem 0;
    }
    
    /* Status indicator */
    .status-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    /* Links */
    a {
        color: #3b82f6;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #2563eb;
        text-decoration: underline;
    }
    
    /* Markdown text improvements */
    [data-testid="stMarkdownContainer"] {
        color: #1f2937;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    '<div style="padding: 20px; background: linear-gradient(135deg, #fff 0%, #f0f9ff 100%); border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 2rem;">'
    '<h1 style="margin: 0; padding: 0;">🏦 HBDB Banking Bot</h1>'
    '<p class="subtitle" style="margin: 8px 0 0 0; color: #64748b;">Your 24/7 Banking Assistant - Powered by Mistral AI</p>'
    '</div>',
    unsafe_allow_html=True
)

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

if "response_needed" not in st.session_state:
    st.session_state.response_needed = False

# Display all chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check if we need to generate a response
def needs_response():
    if not st.session_state.messages:
        return False
    return st.session_state.messages[-1]["role"] == "user"

# Generate response if needed
if needs_response():
    user_message = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            for chunk in bot.get_response(user_message):
                if chunk:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
            
            if full_response:
                message_placeholder.markdown(full_response)
            else:
                message_placeholder.markdown("I apologize, I could not generate a response.")
                full_response = "Error: No response"
                
        except Exception as e:
            error_msg = f"⚠️ Error: {str(e)}"
            message_placeholder.markdown(error_msg)
            full_response = error_msg
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Chat input
user_input = st.chat_input("Ask me about HBDB banking services...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 📚 About This Bot")
    st.markdown(
        "Intelligent banking assistant powered by **Mistral AI**. Get instant answers to all your HBDB banking questions."
    )
    
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
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        st.markdown(
            '<span style="display: flex; align-items: center; justify-content: center; padding: 8px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border-radius: 8px; font-weight: 600; font-size: 0.85rem;">✓ Ready</span>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    st.markdown(
        "<p style='text-align: center; color: #cbd5e1; font-size: 0.85rem;'>"
        "🚀 <strong>Professional Banking Assistant</strong><br/>"
        "Powered by Advanced AI<br/>"
        "© 2026 HBDB"
        "</p>",
        unsafe_allow_html=True
    )


