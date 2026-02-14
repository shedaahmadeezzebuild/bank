import streamlit as st
from banking_bot import BankingBot
import os
from datetime import datetime

# ============================================================================
# PAGE CONFIG - Must be first Streamlit command
# ============================================================================
st.set_page_config(
    page_title="HBDB Banking - Digital Banking Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL FINTECH CSS STYLING
# ============================================================================
st.markdown("""
<style>
/* ===== ROOT VARIABLES ===== */
:root {
    --primary-dark: #0B1C2D;
    --primary: #1E3A5F;
    --accent-gold: #C6A14A;
    --accent-blue: #1E88E5;
    --bg-light: #F5F7FA;
    --bg-white: #FFFFFF;
    --text-dark: #1A2A3A;
    --text-secondary: #6B7B8F;
    --border-light: #E8EAED;
    --success: #10B981;
}

/* ===== GLOBAL STYLES ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebarContent"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    letter-spacing: 0.4px;
}

/* ===== MAIN CONTAINER ===== */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #F5F7FA 0%, #F0F2F5 100%);
}

/* ===== SIDEBAR - PROFESSIONAL BANKING NAV ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1C2D 0%, #0F2438 100%) !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF;
}

/* Sidebar logo area */
.sidebar-logo {
    padding: 2rem 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    text-align: center;
    background: rgba(0,0,0,0.2);
}

.sidebar-logo h2 {
    font-size: 1.4rem;
    font-weight: 700;
    color: #C6A14A;
    margin: 0;
    letter-spacing: 0.5px;
}

.sidebar-logo p {
    font-size: 0.75rem;
    color: #9CAFC0;
    margin-top: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Navigation menu items */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #C8D3E0 !important;
    border: none !important;
    border-left: 3px solid transparent;
    border-radius: 0 !important;
    padding: 1rem 1.5rem !important;
    width: 100% !important;
    text-align: left !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    font-size: 0.95rem !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(198, 161, 74, 0.1) !important;
    color: #C6A14A !important;
    border-left-color: #C6A14A !important;
    padding-left: 1.8rem !important;
}

/* ===== SECTION HEADERS IN SIDEBAR ===== */
[data-testid="stSidebar"] h3 {
    color: #9CAFC0;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
    padding: 0 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding-top: 1.5rem;
}

/* ===== TOP HEADER BAR ===== */
.header-bar {
    background: #FFFFFF;
    border-bottom: 1px solid var(--border-light);
    padding: 1.2rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-bottom: 2rem;
    border-radius: 0;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.header-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--primary-dark);
    margin: 0;
}

.header-subtitle {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin: 0;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.secure-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(16, 185, 129, 0.1);
    color: var(--success);
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

/* ===== CHAT INTERFACE ===== */
.chat-container {
    background: var(--bg-white);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
    min-height: 500px;
}

/* ===== MESSAGE BUBBLES ===== */
.message-wrapper {
    display: flex;
    margin-bottom: 1.5rem;
    animation: fadeInMessage 0.4s ease-in;
}

@keyframes fadeInMessage {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message-wrapper.user {
    justify-content: flex-end;
}

.message-wrapper.assistant {
    justify-content: flex-start;
}

/* Avatar styling */
.message-avatar {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
    margin: 0 0.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.message-avatar.user {
    background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
    order: 2;
}

.message-avatar.assistant {
    background: linear-gradient(135deg, #0B1C2D 0%, #1E3A5F 100%);
    order: 1;
}

/* Message bubble */
.message-bubble {
    max-width: 60%;
    padding: 1rem 1.25rem;
    border-radius: 12px;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    word-wrap: break-word;
}

.message-bubble.user {
    background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
    color: #FFFFFF;
    border-radius: 12px 2px 12px 12px;
}

.message-bubble.assistant {
    background: var(--bg-white);
    color: var(--text-dark);
    border: 1px solid var(--border-light);
    border-radius: 2px 12px 12px 12px;
}

/* Message content */
.message-content {
    font-size: 0.95rem;
    line-height: 1.6;
}

.message-meta {
    font-size: 0.75rem;
    margin-top: 0.5rem;
    opacity: 0.7;
}

.message-bubble.user .message-meta {
    color: rgba(255,255,255,0.8);
}

.message-bubble.assistant .message-meta {
    color: var(--text-secondary);
}

/* ===== TYPING INDICATOR ===== */
@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-8px); }
}

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 1rem 1.25rem;
    background: var(--bg-light);
    border-radius: 12px;
    width: fit-content;
}

.typing-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--text-secondary);
    animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

/* ===== BUTTON STYLING ===== */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-gold) 0%, #B8963F 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(198, 161, 74, 0.2) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(198, 161, 74, 0.3) !important;
    background: linear-gradient(135deg, #D4B257 0%, #C6A14A 100%) !important;
}

/* ===== QUICK QUESTIONS ===== */
.quick-questions-section {
    margin-top: 2rem;
    border-top: 1px solid var(--border-light);
    padding-top: 2rem;
}

/* ===== TYPOGRAPHY ===== */
h1, h2, h3, h4, h5, h6 {
    color: var(--primary-dark) !important;
    font-weight: 700 !important;
}

p, span, div {
    color: var(--text-dark);
}

[data-testid="stMarkdownContainer"] {
    color: var(--text-dark) !important;
}

[data-testid="stMarkdownContainer"] a {
    color: var(--accent-blue) !important;
    text-decoration: none !important;
}

[data-testid="stMarkdownContainer"] a:hover {
    color: #1565C0 !important;
}

/* ===== DIVIDERS ===== */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--border-light) 20%, var(--border-light) 80%, transparent) !important;
    margin: 1.5rem 0 !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(11, 28, 45, 0.2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(11, 28, 45, 0.4);
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 768px) {
    .message-bubble {
        max-width: 85%;
    }
    
    .header-bar {
        flex-wrap: wrap;
        gap: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================================
# API KEY MANAGEMENT
# ============================================================================
api_key = None

# Try environment variable
api_key = os.getenv("MISTRAL_API_KEY")

# Try Streamlit secrets
if not api_key:
    try:
        api_key = st.secrets.get("MISTRAL_API_KEY")
    except:
        pass

# Fallback for testing
if not api_key:
    api_key = "hKjvYtwfSKR7Ysd7WKvmItCtPL6YfjdR"

# Check CSV file
csv_path = "hbdb_banking_faqs (2) (1).csv"
if not os.path.exists(csv_path):
    st.error(f"CSV file not found: {csv_path}")
    st.stop()

# ============================================================================
# BOT INITIALIZATION
# ============================================================================
@st.cache_resource
def init_bot():
    try:
        bot = BankingBot(api_key=api_key, csv_path=csv_path)
        return bot
    except Exception as e:
        st.error(f"Failed to initialize bot: {str(e)}")
        st.stop()

bot = init_bot()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "response_needed" not in st.session_state:
    st.session_state.response_needed = False

if "show_typing" not in st.session_state:
    st.session_state.show_typing = False

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    # Logo Section
    st.markdown("""
    <div class="sidebar-logo">
        <h2>HBDB</h2>
        <p>Banking Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Navigation Menu
    st.markdown("<h3>Main Menu</h3>", unsafe_allow_html=True)
    
    nav_items = [
        ("Dashboard", "dashboard"),
        ("Accounts", "accounts"),
        ("Loans", "loans"),
        ("Cards", "cards"),
        ("Support", "support")
    ]
    
    for label, key in nav_items:
        st.button(label, key=f"nav_{key}", use_container_width=True)
    
    st.markdown("")
    st.markdown("<h3>Assistance</h3>", unsafe_allow_html=True)
    st.button("Chat with Assistant", key="nav_chat", use_container_width=True)
    
    st.markdown("")
    
    # Quick Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear", key="btn_clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        st.markdown(
            '<div style="display: flex; align-items: center; justify-content: center; padding: 0.75rem; background: rgba(16,185,129,0.15); color: #10B981; border-radius: 10px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(16,185,129,0.3);">STATUS: ONLINE</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("")
    
    # Footer Info
    st.markdown(
        """
        <p style='text-align: center; color: #9CAFC0; font-size: 0.8rem; line-height: 1.5; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);'>
            <strong>HBDB Digital Banking</strong><br/>
            Secure &bull; Fast &bull; Reliable<br/>
            2026
        </p>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Header Bar
st.markdown("""
<div class="header-bar">
    <div class="header-left">
        <div>
            <h2 class="header-title">Banking Assistant</h2>
            <p class="header-subtitle">Get instant answers to your banking questions</p>
        </div>
    </div>
    <div class="header-right">
        <div class="secure-badge">
            Secure Session
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display Messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", "")
    
    if role == "user":
        st.markdown(f"""
        <div class="message-wrapper user">
            <div class="message-avatar user">👤</div>
            <div class="message-bubble user">
                <div class="message-content">{content}</div>
                <div class="message-meta">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-wrapper assistant">
            <div class="message-avatar assistant">👨‍💼</div>
            <div class="message-bubble assistant">
                <div class="message-content">{content}</div>
                <div class="message-meta">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Show typing indicator if needed
if st.session_state.show_typing:
    st.markdown("""
    <div class="message-wrapper assistant">
        <div class="message-avatar assistant">👨‍💼</div>
        <div class="typing-indicator">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Check if response is needed
def needs_response():
    if not st.session_state.messages:
        return False
    return st.session_state.messages[-1]["role"] == "user"

# Generate response
if needs_response():
    st.session_state.show_typing = True
    st.rerun()

if st.session_state.show_typing and len(st.session_state.messages) > 0:
    user_message = st.session_state.messages[-1]["content"]
    
    full_response = ""
    try:
        for chunk in bot.get_response(user_message):
            if chunk:
                full_response += chunk
        
        if full_response:
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "timestamp": timestamp
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "I apologize, I could not generate a response at this time.",
                "timestamp": datetime.now().strftime("%H:%M")
            })
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"An error occurred: {str(e)}",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    st.session_state.show_typing = False
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Input Area
user_input = st.chat_input("Type your question here...")

if user_input:
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    st.rerun()

# ============================================================================
# QUICK QUESTIONS SECTION
# ============================================================================
st.markdown("---")
st.markdown("""
<div class="quick-questions-section">
    <h3 style='margin-bottom: 1.5rem;'>Suggested Questions</h3>
</div>
""", unsafe_allow_html=True)

questions = [
    "How do I open a savings account?",
    "What is HBDB Premier?",
    "How do I reset my password?",
    "What are the interest rates?",
    "How do I apply for a loan?"
]

cols = st.columns(len(questions))
for idx, (col, question) in enumerate(zip(cols, questions)):
    with col:
        if st.button(question, key=f"quick_q_{idx}", use_container_width=True):
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                "role": "user",
                "content": question,
                "timestamp": timestamp
            })
            st.rerun()
