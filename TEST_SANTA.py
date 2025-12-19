import streamlit as st
import time
import os
from datetime import datetime

st.set_page_config(page_title="🎅 Secret Santa 🎄", layout="centered")

# ---- SESSION STATE ----
if "started" not in st.session_state:
    st.session_state.started = False

# ---- GLOBAL CSS ----
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #b30000, #006600);
    }

    /* Snowflakes */
    .snowflake {
        color: #fff;
        font-size: 1em;
        position: fixed;
        top: -10%;
        z-index: 9999;
        user-select: none;
        animation: fall linear infinite;
    }
    @keyframes fall {
        0% { transform: translateY(0); }
        100% { transform: translateY(110vh); }
    }

    /* Box opening animation */
    .gift-box {
        width: 300px;
        height: 200px;
        background: #ff3333;
        margin: 40px auto;
        border-radius: 12px;
        position: relative;
        animation: openBox 1.5s ease-out forwards;
    }
    .gift-box::before {
        content: '';
        position: absolute;
        top: -60px;
        left: 0;
        width: 100%;
        height: 60px;
        background: #cc0000;
        border-radius: 12px 12px 0 0;
        animation: lidOpen 1.5s ease-out forwards;
    }
    @keyframes openBox {
        0% { transform: scale(0.6); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    @keyframes lidOpen {
        0% { transform: rotateX(0deg); }
        100% { transform: rotateX(75deg) translateY(-20px); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Snowflakes ----
for i in range(25):
    st.markdown(
        f"<div class='snowflake' style='left:{i*4}%; animation-duration:{5+i%5}s'>❄️</div>",
        unsafe_allow_html=True
    )

# ---- Ensure log directory inside git repo (absolute path) ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(BASE_DIR, "secret_santa.log")
os.makedirs(LOG_DIR, exist_ok=True)

# ---- ENSURE LOG FILE EXISTS (touch file) ----
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")


# ---- DEBUG (optional): show where logs are written ----
# st.write("Logs will be written to:", LOG_FILE)

# ================= START PAGE =================
if not st.session_state.started:
    st.markdown("<h1 style='text-align:center;'>🎄 Welcome to Secret Santa 🎄</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px;'>Press the magic button to begin</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎁 START 🎁"):
            st.session_state.started = True
            st.rerun()

# ================= MAIN PAGE =================
if st.session_state.started:
    # Gift box opening animation
    st.markdown("<div class='gift-box'></div>", unsafe_allow_html=True)
    time.sleep(1)

    st.title("🎁 Secret Santa 🎁")
    st.subheader("Answer this to unlock your festive spirit 🎄")

    question = "What gift would make you smile this Christmas?"
    st.write(f"🎅 **Question:** {question}")

    answer = st.text_input("🎄 Your Answer")

    if st.button("Reveal Magic ✨") and answer:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_message = (
            f"[{timestamp}] | EVENT=SECRET_SANTA_RESPONSE | "
            f"QUESTION=\"{question}\" | ANSWER=\"{answer}\"\n"
        )

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_message)

        st.success("Ho Ho Ho! 🎅 Your answer has been safely sent to Santa 🎁")
        time.sleep(1)

    st.caption("❄️ Snow falling, Santa is watching...")

