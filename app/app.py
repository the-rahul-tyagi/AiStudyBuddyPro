# ====================== IMPORTS ======================
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime, timedelta
import json
import time
import base64
from PIL import Image
import io
import pdfkit
import random

# Import database manager
try:
    from database import db_manager
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from database import db_manager

# ====================== CONFIGURATION ======================
# Load environment variables
load_dotenv()

# Initialize database once
@st.cache_resource
def init_database():
    db_manager.init_db()

init_database()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env file!")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Try to use the best available model
try:
    # Try gemini-2.5-flash first (newest)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
except:
    try:
        # Fallback to gemini-1.5-flash
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
    except:
        try:
            # Fallback to gemini-pro
            model = genai.GenerativeModel(
                model_name="gemini-pro",
                generation_config=generation_config,
                safety_settings=safety_settings
            )
        except:
            # Last resort - use whatever is available
            model = genai.GenerativeModel(
                model_name="models/gemini-1.5-flash",
                generation_config=generation_config,
                safety_settings=safety_settings
            )

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ====================== GAMIFICATION SETUP ======================
# Badge definitions
BADGES = {
    "fast_learner": {"name": "Fast Learner", "desc": "Completed 5 study sessions in one day", "icon": "⚡", "points": 50},
    "streak_master": {"name": "Streak Master", "desc": "7-day study streak", "icon": "🔥", "points": 100},
    "quiz_champ": {"name": "Quiz Champ", "desc": "Scored 100% on a practice test", "icon": "🏆", "points": 75},
    "material_explorer": {"name": "Material Explorer", "desc": "Viewed all types of study materials", "icon": "🔍", "points": 40},
    "flashcard_pro": {"name": "Flashcard Pro", "desc": "Reviewed 50 flashcards", "icon": "🎴", "points": 60},
    "early_bird": {"name": "Early Bird", "desc": "Studied before 8 AM", "icon": "🌅", "points": 30},
    "night_owl": {"name": "Night Owl", "desc": "Studied after 10 PM", "icon": "🌙", "points": 30},
    "perfect_week": {"name": "Perfect Week", "desc": "Studied every day for a week", "icon": "🌟", "points": 150},
}

# Helper to save stats back to DB
def save_stats():
    """Helper to save gamification state to DB"""
    db_manager.save_gamification_state(st.session_state.gamification)

# Initialize gamification state
if "gamification" not in st.session_state:
    st.session_state.gamification = db_manager.get_gamification_state()

# ====================== HELPER FUNCTIONS ======================
def update_streak():
    """Update study streak based on last study date"""
    today = datetime.now().date()
    last_date = st.session_state.gamification["last_study_date"]
    
    if last_date:
        if today == last_date:
            return  # Already studied today
        
        if today == last_date + timedelta(days=1):
            st.session_state.gamification["streak"] += 1
            st.session_state.gamification["perfect_days"] += 1
        else:
            st.session_state.gamification["streak"] = 1
            st.session_state.gamification["perfect_days"] = 1
    else:
        st.session_state.gamification["streak"] = 1
        st.session_state.gamification["perfect_days"] = 1
    
    st.session_state.gamification["last_study_date"] = today
    check_streak_badges()
    save_stats()

def check_streak_badges():
    """Check if user earned any streak-related badges"""
    streak = st.session_state.gamification["streak"]
    perfect_days = st.session_state.gamification["perfect_days"]
    
    if streak >= 7 and "streak_master" not in st.session_state.gamification["badges"]:
        award_badge("streak_master")
    
    if perfect_days >= 7 and "perfect_week" not in st.session_state.gamification["badges"]:
        award_badge("perfect_week")

def award_points(points):
    """Award points to user"""
    st.session_state.gamification["points"] += points
    
    # Update leaderboard
    for entry in st.session_state.gamification["leaderboard"]:
        if entry["name"] == "You":
            entry["points"] = st.session_state.gamification["points"]
            break
    
    # Sort leaderboard
    st.session_state.gamification["leaderboard"].sort(key=lambda x: x["points"], reverse=True)
    save_stats()

def award_badge(badge_id):
    """Award a badge to the user"""
    if badge_id not in st.session_state.gamification["badges"]:
        st.session_state.gamification["badges"].append(badge_id)
        badge = BADGES[badge_id]
        award_points(badge["points"])
        st.toast(f"🎉 You earned the {badge['name']} badge! {badge['icon']} (+{badge['points']} points)", icon="🎖️")
        save_stats()

def check_time_based_badges():
    """Check for time-based badges (early bird/night owl)"""
    now = datetime.now().time()
    morning = datetime.strptime("08:00:00", "%H:%M:%S").time()
    night = datetime.strptime("22:00:00", "%H:%M:%S").time()
    
    if now < morning and "early_bird" not in st.session_state.gamification["badges"]:
        award_badge("early_bird")
    elif now > night and "night_owl" not in st.session_state.gamification["badges"]:
        award_badge("night_owl")

def check_study_session_badges():
    """Check for study session related badges"""
    sessions_today = st.session_state.gamification["study_sessions_today"]
    if sessions_today >= 5 and "fast_learner" not in st.session_state.gamification["badges"]:
        award_badge("fast_learner")

def check_flashcard_badges():
    """Check for flashcard related badges"""
    if st.session_state.gamification["flashcards_reviewed"] >= 50 and "flashcard_pro" not in st.session_state.gamification["badges"]:
        award_badge("flashcard_pro")

def generate_study_materials(topic, level, style, goals):
    """Generate personalized study materials"""
    # Gamification - track study session
    st.session_state.gamification["study_sessions_today"] += 1
    award_points(10)
    update_streak()
    check_study_session_badges()
    check_time_based_badges()
    
    prompt = f"""
    You are an expert tutor creating personalized study materials for a student.
    
    Student Profile:
    - Subject/Topic: {topic}
    - Education Level: {level}
    - Learning Style: {style}
    - Study Goals: {goals}
    
    Create comprehensive study materials that:
    1. Cover key concepts in an organized manner.
    2. Are tailored to the specified learning style.
    3. Include examples and explanations.
    4. Address the student's specific goals.
    
    Formatting Guidelines for Professional Presentation:
    - Organize with clear heading levels (e.g. # Header 1, ## Header 2).
    - Bold key definitions and terms upon first mention.
    - Present comparisons, lists, or parameters in Markdown Tables (`| Header 1 | Header 2 |`) for clear structured readability.
    - Place important takeaways or concepts inside Markdown Blockquotes (`> **Key Concept:** ...`).
    - Use lists with bullet points (`- Item`) for step-by-step procedures.
    - If code or formulas are required, use standard markdown syntax highlighting block format (e.g. ```python ... ``` or LaTeX).
    - Provide a concise summary or checklist at the end.
    """
    response = st.session_state.chat_session.send_message(prompt)
    return response.text

def generate_practice_test(topic, level, style, goals):
    """Generate a customized practice test"""
    # Gamification - track study session
    st.session_state.gamification["study_sessions_today"] += 1
    award_points(15)
    update_streak()
    st.session_state.gamification["last_study_date"] = datetime.now().date()
    check_study_session_badges()
    check_time_based_badges()
    
    prompt = f"""
    Create a personalized practice test based on:
    - Subject/Topic: {topic}
    - Education Level: {level}
    - Learning Style: {style}
    - Study Goals: {goals}
    
    Include:
    1. 5-10 varied questions (multiple choice, short answer, problem-solving).
    2. Clear instructions at the beginning.
    3. Appropriate difficulty level.
    4. Answer key with detailed explanations at the end.
    
    Formatting Guidelines:
    - Organize the test clearly into sections (e.g., ## Section 1: Multiple Choice, ## Section 2: Written Response).
    - Highlight key terms or problem variables in bold.
    - Format code snippets or mathematical expressions cleanly.
    - Keep the answer key separate at the bottom under a clear divider.
    """
    response = st.session_state.chat_session.send_message(prompt)
    return response.text

def evaluate_answers(question, answer):
    """Evaluate user's answers and provide feedback"""
    # Gamification - award points for answering questions
    award_points(5)
    
    prompt = f"""
    Evaluate the following answer to the question:
    
    Question: {question}
    Answer: {answer}
    
    Provide your evaluation in a highly structured layout with these sections:
    
    ### 📊 Evaluation Result
    - **Accuracy:** [Specify: Correct / Partially Correct / Incorrect]
    
    ### 📝 Detailed Feedback
    [Your detailed feedback assessing the student's answer, explaining what is right/wrong.]
    
    ### 💡 Suggestions for Improvement
    [Actionable, specific points on how the student can improve this answer next time.]
    
    ### 🔍 Additional Concept Explanation
    [Provide a brief, clean explanation of the underlying concept to reinforce learning.]
    
    Be constructive, supportive, and extremely clear. Use markdown bolding, list bullets, or quotes where appropriate.
    """
    response = st.session_state.chat_session.send_message(prompt)
    
    # Check for perfect score badge
    if "100%" in response.text.lower() or "perfect" in response.text.lower():
        if "quiz_champ" not in st.session_state.gamification["badges"]:
            award_badge("quiz_champ")
    
    return response.text

def parse_flashcards(content):
    """Parse flashcard content into front/back pairs"""
    cards = []
    current_card = {}
    
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith(('Front:', 'front:')):
            if current_card:
                cards.append(current_card)
            current_card = {'front': line.replace('Front:', '').replace('front:', '').strip()}
        elif line.strip().startswith(('Back:', 'back:')):
            current_card['back'] = line.replace('Back:', '').replace('back:', '').strip()
        elif line.strip() and 'front' in current_card and 'back' not in current_card:
            current_card['front'] += '\n' + line.strip()
        elif line.strip() and 'back' in current_card:
            current_card['back'] += '\n' + line.strip()
    
    if current_card:
        cards.append(current_card)
    
    return cards

def generate_pdf(content):
    """Generate PDF from content"""
    try:
        return pdfkit.from_string(content, False)
    except:
        # Fallback if pdfkit not properly configured
        return content.encode('utf-8')

# ====================== STREAMLIT UI ======================
# App configuration
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with gamification elements and enhanced modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    :root {
        --font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        --bg-dark: #05070f;
        --bg-slate: #0b0f19;
        --bg-card: rgba(13, 20, 38, 0.65);
        --border-color: rgba(255, 255, 255, 0.06);
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --primary: #818cf8;
        --primary-glow: rgba(129, 140, 248, 0.25);
        --accent-purple: #c084fc;
        --accent-pink: #d946ef;
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #d946ef 100%);
        --gradient-success: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        --gradient-warning: linear-gradient(135deg, #f59e0b 0%, #ec4899 100%);
        --gradient-info: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        --transition-smooth: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Ambient Glowing Blobs in Background with live float animations */
    @keyframes floatBlob1 {
        0% { transform: translate(0px, 0px) scale(1); }
        33% { transform: translate(40px, -60px) scale(1.1); }
        66% { transform: translate(-20px, 30px) scale(0.9); }
        100% { transform: translate(0px, 0px) scale(1); }
    }

    @keyframes floatBlob2 {
        0% { transform: translate(0px, 0px) scale(1); }
        50% { transform: translate(-60px, 50px) scale(1.15); }
        100% { transform: translate(0px, 0px) scale(1); }
    }

    @keyframes floatBlob3 {
        0% { transform: translate(0px, 0px) scale(1); }
        50% { transform: translate(50px, -40px) scale(0.95); }
        100% { transform: translate(0px, 0px) scale(1); }
    }

    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 5%;
        left: 10%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.22) 0%, rgba(0, 0, 0, 0) 70%);
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
        animation: floatBlob1 20s infinite ease-in-out;
    }

    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: absolute;
        bottom: 15%;
        right: 10%;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, rgba(217, 70, 239, 0.16) 0%, rgba(0, 0, 0, 0) 70%);
        filter: blur(100px);
        pointer-events: none;
        z-index: 0;
        animation: floatBlob2 25s infinite ease-in-out;
    }

    .main::before {
        content: "";
        position: absolute;
        top: 40%;
        right: 20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.15) 0%, rgba(0, 0, 0, 0) 70%);
        filter: blur(90px);
        pointer-events: none;
        z-index: 0;
        animation: floatBlob3 22s infinite ease-in-out;
    }

    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: var(--font-family) !important;
        background-color: var(--bg-dark) !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.25) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(217, 70, 239, 0.2) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(6, 182, 212, 0.15) 0px, transparent 50%) !important;
        background-attachment: fixed !important;
        color: var(--text-main) !important;
    }

    /* Header background to match */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Sidebar container and design */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #03050c 0%, #090e1a 100%) !important;
        border-right: 1px solid var(--border-color) !important;
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.5) !important;
    }

    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] label {
        color: var(--text-main) !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: var(--border-color) !important;
    }

    [data-testid="stSidebar"] .stExpander {
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        background: rgba(13, 20, 38, 0.6) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
        margin-bottom: 1.2rem;
    }

    [data-testid="stSidebar"] .stExpander > details > summary {
        font-weight: 700;
        font-size: 1rem;
        color: var(--text-main) !important;
        padding: 0.8rem !important;
    }

    /* Streamlit custom inputs in general */
    input[type="text"], textarea, select, div[data-baseweb="select"] > div {
        background-color: rgba(13, 20, 38, 0.7) !important;
        color: var(--text-main) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        transition: var(--transition-smooth) !important;
    }

    input[type="text"]:focus, textarea:focus, select:focus, div[data-baseweb="select"] > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-glow) !important;
    }

    /* Premium Button styling with glowing shadows */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        transition: var(--transition-smooth) !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.3) !important;
        cursor: pointer !important;
        width: 100% !important;
        letter-spacing: 0.5px !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 25px rgba(217, 70, 239, 0.45) !important;
        border-color: rgba(255, 255, 255, 0.35) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* Chat messages bubble design */
    .chat-message {
        padding: 1.25rem;
        border-radius: 20px;
        margin-bottom: 1.25rem;
        font-size: 0.98rem;
        line-height: 1.6;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: var(--transition-smooth);
        animation: slideUp 0.4s ease-out;
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-message {
        background: linear-gradient(135deg, #4f46e5 0%, #d946ef 100%) !important;
        color: white !important;
        margin-left: 12%;
        border-radius: 20px 20px 4px 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.25) !important;
    }

    .ai-message {
        background: rgba(13, 20, 38, 0.75) !important;
        color: var(--text-main) !important;
        margin-right: 12%;
        border-radius: 20px 20px 20px 4px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-left: 4px solid var(--accent-pink) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
    }

    /* Feature cards on dashboard */
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0) 100%), rgba(13, 20, 38, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin-bottom: 1.5rem !important;
        transition: var(--transition-smooth) !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.15) !important;
        position: relative;
        overflow: hidden;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
        border-radius: 20px 20px 0 0;
    }

    .feature-card:hover {
        transform: translateY(-8px) scale(1.01) !important;
        box-shadow: 0 20px 40px rgba(168, 85, 247, 0.28), inset 0 1px 1px rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(168, 85, 247, 0.5) !important;
    }

    .feature-card h4 {
        color: var(--primary);
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .feature-card p {
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }

    /* Badge cards styling */
    .badge-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0) 100%), rgba(13, 20, 38, 0.7) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 20px !important;
        padding: 1.4rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.12) !important;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        transition: var(--transition-smooth) !important;
    }

    .badge-card:hover {
        border-color: var(--accent-purple) !important;
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 16px 32px rgba(217, 70, 239, 0.28), inset 0 1px 1px rgba(255, 255, 255, 0.22) !important;
    }

    .badge-icon {
        font-size: 2.5rem;
        flex-shrink: 0;
    }

    .badge-info {
        flex-grow: 1;
    }

    .badge-title {
        color: var(--text-main);
        font-weight: 700;
        margin: 0;
        font-size: 1rem;
    }

    .badge-description {
        color: var(--text-muted);
        font-size: 0.85rem;
        margin: 0.3rem 0 0 0;
    }

    /* Points and streak badge display */
    .points-display {
        background: var(--gradient-primary);
        color: white;
        padding: 0.7rem 1.4rem;
        border-radius: 50px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.3);
        font-size: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .streak-display {
        background: linear-gradient(135deg, #f59e0b, #ec4899);
        color: white;
        padding: 0.7rem 1.4rem;
        border-radius: 50px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.35);
        font-size: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Leaderboard container and elements */
    .leaderboard-entry {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.1rem;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        transition: var(--transition-smooth) !important;
        background: rgba(13, 20, 38, 0.45) !important;
        margin-bottom: 0.75rem;
    }

    .leaderboard-entry:hover {
        background: rgba(22, 28, 45, 0.65) !important;
        transform: translateX(8px) !important;
        border-color: rgba(168, 85, 247, 0.45) !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.15) !important;
    }

    .leaderboard-you {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.3) 0%, rgba(217, 70, 239, 0.15) 100%) !important;
        border: 1px solid rgba(217, 70, 239, 0.5) !important;
        font-weight: 700;
        padding-left: 1.2rem !important;
        box-shadow: 0 4px 20px rgba(217, 70, 239, 0.2) !important;
    }

    /* Progress bar */
    .xp-bar {
        height: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        margin: 1rem 0;
        overflow: hidden;
    }

    .xp-progress {
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 10px;
        box-shadow: 0 0 12px rgba(217, 70, 239, 0.6);
    }

    /* 3D Flashcard Design */
    .flashcard-container {
        perspective: 1200px;
        margin: 2.5rem auto;
        width: 100%;
        max-width: 600px;
    }

    .flashcard {
        position: relative;
        width: 100%;
        height: 330px;
        transform-style: preserve-3d;
        transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border-radius: 24px;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.5);
        cursor: pointer;
    }

    .flashcard:hover {
        box-shadow: 0 25px 50px rgba(168, 85, 247, 0.3);
    }

    .flashcard.flipped {
        transform: rotateY(180deg);
    }

    .flashcard-face {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 2.5rem;
        box-sizing: border-box;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }

    .flashcard-front {
        background: linear-gradient(135deg, #0f1026 0%, #3b145a 60%, #701a75 100%) !important;
        color: var(--text-main);
        transform: rotateY(0deg);
        box-shadow: inset 0 2px 20px rgba(255, 255, 255, 0.05);
    }

    .flashcard-back {
        background: linear-gradient(135deg, #011c16 0%, #043e2e 60%, #065f46 100%) !important;
        color: var(--text-main);
        transform: rotateY(180deg);
        box-shadow: inset 0 2px 20px rgba(255, 255, 255, 0.05);
    }

    .flashcard-content {
        font-size: 1.25rem;
        text-align: center;
        overflow-y: auto;
        max-height: 85%;
        width: 100%;
        line-height: 1.6;
        font-weight: 500;
    }

    /* Flashcard controls */
    .flashcard-nav-btn {
        background: var(--gradient-primary);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 0.8rem 1.8rem;
        border-radius: 12px;
        font-size: 0.95rem;
        cursor: pointer;
        font-weight: 600;
        transition: var(--transition-smooth);
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.25);
    }

    .flashcard-nav-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(217, 70, 239, 0.45);
    }

    .flashcard-progress {
        width: 100%;
        max-width: 600px;
        margin: 1.5rem auto;
    }

    .flashcard-set-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: var(--bg-card);
        border-radius: 20px;
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }

    .flashcard-actions {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }

    .flashcard-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid var(--border-color);
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        margin: 0.4rem;
        font-weight: 600;
        color: var(--text-main);
        transition: var(--transition-smooth);
    }

    .flashcard-tag:hover {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
        transform: scale(1.05);
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 4px;
        transition: var(--transition-smooth);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }

    /* Streamlit Custom Tab design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem;
        border-bottom: 1px solid var(--border-color) !important;
        padding: 0.5rem 1rem;
        background: rgba(13, 20, 38, 0.45) !important;
        border-radius: 14px !important;
        margin-bottom: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem !important;
        border-radius: 10px !important;
        background: transparent !important;
        border: none !important;
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        transition: var(--transition-smooth) !important;
        font-size: 0.95rem !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-main) !important;
        background: rgba(255, 255, 255, 0.02) !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--gradient-primary) !important;
        color: white !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4) !important;
    }

    /* Streamlit Expander styling overrides */
    .streamlit-expanderHeader {
        border-radius: 14px !important;
        background: rgba(13, 20, 38, 0.6) !important;
        border: 1px solid var(--border-color) !important;
        transition: var(--transition-smooth) !important;
        padding: 1rem 1.25rem !important;
        font-weight: 600 !important;
        color: var(--text-main) !important;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(22, 28, 45, 0.8) !important;
        border-color: var(--primary) !important;
        box-shadow: 0 4px 20px var(--primary-glow) !important;
    }

    .streamlit-expanderContent {
        border-radius: 0 0 14px 14px !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        background: rgba(13, 20, 38, 0.4) !important;
        padding: 1.5rem !important;
        color: var(--text-main) !important;
    }

    /* Radiant multi-color text gradients for title headings */
    h1, h2, h3 {
        background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 30%, #c084fc 70%, #d946ef 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 800 !important;
        letter-spacing: -0.3px;
    }

    h1 {
        font-size: 2.7rem !important;
        margin-bottom: 1.5rem !important;
    }

    h2 {
        font-size: 1.95rem !important;
        margin-bottom: 1.1rem !important;
    }

    h3 {
        font-size: 1.45rem !important;
        margin-bottom: 0.9rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.8rem; margin: 0;">
            ⚙️ Setup
        </h2>
        <p style="color: var(--text-muted); font-size: 0.95rem; margin-top: 0.4rem;">
            Personalize your study path
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Study Subject (Primary focus so we pull it up top for ease of use)
    st.markdown("<p style='color: var(--text-main); font-weight: 600; margin-bottom: 0.2rem;'>🎯 Core Topic</p>", unsafe_allow_html=True)
    study_subject = st.text_input(
        "Subject/Topic",
        value="Python Programming",
        placeholder="e.g., Calculus, Biology...",
        label_visibility="collapsed",
        help="What do you want to learn today?"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Simplified Gamification widget
    with st.expander("🏆 **Your Stats**", expanded=True):
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; text-align: center; background: rgba(17, 24, 39, 0.5); padding: 0.8rem; border-radius: 12px; border: 1px solid var(--border-color); box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
            <div>
                <strong style="background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.2rem;">{st.session_state.gamification["points"]} XP</strong><br>
                <small style="color: var(--text-muted);">Score</small>
            </div>
            <div style="border-left: 1px solid var(--border-color);"></div>
            <div>
                <strong style="color: #ef4444; font-size: 1.2rem;">{st.session_state.gamification["streak"]} 🔥</strong><br>
                <small style="color: var(--text-muted);">Streak</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        level = st.session_state.gamification["points"] // 100
        xp_progress = st.session_state.gamification["points"] % 100
        st.markdown(f"""
        <div style="margin-top: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                <small style="color: var(--text-main); font-weight: 600;">Level {level + 1}</small>
                <small style="color: var(--text-muted);">{xp_progress}/100 XP to Level {level + 2}</small>
            </div>
            <div style="height: 8px; background: rgba(255, 255, 255, 0.05); border-radius: 4px; overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);">
                <div style="width: {xp_progress}%; height: 100%; background: var(--gradient-primary); border-radius: 4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📋 **Learning Profile**", expanded=False):
        st.markdown("<small style='color: var(--text-muted);'>Customize how AI teaches you</small>", unsafe_allow_html=True)
        
        education_level = st.selectbox(
            "Education Level",
            ["High School", "Undergraduate", "Graduate", "Professional"],
            index=1,
            help="Adapts the complexity of the materials."
        )
        
        learning_style = st.selectbox(
            "Learning Style",
            ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Mixed"],
            index=0,
            help="Tailors how information is presented."
        )
        
        response_length = st.select_slider(
            "Response Detail",
            ["Concise", "Balanced", "Detailed"],
            "Balanced"
        )
        
        study_goals = st.text_area(
            "Specific Objectives",
            height=68,
            placeholder="e.g., Master loops for my final exam...",
            help="Any specific goals to steer the content generation?"
        )

    with st.expander("📈 **Proficiency Tracking**", expanded=False):
        proficiency_level = st.slider("Current Level (1-10)", 1, 10, 5, help="Where are you currently at?")
        target_proficiency = st.slider("Target Level (1-10)", 1, 10, 8, help="Where do you want to be?")
        
        progress_percent = min(100, int((proficiency_level / target_proficiency) * 100)) if target_proficiency > 0 else 0
        st.markdown(f"""
        <div style="margin-top: 0.5rem;">
            <small style="color: var(--text-muted); font-weight: 600;">Goal Progress: {progress_percent}%</small>
            <div style="height: 6px; background: rgba(255, 255, 255, 0.05); border-radius: 3px; overflow: hidden; margin-top: 0.2rem;">
                <div style="width: {progress_percent}%; height: 100%; background: var(--gradient-success); border-radius: 3px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: var(--text-muted); font-weight: 600; font-size: 0.85rem; margin-bottom: 0.5rem; letter-spacing: 0.5px;'>ACTIONS</p>", unsafe_allow_html=True)
    
    col_btn_1, col_btn_2 = st.columns(2, gap="small")
    with col_btn_1:
        if st.button("🧹 Clear Chat", use_container_width=True, help="Wipes the current AI conversation history."):
            st.session_state.chat_session = model.start_chat(history=[])
            st.toast("✅ Chat history cleared!", icon="🧹")
            st.rerun()
    with col_btn_2:
        if st.button("🔄 Reset Stats", use_container_width=True, help="Resets gamification points and streaks back to zero."):
            db_manager.reset_stats('You')
            st.session_state.gamification = db_manager.get_gamification_state('You')
            st.toast("✅ Stats reset!", icon="🔄")
            st.rerun()

    if st.button("🗑️ Clear All Generated Content", use_container_width=True, help="Removes all generated quizzes, study guides, and flashcards."):
        db_manager.clear_generated_content('You')
        st.session_state.study_materials = []
        st.session_state.practice_tests = []
        st.session_state.flashcards = []
        st.session_state.study_plan = None
        st.toast("🗑️ All generated content cleared!", icon="🗑️")
        st.rerun()
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1.2rem; 
                background: rgba(17, 24, 39, 0.45);
                border-radius: 12px; border: 1px solid var(--border-color);">
        <small style="color: var(--text-main); font-weight: 700; font-size: 0.95rem;">
            📱 AI Study Buddy
        </small>
        <div style="margin-top: 0.5rem;">
            <span style="background: var(--primary-glow); color: var(--primary); padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; border: 1px solid rgba(99, 102, 241, 0.25);">
                Gemini Powered
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====================== MAIN CONTENT ======================
# Initialize session state
if "study_materials" not in st.session_state:
    st.session_state.study_materials = db_manager.get_study_materials('You')
if "practice_tests" not in st.session_state:
    st.session_state.practice_tests = db_manager.get_practice_tests('You')
if "flashcards" not in st.session_state:
    st.session_state.flashcards = db_manager.get_flashcards('You')
if "study_plan" not in st.session_state:
    st.session_state.study_plan = None

# App header with enhanced styling
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem; font-weight: 800; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🧠 AI Study Buddy</h1>
    <p style="font-size: 1.3rem; color: var(--text-muted); font-weight: 500; margin: 0;">
        Your <strong style="color: var(--primary);">Personalized Learning Assistant</strong> Powered by AI
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(6, 182, 212, 0.15)); 
            border: 1px solid rgba(99, 102, 241, 0.3); padding: 2rem; border-radius: 20px; 
            margin-bottom: 2.5rem; backdrop-filter: blur(10px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);">
    <h3 style="color: var(--text-main); margin-top: 0; font-size: 1.3rem;">✨ Welcome to Your Learning Journey</h3>
    <p style="color: var(--text-muted); font-size: 1.05rem; margin: 0; line-height: 1.6;">
        Adapt your study approach to <strong>your unique needs</strong> with personalized content, 
        adaptive tests, and intelligent feedback powered by advanced AI technology.
    </p>
</div>
""", unsafe_allow_html=True)

# Enhanced Feature cards
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    with st.container():
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem; text-align: center;">📖</div>
            <h4 style="margin: 0 0 0.75rem 0; color: var(--primary);">Smart Study Materials</h4>
            <p style="margin: 0; color: var(--text-muted); font-size: 0.95rem; line-height: 1.5;">
                Get AI-generated customized content tailored to your learning style, education level, and specific goals.
            </p>
        </div>
        """, unsafe_allow_html=True)
with col2:
    with st.container():
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem; text-align: center;">✍️</div>
            <h4 style="margin: 0 0 0.75rem 0; color: var(--primary);">Adaptive Practice Tests</h4>
            <p style="margin: 0; color: var(--text-muted); font-size: 0.95rem; line-height: 1.5;">
                Generate MCQ tests with varying difficulty levels that match your current knowledge and adapt to your progress.
            </p>
        </div>
        """, unsafe_allow_html=True)
with col3:
    with st.container():
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem; text-align: center;">🗂️</div>
            <h4 style="margin: 0 0 0.75rem 0; color: var(--primary);">Interactive Flashcards</h4>
            <p style="margin: 0; color: var(--text-muted); font-size: 0.95rem; line-height: 1.5;">
                Create and review beautiful 3D flip cards with shuffle, restart, and progress tracking features.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Dashboard", 
    "📖 Study Materials", 
    "✍️ Practice Tests", 
    "🗂️ Flashcards", 
    "💬 Tutor Chat",
    "🏆 Gamification"
])

# ====================== DASHBOARD TAB ======================
with tab1:
    st.markdown("### 🚀 Quick Start")
    
    if not study_subject or study_subject.strip() == "":
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.1) 100%); 
                    border-left: 4px solid var(--primary); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid rgba(99, 102, 241, 0.25);">
            <p style="margin: 0; color: var(--text-main); font-weight: 600; font-size: 1.05rem;">
                👋 Welcome! Enter a topic in the sidebar to get started, or use our quick preset below.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Try One of These Popular Topics:")
        col1, col2, col3 = st.columns(3)
        
        quick_topics = {
            "Python": col1,
            "Biology": col2, 
            "History": col3
        }
        
        for topic, col in quick_topics.items():
            with col:
                if st.button(f"📚 Learn {topic}", key=f"quick_{topic}", use_container_width=True):
                    st.session_state.sidebar_subject = topic
                    st.rerun()
    else:
        st.markdown(f"""
        <div style="background: var(--gradient-primary); color: white; 
                    padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.35); border: 1px solid rgba(255, 255, 255, 0.1);">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.8rem; color: white !important;">📚 {study_subject}</h3>
            <p style="margin: 0; opacity: 0.95; font-size: 0.95rem; color: #e2e8f0 !important;">
                Level: <strong>{education_level}</strong> • Style: <strong>{learning_style}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### ⚡ One-Click Learning:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📖 Generate Study Guide", use_container_width=True, key="quick_materials"):
                st.session_state.active_tab = "materials"
                st.rerun()
        
        with col2:
            if st.button("✍️ Take Quick Quiz", use_container_width=True, key="quick_test"):
                st.session_state.active_tab = "tests"
                st.rerun()
        
        with col3:
            if st.button("🗂️ Make Flashcards", use_container_width=True, key="quick_cards"):
                st.session_state.active_tab = "cards"
                st.rerun()
    
    if study_subject and study_subject.strip() != "":
        st.divider()
        st.markdown("### 📊 Your Progress")
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown(f"""
            <div style="background: var(--bg-card); border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 16px; text-align: center; backdrop-filter: blur(8px); box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                <div style="font-size: 2.2rem; font-weight: 800; color: #6366f1; margin-bottom: 0.5rem;">{proficiency_level}/10</div>
                <div style="font-size: 0.9rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Current Level</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: var(--bg-card); border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 16px; text-align: center; backdrop-filter: blur(8px); box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                <div style="font-size: 2.2rem; font-weight: 800; color: #a855f7; margin-bottom: 0.5rem;">{target_proficiency}/10</div>
                <div style="font-size: 0.9rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Target Level</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            progress_percent = min(100, int((proficiency_level / target_proficiency) * 100)) if target_proficiency > 0 else 0
            st.markdown(f"""
            <div style="background: var(--bg-card); border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 16px; text-align: center; backdrop-filter: blur(8px); box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                <div style="font-size: 2.2rem; font-weight: 800; color: #10b981; margin-bottom: 0.5rem;">{progress_percent}%</div>
                <div style="font-size: 0.9rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Progress</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("#### 💡 Study Tips")
        st.markdown("1. Start with study materials to build foundational knowledge")
        st.markdown("2. Practice tests help identify weak areas")
        st.markdown("3. Flashcards are great for memorization and review")
        st.markdown("4. Use the tutor chat for in-depth explanations")
 
# ====================== STUDY MATERIALS TAB ======================
with tab2:
    st.markdown("""
    <div style="background: var(--gradient-primary); color: white; 
                padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3); border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="margin: 0; font-size: 2.2rem; color: white !important;">📖 Personalized Study Materials</h2>
        <p style="margin: 0.5rem 0 0 0; color: rgba(248, 250, 252, 0.9) !important; font-size: 1.05rem;">
            AI-generated content tailored to your learning style and goals
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if study_subject:
        with st.expander("🛠️ **Generate New Materials**", expanded=True):
            col1, col2 = st.columns(2, gap="large")
            with col1:
                material_type = st.selectbox(
                    "📝 Material Type",
                    ["Comprehensive Guide", "Summary Sheet", "Concept Map", "Cheat Sheet"],
                    label_visibility="collapsed"
                )
            with col2:
                detail_level = st.select_slider(
                    "📊 Detail Level",
                    ["Overview", "Standard", "In-Depth"],
                    label_visibility="collapsed"
                )
            
            if st.button("✨ Generate Materials", use_container_width=True):
                with st.spinner(f"🎨 Creating {material_type}..."):
                    materials = generate_study_materials(
                        study_subject, education_level, learning_style, study_goals
                    )
                    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                    db_manager.save_study_material('You', material_type, study_subject, materials)
                    st.session_state.study_materials.append({
                        "timestamp": timestamp_str,
                        "type": material_type,
                        "content": materials
                    })
                    st.success("✅ Materials generated!")
                    st.rerun()
        
        if st.session_state.study_materials:
            latest = st.session_state.study_materials[-1]
            st.markdown(f"""
            <div style="background: rgba(17, 24, 39, 0.5); 
                        border-left: 4px solid var(--primary) !important; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                        border: 1px solid var(--border-color); border-left: 4px solid var(--primary) !important;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: var(--primary) !important; font-size: 1.3rem;">📄 {latest['type']}</h3>
                        <small style="color: var(--text-muted);">Generated at {latest['timestamp']}</small>
                    </div>
                    <div style="font-size: 2rem;">📚</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📝 **View Content**", expanded=True):
                st.markdown(f"""
                <div style="background: rgba(17, 24, 39, 0.35); padding: 1.5rem; border-radius: 12px; 
                            border: 1px solid var(--border-color); line-height: 1.8; color: var(--text-main) !important;">
                {latest["content"]}
                </div>
                """, unsafe_allow_html=True)
            
            # Export options
            st.markdown("### 📥 Export & Share")
            export_col1, export_col2, export_col3 = st.columns(3, gap="large")
            with export_col1:
                st.download_button(
                    label="📄 Download as Text",
                    data=latest["content"],
                    file_name=f"{study_subject}_{latest['type'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with export_col2:
                st.download_button(
                    label="📑 Download as Markdown",
                    data=latest["content"],
                    file_name=f"{study_subject}_{latest['type'].replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with export_col3:
                st.download_button(
                    label="📑 Download as PDF",
                    data=generate_pdf(latest["content"]),
                    file_name=f"{study_subject}_{latest['type'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(17, 24, 39, 0.45);
                    border-radius: 20px; border: 2px dashed var(--primary); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);">
            <h3 style="color: var(--primary) !important; margin-bottom: 1rem;">📚 Select a Subject First</h3>
            <p style="color: var(--text-muted); font-size: 1.1rem; margin: 0;">
                Enter a subject/topic in the sidebar to generate personalized study materials.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ====================== PRACTICE TESTS TAB ======================
with tab3:
    st.header("✍️ MCQ Practice Tests")
    
    if study_subject:
        with st.expander("🛠️ Create New Test", expanded=True):
            num_questions = st.number_input(
                "Number of Questions",
                min_value=1,
                max_value=20,
                value=5,
                step=1
            )
            
            difficulty = st.select_slider(
                "Difficulty Level",
                options=["Basic", "Intermediate", "Advanced"],
                value="Intermediate"
            )
            
            if st.button("Generate MCQ Test"):
                with st.spinner(f"Creating {num_questions} MCQ questions..."):
                    prompt = f"""
                    Create a multiple choice practice test with these specifications:
                    - Subject/Topic: {study_subject}
                    - Number of Questions: {num_questions}
                    - Question Type: Multiple Choice Only (MCQs)
                    - Difficulty Level: {difficulty}
                    - Education Level: {education_level}
                    - Learning Style: {learning_style}
                    
                    Format requirements:
                    1. Start with '### MCQ Test:' header
                    2. For each question:
                       - Start with '#### Q{{number}}:' followed by the question text
                       - Provide exactly 4 options labeled a), b), c), d)
                       - Mark the correct answer with '[CORRECT]' after the option
                       - Include a brief explanation after each question, labeled 'Explanation:'
                    3. End with '### Answer Key:' section listing all correct answers
                    """
                    response = st.session_state.chat_session.send_message(prompt)
                    test_content = response.text
                    
                    new_test = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "num_questions": num_questions,
                        "difficulty": difficulty,
                        "content": test_content,
                        "user_answers": {},
                        "submitted": False,
                        "show_answers": False
                    }
                    db_manager.save_practice_test('You', study_subject, new_test)
                    st.session_state.practice_tests.append(new_test)
                    st.session_state.current_test = len(st.session_state.practice_tests) - 1
                    st.rerun()
        
        # Handle test display and submission
        if "current_test" not in st.session_state or st.session_state.current_test is None:
            if st.session_state.practice_tests:
                st.info("Select a test from the list below:")
                test_labels = [f"Test {i+1} ({t['num_questions']} questions, {t['difficulty']})" 
                             for i, t in enumerate(st.session_state.practice_tests)]
                selected_test = st.selectbox("Available Tests", test_labels)
                if st.button("Load Selected Test"):
                    st.session_state.current_test = test_labels.index(selected_test)
                    st.rerun()
            else:
                st.info("No tests available. Generate a new test above.")
        else:
            current_test = st.session_state.practice_tests[st.session_state.current_test]
            
            st.subheader(f"{current_test['num_questions']} MCQ Questions ({current_test['difficulty']})")
            
            if not current_test["submitted"]:
                if "### MCQ Test:" in current_test["content"]:
                    questions_section = current_test["content"].split("### MCQ Test:")[1].split("### Answer Key:")[0]
                    questions = [q.strip() for q in questions_section.split("#### Q") if q.strip()]
                    
                    for i, question in enumerate(questions):
                        question_num = i + 1
                        q_text = question.split("\n")[0]
                        options_section = question.split("\n")[1:] if "\n" in question else []
                        
                        st.markdown(f"#### Q{question_num}: {q_text}")
                        
                        options = []
                        correct_option = None
                        explanation = ""
                        
                        for line in options_section:
                            if line.startswith(("a)", "b)", "c)", "d)")):
                                opt_text = line[2:].strip()
                                if "[CORRECT]" in opt_text:
                                    correct_option = line[0]
                                    opt_text = opt_text.replace("[CORRECT]", "").strip()
                                options.append(opt_text)
                            elif line.startswith("Explanation:"):
                                explanation = line.replace("Explanation:", "").strip()
                        
                        current_test[f"q{question_num}_correct"] = correct_option
                        current_test[f"q{question_num}_explanation"] = explanation
                        
                        user_answer = st.radio(
                            f"Select answer for Q{question_num}",
                            options,
                            key=f"q{question_num}_{st.session_state.current_test}",
                            index=None
                        )
                        
                        if user_answer:
                            current_test["user_answers"][f"q{question_num}"] = chr(97 + options.index(user_answer))
                
                if st.button("Submit Test"):
                    current_test["submitted"] = True
                    st.session_state.gamification["study_sessions_today"] += 1
                    award_points(10 + current_test["num_questions"])  # More points for longer tests
                    update_streak()
                    db_manager.save_practice_test('You', study_subject, current_test)
                    st.rerun()
            
            # In the Practice Tests tab (tab3), replace the evaluation section with this:

            else:
                st.success("✅ Test Submitted!")
                
                total_questions = current_test["num_questions"]
                correct_answers = 0
                
                for q_num in range(1, total_questions + 1):
                    q_key = f"q{q_num}"
                    user_answer = current_test["user_answers"].get(q_key)
                    correct_answer = current_test.get(f"{q_key}_correct")
                    explanation = current_test.get(f"{q_key}_explanation", "No explanation provided.")
                    
                    st.markdown(f"#### Q{q_num}:")
                    
                    if user_answer is None:
                        st.warning("⚠️ Not answered")
                        st.markdown(f"**Correct answer:** {correct_answer.upper() if correct_answer else 'Unknown'}")
                    elif correct_answer is None:
                        st.error("❌ Error: Could not determine correct answer")
                    elif user_answer == correct_answer:
                        correct_answers += 1
                        st.success(f"✅ Your answer: {user_answer.upper()} (Correct)")
                    else:
                        st.error(f"❌ Your answer: {user_answer.upper()} (Incorrect)")
                        st.markdown(f"**Correct answer:** {correct_answer.upper() if correct_answer else 'Unknown'}")
                    
                    with st.expander("View Explanation"):
                        st.markdown(explanation)
                
                score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
                
                if score == 100:
                    st.balloons()
                    award_badge("quiz_champ")
                    award_points(50) # Bonus for perfect score
                elif score >= 90:
                    award_badge("test_ace")
                    award_points(25) # Bonus for high score
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; 
                            padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem;">
                    <h3 style="color: white;">Your Score: {score:.2f}%</h3>
                    <p style="margin: 0;">You answered {correct_answers} out of {total_questions} questions correctly.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Try Another Test"):
                    st.session_state.current_test = None
                    st.rerun()
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(6, 182, 212, 0.05));
                    border-radius: 20px; border: 2px dashed #6366f1;">
            <h3 style="color: #6366f1; margin-bottom: 1rem;">✍️ Select a Subject First</h3>
            <p style="color: #64748b; font-size: 1.1rem; margin: 0;">
                Enter a subject/topic in the sidebar to generate practice tests.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ====================== FLASHCARDS TAB ======================
with tab4:
    st.header("🗂️ Interactive Flashcards", anchor="flashcards")
    
    if study_subject:
        with st.expander("✨ Create New Flashcard Set", expanded=True):
            st.markdown("### 🛠️ Create New Set")
            col1, col2 = st.columns(2)
            with col1:
                flashcard_count = st.slider(
                    "Number of Flashcards", 
                    5, 30, 10,
                    help="Choose how many flashcards to generate"
                )
            with col2:
                flashcard_focus = st.selectbox(
                    "Focus Area",
                    ["Key Terms", "Important Concepts", "Formulas", "Dates & Events", "Mixed"],
                    help="Select the type of content for your flashcards"
                )
            
            if st.button("🎨 Generate Flashcards", use_container_width=True):
                with st.spinner(f"✨ Creating {flashcard_count} {flashcard_focus.lower()} flashcards..."):
                    prompt = f"""
                    Create a set of {flashcard_count} high-quality flashcards for {study_subject} at {education_level} level.
                    Focus area: {flashcard_focus}.
                    Current proficiency: {proficiency_level}/10.
                    Preferred learning style: {learning_style}.
                    
                    Format each flashcard EXACTLY as follows:
                    
                    Front: [The question or term goes here]
                    Back: [The definition or explanation goes here]
                    
                    [Optional additional information about this card]
                    
                    Front: [Next question]
                    Back: [Next answer]
                    
                    Important guidelines:
                    1. Keep front content concise (1-2 lines)
                    2. Back content can be more detailed
                    3. Use clear, simple language
                    4. Include examples where helpful
                    5. Ensure each flashcard has both Front and Back sections
                    """
                    response = st.session_state.chat_session.send_message(prompt)
                    new_set = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "count": flashcard_count,
                        "focus": flashcard_focus,
                        "content": response.text,
                        "srs_data": {}
                    }
                    db_manager.save_flashcard('You', study_subject, new_set)
                    st.session_state.flashcards.append(new_set)
                    st.session_state.current_flashcard_set = len(st.session_state.flashcards) - 1
                    st.rerun()
        
        if st.session_state.flashcards:
            if "current_flashcard_set" not in st.session_state:
                st.session_state.current_flashcard_set = len(st.session_state.flashcards) - 1
            
            # Flashcard set selector with improved styling
            st.markdown("---")
            st.markdown("### 📚 Your Flashcard Sets")
            flash_select = st.selectbox(
                "Select a set to review",
                [f"Set {i+1} ({f.get('count', 10)} cards, {f.get('focus', 'General')}) - {f['timestamp']}" 
                 for i, f in enumerate(st.session_state.flashcards)],
                index=st.session_state.current_flashcard_set,
                label_visibility="collapsed"
            )
            
            st.session_state.current_flashcard_set = int(flash_select.split(" ")[1]) - 1
            selected_flashcards = st.session_state.flashcards[st.session_state.current_flashcard_set]
            
            # Flashcard set header with metadata
            st.markdown(f"""
            <div class="flashcard-set-header">
                <h3>📖 {selected_flashcards.get('focus', 'General')} Flashcards</h3>
                <div>
                    <span class="flashcard-tag">✏️ {selected_flashcards.get('count', 10)} cards</span>
                    <span class="flashcard-tag">⏱️ {selected_flashcards['timestamp']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive flashcard display
            if "current_card" not in st.session_state:
                st.session_state.current_card = 0
                st.session_state.show_answer = False
            
            cards = parse_flashcards(selected_flashcards["content"])
            if cards:
                total_cards = len(cards)
                current_idx = st.session_state.current_card % total_cards
                current_card = cards[current_idx]
                
                # Animated flashcard
                st.markdown(f"""
                <div class="flashcard-container">
                    <div class="flashcard {'flipped' if st.session_state.show_answer else ''}" 
                         onclick="this.classList.toggle('flipped')">
                        <div class="flashcard-face flashcard-front">
                            <div class="flashcard-content">
                                <h3 style="color: white;">{current_card['front']}</h3>
                                <p style="opacity: 0.8;">(Click to flip)</p>
                            </div>
                        </div>
                        <div class="flashcard-face flashcard-back">
                            <div class="flashcard-content">
                                <p>{current_card['back']}</p>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Navigation buttons with better styling
                col1, col2, col3 = st.columns([1,2,1])
                with col1:
                    if st.button("⬅️ Previous", key="flash_prev", use_container_width=True):
                        st.session_state.current_card = (st.session_state.current_card - 1) % total_cards
                        st.session_state.show_answer = False
                        st.rerun()
                with col2:
                    if st.button("🔁 Flip Card", key="flash_flip", use_container_width=True):
                        st.session_state.show_answer = not st.session_state.show_answer
                        st.rerun()
                with col3:
                    if st.button("Next ➡️", key="flash_next", use_container_width=True):
                        st.session_state.current_card = (st.session_state.current_card + 1) % total_cards
                        st.session_state.show_answer = False
                        st.session_state.gamification["flashcards_reviewed"] += 1
                        award_points(2)
                        check_flashcard_badges()
                        st.rerun()
                
                # Enhanced progress indicator
                progress = (current_idx + 1) / total_cards
                st.markdown(f"""
                <div class="flashcard-progress">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <small>Card {current_idx + 1} of {total_cards}</small>
                        <small>{int(progress * 100)}% Complete</small>
                    </div>
                    <div style="height: 8px; background-color: rgba(255, 255, 255, 0.05); border-radius: 4px;">
                        <div style="height: 100%; width: {progress * 100}%; 
                                    background: var(--gradient-primary); 
                                    border-radius: 4px; transition: width 0.3s ease;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Additional actions
                st.markdown("---")
                st.markdown("### 🔧 Flashcard Actions")
                action_col1, action_col2, action_col3 = st.columns(3)
                with action_col1:
                    if st.button("🔄 Restart Set", help="Start reviewing from the first card", use_container_width=True):
                        st.session_state.current_card = 0
                        st.session_state.show_answer = False
                        st.rerun()
                with action_col2:
                    if st.button("🎲 Shuffle", help="Randomize the card order", use_container_width=True):
                        random.shuffle(cards)
                        selected_flashcards["content"] = "\n".join([f"Front: {c['front']}\nBack: {c['back']}" for c in cards])
                        st.session_state.current_card = 0
                        st.session_state.show_answer = False
                        st.rerun()
                with action_col3:
                    if st.button("🗑️ Delete Set", help="Remove this flashcard set", use_container_width=True):
                        st.session_state.flashcards.pop(st.session_state.current_flashcard_set)
                        st.session_state.current_flashcard_set = None
                        st.session_state.current_card = 0
                        st.rerun()
            else:
                st.error("No flashcards could be parsed from this set. Please try generating a new set.")
    else:
        st.info("📚 Please enter a subject/topic in the sidebar to generate flashcards.")

# ====================== TUTOR CHAT TAB ======================
with tab5:
    st.header("💬 Interactive Tutor Chat")
    st.markdown("""
    <div style="background-color: rgba(17, 24, 39, 0.45); padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid var(--border-color);">
        <p style="margin: 0; color: var(--text-muted);">Ask specific questions about your study topic for personalized explanations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat session specifically for tutor chat
    if "tutor_chat_session" not in st.session_state:
        st.session_state.tutor_chat_session = model.start_chat(history=[])
    
    # Display only tutor chat history
    for message in st.session_state.tutor_chat_session.history:
        role = "You" if message.role == "user" else "Tutor"
        css_class = "user-message" if role == "You" else "ai-message"
        avatar = "👤" if role == "You" else "🧠"
        
        with st.container():
            st.markdown(f"""
            <div class="chat-message {css_class}">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">{avatar}</span>
                    <strong>{role}</strong>
                </div>
                {message.parts[0].text}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input with enhanced features
    with st.form("tutor_chat_input_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Ask your study question here...",
                placeholder="Type your question or upload an image of a problem",
                key="tutor_chat_input",
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Send", use_container_width=True)
        
        # File uploader for images/documents
        uploaded_file = st.file_uploader(
            "Upload image/document (optional)",
            type=["png", "jpg", "jpeg", "pdf"],
            key="tutor_file_uploader",
            label_visibility="collapsed"
        )
    
    if (submitted and user_input) or uploaded_file:
        # Add user message to chat
        with st.container():
            content = user_input if user_input else f"Uploaded file: {uploaded_file.name}"
            st.markdown(f"""
            <div class="chat-message user-message">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">👤</span>
                    <strong>You</strong>
                </div>
                {content}
            </div>
            """, unsafe_allow_html=True)
        
        # Get AI response
        with st.spinner("Tutor is thinking..."):
            if uploaded_file:
                # Handle file upload
                if uploaded_file.type.startswith('image'):
                    image = Image.open(uploaded_file)
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    prompt = "Please analyze this image and help me with the problem or concept shown."
                    response = st.session_state.tutor_chat_session.send_message(
                        [prompt, {"mime_type": "image/png", "data": img_byte_arr}]
                    )
                else:
                    # For PDFs
                    import pypdf
                    try:
                        pdf_reader = pypdf.PdfReader(uploaded_file)
                        text = ""
                        for page in pdf_reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        if not text.strip():
                            text = "[No text extractable from this PDF (it might be a scanned image or contain no selectable text)]"
                    except Exception as e:
                        text = f"[Error reading PDF file: {e}]"
                    
                    user_q = user_input if user_input else "Summarize this document and explain the key concepts."
                    prompt = f"""
You are a helpful tutor analyzing an uploaded PDF document.

Document Name: {uploaded_file.name}

--- DOCUMENT CONTENT ---
{text}
--- END DOCUMENT CONTENT ---

User Question: {user_q}

Please answer the user's question based on the document content above. If the document content is empty or unreadable, guide the student on how to proceed.
"""
                    response = st.session_state.tutor_chat_session.send_message(prompt)
            else:
                response = st.session_state.tutor_chat_session.send_message(user_input)
            
            # Display AI response
            with st.container():
                st.markdown(f"""
                <div class="chat-message ai-message">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">🧠</span>
                        <strong>Tutor</strong>
                    </div>
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("🧹 Clear Tutor Chat History", use_container_width=True):
        st.session_state.tutor_chat_session = model.start_chat(history=[])
        st.rerun()
# ====================== GAMIFICATION TAB ======================
with tab6:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f59e0b 0%, #ec4899 100%); color: white; 
                padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(245, 158, 11, 0.25); border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="margin: 0; font-size: 2.2rem; color: white !important;">🏆 Your Learning Journey</h2>
        <p style="margin: 0.5rem 0 0 0; color: rgba(248, 250, 252, 0.9) !important; font-size: 1.05rem;">
            Track achievements, badges, and compete on the leaderboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("### 🎖️ Your Badges")
        if not st.session_state.gamification["badges"]:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(17, 24, 39, 0.45);
                        border-radius: 15px; border: 2px dashed var(--primary); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);">
                <p style="color: var(--text-muted); font-size: 1.05rem; margin: 0;">
                    🌱 You haven't earned any badges yet.<br>
                    Keep studying to unlock amazing achievements!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            badge_cols = st.columns(2, gap="large")
            for idx, badge_id in enumerate(st.session_state.gamification["badges"]):
                badge = BADGES[badge_id]
                with badge_cols[idx % 2]:
                    st.markdown(f"""
                    <div class="badge-card">
                        <div class="badge-icon">{badge['icon']}</div>
                        <div class="badge-info">
                            <strong style="color: var(--primary) !important; font-size: 1.1rem; display: block;">{badge['name']}</strong>
                            <p style="margin: 0.3rem 0; color: var(--text-muted) !important; font-size: 0.9rem;">{badge['desc']}</p>
                            <small style="color: var(--primary) !important; font-weight: 700;">+{badge['points']} XP</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("### 📊 Detailed Statistics")
        stats_col1, stats_col2 = st.columns(2, gap="large")
        
        with stats_col1:
            st.markdown(f"""
            <div style="background: var(--gradient-primary); color: white; 
                        padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);">
                <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: white !important;">
                    {st.session_state.gamification["study_sessions_today"]}
                </div>
                <div style="font-size: 0.95rem; opacity: 0.9; color: #f1f5f9 !important;">Study Sessions Today</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_col2:
            st.markdown(f"""
            <div style="background: var(--gradient-info); color: white; 
                        padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(6, 182, 212, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);">
                <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: white !important;">
                    {st.session_state.gamification["flashcards_reviewed"]}
                </div>
                <div style="font-size: 0.95rem; opacity: 0.9; color: #f1f5f9 !important;">Flashcards Reviewed</div>
            </div>
            """, unsafe_allow_html=True)
        
        stats_col3, stats_col4 = st.columns(2, gap="large")
        
        with stats_col3:
            st.markdown(f"""
            <div style="background: var(--gradient-warning); color: white; 
                        padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);">
                <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: white !important;">
                    {st.session_state.gamification["streak"]} 🔥
                </div>
                <div style="font-size: 0.95rem; opacity: 0.9; color: #f1f5f9 !important;">Day Streak</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_col4:
            st.markdown(f"""
            <div style="background: var(--gradient-success); color: white; 
                        padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);">
                <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: white !important;">
                    {st.session_state.gamification["perfect_days"]}/7
                </div>
                <div style="font-size: 0.95rem; opacity: 0.9; color: #f1f5f9 !important;">Perfect Days This Week</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🏅 Leaderboard")
        st.markdown("<small style='color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Top Learners This Week</small>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(17, 24, 39, 0.45); 
                    border-radius: 16px; padding: 1.5rem; border: 1px solid var(--border-color);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);">
        """, unsafe_allow_html=True)
        
        for i, entry in enumerate(st.session_state.gamification["leaderboard"]):
            is_you = entry["name"] == "You"
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
            
            st.markdown(f"""
            <div class="leaderboard-entry {'leaderboard-you' if is_you else ''}">
                <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span style="font-size: 1.5rem; font-weight: 700;">{medal}</span>
                        <span style="font-weight: 600; color: {'var(--primary)' if is_you else 'var(--text-main)'};">{entry['name']}</span>
                    </div>
                    <div style="font-weight: 700; color: var(--primary); font-size: 1.05rem;">{entry['points']} XP</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("### 🔜 Next Badges")
        st.markdown("<small style='color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Earn These Next</small>", unsafe_allow_html=True)
        
        available_badges = [b for b in BADGES if b not in st.session_state.gamification["badges"]]
        if available_badges:
            sample_badges = random.sample(available_badges, min(2, len(available_badges)))
            for badge_id in sample_badges:
                badge = BADGES[badge_id]
                st.markdown(f"""
                <div style="background: rgba(17, 24, 39, 0.45); 
                            padding: 1rem; border-radius: 12px; margin-bottom: 0.75rem; 
                            border-left: 3px solid var(--primary) !important; border: 1px solid var(--border-color); border-left: 3px solid var(--primary) !important;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span style="font-size: 1.5rem;">{badge['icon']}</span>
                        <div style="flex-grow: 1;">
                            <strong style="color: var(--primary); display: block;">{badge['name']}</strong>
                            <small style="color: var(--text-muted);">{badge['desc']}</small>
                        </div>
                        <span style="font-weight: 700; color: var(--primary); white-space: nowrap;">+{badge['points']} XP</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 You've earned all available badges! You're a learning superstar!")

# ====================== FOOTER ======================
st.divider()
st.markdown("""
<div style="text-align: center; padding: 2.5rem 1rem; 
            background: rgba(17, 24, 39, 0.45);
            border-radius: 16px; margin-top: 2rem; border: 1px solid var(--border-color); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);">
    <h4 style="color: var(--primary); margin-bottom: 0.75rem; font-size: 1.1rem;">✨ AI Study Buddy</h4>
    <p style="color: var(--text-muted); margin: 0.5rem 0; font-size: 0.95rem;">
        Advanced Learning Platform Powered by Gemini 2.5 Flash
    </p>
    <p style="color: #94a3b8; margin: 0.5rem 0; font-size: 0.85rem;">
        v2.0 • © 2026 Learning Technologies • Designed for Modern Students
    </p>
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
        <small style="color: #94a3b8;">
            🚀 Combining AI Intelligence with Interactive Learning
        </small>
    </div>
</div>
""", unsafe_allow_html=True)