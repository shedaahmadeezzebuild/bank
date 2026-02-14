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

# Professional Black & White CSS styling with custom avatars
st.markdown("""
    <style>
    /* Root colors and backgrounds */
    :root {
        --primary: #000000;
        --primary-light: #1a1a1a;
        --accent: #ffffff;
        --dark-gray: #2d2d2d;
        --light-gray: #f5f5f5;
        --text-dark: #1a1a1a;
        --text-light: #ffffff;
        --card-shadow: 0 10px 30px rgba(0,0,0,0.15);
        --card-hover: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        padding: 2rem;
    }
    
    /* Title styling */
    h1 {
        background: linear-gradient(135deg, #000000 0%, #2d2d2d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 2.8rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px;
    }
    
    /* Subtitle */
    .subtitle {
        color: #555555;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
    }
    
    /* Chat container */
    .stChatMessage {
        background: white;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid #000000;
        transition: all 0.3s ease;
    }
    
    .stChatMessage:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        transform: translateY(-3px);
        border-left-color: #2d2d2d;
    }
    
    /* Custom user avatar - Person icon */
    [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important;
        border-radius: 10px !important;
        font-size: 1.5rem !important;
    }
    
    /* Custom assistant avatar - Robot/AI icon */
    [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #ffffff 0%, #e8e8e8 100%) !important;
        border: 2px solid #000000 !important;
        border-radius: 10px !important;
        font-size: 1.5rem !important;
        color: #000000 !important;
    }
    
    /* Chat message text */
    [data-testid="chatAvatarIcon-user"] ~ div {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    
    [data-testid="chatAvatarIcon-assistant"] ~ div {
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%) !important;
        color: #1a1a1a !important;
        border-radius: 12px !important;
        padding: 12px !important;
        border: 1px solid #e0e0e0;
    }
    
    /* Chat input area */
    .stChatInputContainer {
        background: white;
        border: 2px solid #000000;
        border-radius: 16px;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #000000;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Input text */
    .stChatInputContainer input {
        font-size: 1rem;
        border: none !important;
        padding: 8px 4px;
        color: #1a1a1a;
    }
    
    .stChatInputContainer input::placeholder {
        color: #999999;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Sidebar section headers */
    [data-testid="stSidebar"] h3 {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.2rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        padding-bottom: 0.5rem;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p {
        color: #d0d0d0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Buttons - Black & White elegant */
    .stButton > button {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        color: white;
        border: 2px solid #000000;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 28px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-color: #ffffff;
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Sidebar buttons - White on black */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #ffffff 0%, #e8e8e8 100%);
        color: #000000;
        border: 2px solid #ffffff;
        box-shadow: 0 6px 16px rgba(255,255,255,0.2);
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        color: #ffffff;
        border-color: #ffffff;
        box-shadow: 0 10px 28px rgba(0,0,0,0.5);
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        border-left: 4px solid #ffffff;
        border-radius: 8px;
        padding: 12px;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Info message */
    .stInfo {
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
        border-left: 4px solid #000000;
        border-radius: 8px;
        padding: 12px;
        color: #1a1a1a;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Divider */
    hr {
        border: none;
        background: linear-gradient(90deg, transparent, rgba(0,0,0,0.3), transparent);
        height: 2px;
        margin: 1.5rem 0;
    }
    
    /* Status badge */
    .status-badge {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Links */
    a {
        color: #000000;
        text-decoration: none;
        font-weight: 700;
        transition: color 0.3s ease;
        border-bottom: 2px solid #000000;
    }
    
    a:hover {
        color: #2d2d2d;
        border-bottom-color: #2d2d2d;
    }
    
    /* Markdown text */
    [data-testid="stMarkdownContainer"] {
        color: #1a1a1a;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    
    /* Header card background */
    .header-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%);
        border: 2px solid #000000;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    
    /* Elegant spacing */
    .spacer {
        height: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    '<div style="padding: 24px; background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%); border: 2px solid #000000; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); margin-bottom: 2rem;">'
    '<h1 style="margin: 0; padding: 0; text-align: center;">💳 HBDB Banking Bot</h1>'
    '<p class="subtitle" style="margin: 12px 0 0 0; color: #2d2d2d; text-align: center; font-weight: 600; letter-spacing: 0.5px;">Your Professional 24/7 Banking Assistant</p>'
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

# Display all chat messages with custom emoji avatars
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
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
    st.markdown("### � About This Bot")
    st.markdown(
        "Advanced banking assistant powered by **Mistral AI**. Get instant answers to all your HBDB banking questions 24/7."
    )
    
    st.markdown("---")
    
    st.markdown("### ❔ Quick Questions")
    
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
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        st.markdown(
            '<span style="display: flex; align-items: center; justify-content: center; padding: 8px; background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); color: white; border: 1px solid #ffffff; border-radius: 8px; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">● Ready</span>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    st.markdown(
        "<p style='text-align: center; color: #a0a0a0; font-size: 0.85rem; line-height: 1.6;'>"
        "<strong>🏦 Professional Banking<br/>Assistant</strong><br/>"
        "Powered by Advanced AI<br/>"
        "© 2026 HBDB"
        "</p>",
        unsafe_allow_html=True
    )


