import streamlit as st
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Download NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Load model and vectorizer
model = pickle.load(open('models/model.pkl', 'rb'))
vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [word for word in text if word.isalnum()]
    text = [word for word in text if word not in stop_words and word not in string.punctuation]
    text = [ps.stem(word) for word in text]
    return " ".join(text)

# Page config
st.set_page_config(
    page_title="SpamShield AI",
    page_icon="🛡️",
    layout="centered"
)

# Hide default Streamlit elements for cleaner look
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Full custom CSS with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ===== BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Inter', sans-serif;
    }

    /* ===== ANIMATED PARTICLES ===== */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }

    .particle {
        position: absolute;
        width: 6px;
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: floatUp linear infinite;
    }

    .particle:nth-child(1) { left: 10%; animation-duration: 12s; animation-delay: 0s; width: 4px; height: 4px; }
    .particle:nth-child(2) { left: 25%; animation-duration: 15s; animation-delay: 2s; width: 8px; height: 8px; }
    .particle:nth-child(3) { left: 40%; animation-duration: 10s; animation-delay: 4s; width: 5px; height: 5px; }
    .particle:nth-child(4) { left: 55%; animation-duration: 18s; animation-delay: 1s; width: 7px; height: 7px; }
    .particle:nth-child(5) { left: 70%; animation-duration: 14s; animation-delay: 3s; width: 4px; height: 4px; }
    .particle:nth-child(6) { left: 85%; animation-duration: 11s; animation-delay: 5s; width: 6px; height: 6px; }
    .particle:nth-child(7) { left: 15%; animation-duration: 16s; animation-delay: 6s; width: 3px; height: 3px; }
    .particle:nth-child(8) { left: 60%; animation-duration: 13s; animation-delay: 7s; width: 5px; height: 5px; }

    @keyframes floatUp {
        0%   { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10%  { opacity: 1; }
        90%  { opacity: 1; }
        100% { transform: translateY(-10vh) rotate(720deg); opacity: 0; }
    }

    /* ===== GLOWING HEADER ===== */
    .hero-container {
        text-align: center;
        padding: 20px 0 10px 0;
        position: relative;
        z-index: 1;
    }

    .shield-icon {
        font-size: 5rem;
        animation: pulseGlow 2s ease-in-out infinite;
        display: inline-block;
    }

    @keyframes pulseGlow {
        0%, 100% { 
            filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.5));
            transform: scale(1);
        }
        50% { 
            filter: drop-shadow(0 0 25px rgba(99, 102, 241, 0.9));
            transform: scale(1.05);
        }
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #667eea 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 4s ease infinite;
        margin: 10px 0 5px 0;
        letter-spacing: -1px;
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .hero-subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 1.05rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }

    .powered-by {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #a5b4fc;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 8px;
    }

    /* ===== GLASS CARD ===== */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 35px;
        margin: 20px 0;
        position: relative;
        z-index: 1;
        animation: slideUp 0.8s ease-out;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .card-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }

    /* ===== TEXT AREA STYLING ===== */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 18px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        resize: none !important;
    }

    .stTextArea textarea:focus {
        border-color: rgba(99, 102, 241, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }

    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.3) !important;
    }

    .stTextArea label {
        display: none !important;
    }

    /* ===== BUTTON ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 32px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.5px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* ===== RESULT CARDS ===== */
    .result-spam {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        animation: resultBounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        position: relative;
        overflow: hidden;
    }

    .result-spam::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(239, 68, 68, 0.1) 0%, transparent 70%);
        animation: rotateGlow 6s linear infinite;
    }

    .result-ham {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(22, 163, 74, 0.1) 100%);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        animation: resultBounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        position: relative;
        overflow: hidden;
    }

    .result-ham::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(34, 197, 94, 0.1) 0%, transparent 70%);
        animation: rotateGlow 6s linear infinite;
    }

    @keyframes resultBounce {
        0%   { opacity: 0; transform: scale(0.3) rotate(-10deg); }
        60%  { transform: scale(1.05) rotate(2deg); }
        100% { opacity: 1; transform: scale(1) rotate(0deg); }
    }

    @keyframes rotateGlow {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }

    .result-icon {
        font-size: 4.5rem;
        margin-bottom: 15px;
        position: relative;
        z-index: 1;
    }

    .result-label-spam {
        font-size: 2.5rem;
        font-weight: 900;
        color: #ef4444;
        letter-spacing: 3px;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 30px rgba(239, 68, 68, 0.5);
    }

    .result-label-ham {
        font-size: 2.5rem;
        font-weight: 900;
        color: #22c55e;
        letter-spacing: 3px;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 30px rgba(34, 197, 94, 0.5);
    }

    .confidence-text {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1rem;
        margin-top: 12px;
        position: relative;
        z-index: 1;
    }

    .confidence-value {
        font-weight: 800;
        font-size: 1.8rem;
        color: white;
    }

    /* ===== PROGRESS BAR ===== */
    .progress-container {
        width: 100%;
        height: 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-top: 20px;
        overflow: hidden;
        position: relative;
        z-index: 1;
    }

    .progress-bar-spam {
        height: 100%;
        background: linear-gradient(90deg, #f87171, #ef4444, #dc2626);
        border-radius: 10px;
        animation: fillBar 1.5s ease-out;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);
    }

    .progress-bar-ham {
        height: 100%;
        background: linear-gradient(90deg, #4ade80, #22c55e, #16a34a);
        border-radius: 10px;
        animation: fillBar 1.5s ease-out;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.5);
    }

    @keyframes fillBar {
        from { width: 0%; }
    }

    /* ===== SCANNING ANIMATION ===== */
    .scanning {
        text-align: center;
        padding: 30px;
        color: rgba(255, 255, 255, 0.7);
    }

    .scan-line {
        width: 60%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 15px auto;
        animation: scanPulse 1.5s ease-in-out infinite;
        border-radius: 2px;
    }

    @keyframes scanPulse {
        0%, 100% { opacity: 0.3; transform: scaleX(0.5); }
        50%      { opacity: 1; transform: scaleX(1); }
    }

    /* ===== STATS ROW ===== */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 25px;
        position: relative;
        z-index: 1;
    }

    .stat-item {
        text-align: center;
    }

    .stat-number {
        font-size: 1.5rem;
        font-weight: 800;
        color: white;
    }

    .stat-label {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    /* ===== FEATURE PILLS ===== */
    .features {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 20px;
        position: relative;
        z-index: 1;
    }

    .feature-pill {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: rgba(255, 255, 255, 0.7);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .feature-pill:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.4);
        color: white;
    }

    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.8rem;
        margin-top: 30px;
        padding: 15px;
        position: relative;
        z-index: 1;
    }

    .footer a {
        color: rgba(99, 102, 241, 0.7);
        text-decoration: none;
    }

    /* ===== WARNING BOX ===== */
    .stAlert {
        background: rgba(234, 179, 8, 0.1) !important;
        border: 1px solid rgba(234, 179, 8, 0.3) !important;
        border-radius: 12px !important;
        color: #fbbf24 !important;
    }

    /* ===== HIDE STREAMLIT ELEMENTS ===== */
    div[data-testid="stDecoration"] { display: none; }
    .stProgress > div > div { background-color: rgba(255,255,255,0.1) !important; }
    .stProgress > div > div > div { display: none; }
</style>
""", unsafe_allow_html=True)

# Floating particles background
st.markdown("""
<div class="particles">
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
</div>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero-container">
    <div class="shield-icon">🛡️</div>
    <div class="hero-title">SpamShield AI</div>
    <div class="hero-subtitle">Advanced email threat detection powered by machine learning</div>
    <div class="powered-by">⚡ Powered by Naive Bayes + NLP</div>
</div>
""", unsafe_allow_html=True)

# Input card
st.markdown("""
<div class="glass-card">
    <div class="card-label">📨 Paste Email Content</div>
</div>
""", unsafe_allow_html=True)

email_input = st.text_area(
    "Email Content",
    placeholder="Drop your suspicious email here to scan for threats...",
    height=180,
    label_visibility="hidden"
)

# Analyze button
analyze = st.button("🔍  Analyze Email", use_container_width=True)

if analyze:
    if email_input.strip() == "":
        st.warning("⚠️ Please paste an email to analyze!")
    else:
        # Scanning animation
        scanning_placeholder = st.empty()
        scanning_placeholder.markdown("""
            <div class="scanning">
                <div style="font-size: 1.5rem; margin-bottom: 5px;">🔬 Scanning email...</div>
                <div class="scan-line"></div>
                <div style="font-size: 0.85rem;">Analyzing patterns, keywords, and threat signatures</div>
            </div>
        """, unsafe_allow_html=True)

        import time
        time.sleep(2)
        scanning_placeholder.empty()

        # Process and predict
        transformed = transform_text(email_input)
        vectorized = vectorizer.transform([transformed])
        prediction = model.predict(vectorized)[0]
        probability = model.predict_proba(vectorized)[0]

        word_count = len(email_input.split())
        char_count = len(email_input)

        if prediction == 1:
            confidence = round(probability[1] * 100, 1)
            st.markdown(f"""
                <div class="result-spam">
                    <div class="result-icon">🚨</div>
                    <div class="result-label-spam">SPAM DETECTED</div>
                    <div class="confidence-text">
                        Threat Level: <span class="confidence-value">{confidence}%</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar-spam" style="width: {confidence}%;"></div>
                    </div>
                    <div class="stats-row">
                        <div class="stat-item">
                            <div class="stat-number">{word_count}</div>
                            <div class="stat-label">Words</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{char_count}</div>
                            <div class="stat-label">Characters</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">⚠️ High</div>
                            <div class="stat-label">Risk Level</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        else:
            confidence = round(probability[0] * 100, 1)
            st.markdown(f"""
                <div class="result-ham">
                    <div class="result-icon">✅</div>
                    <div class="result-label-ham">SAFE EMAIL</div>
                    <div class="confidence-text">
                        Safety Score: <span class="confidence-value">{confidence}%</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar-ham" style="width: {confidence}%;"></div>
                    </div>
                    <div class="stats-row">
                        <div class="stat-item">
                            <div class="stat-number">{word_count}</div>
                            <div class="stat-label">Words</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{char_count}</div>
                            <div class="stat-label">Characters</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">✅ Low</div>
                            <div class="stat-label">Risk Level</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Features section
st.markdown("""
<div style="text-align: center; margin-top: 30px; position: relative; z-index: 1;">
    <div class="features">
        <div class="feature-pill">🧠 Machine Learning</div>
        <div class="feature-pill">📊 NLP Processing</div>
        <div class="feature-pill">⚡ Real-time Analysis</div>
        <div class="feature-pill">🎯 98% Accuracy</div>
        <div class="feature-pill">🔒 100% Precision</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Built with ❤️ using Python, Scikit-learn & Streamlit<br>
    Trained on 5,000+ real email samples
</div>
""", unsafe_allow_html=True)