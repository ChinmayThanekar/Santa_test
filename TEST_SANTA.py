import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="🎅 Secret Santa 🎄", layout="centered")

# ---- Snow Animation CSS ----
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #b30000, #006600);
    }
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

st.title("🎁 Secret Santa 🎁")
st.subheader("Answer this to unlock your festive spirit 🎄")

# ---- Background Music ----
st.audio(
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    format="audio/mp3",
    start_time=0
)

question = "What gift would make you smile this Christmas?"
st.write(f"🎅 **Question:** {question}")

answer = st.text_input("🎄 Your Answer")

if st.button("Reveal Magic ✨") and answer:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---- LOG FORMAT ----
    log_message = (
        f"[{timestamp}] | EVENT=SECRET_SANTA_RESPONSE | "
        f"QUESTION=\"{question}\" | ANSWER=\"{answer}\""
    )

    st.success("Ho Ho Ho! 🎅 Your Secret Santa is taking notes!")
    st.code(log_message, language="log")

    # Optional delay for effect
    time.sleep(1)

st.caption("🎶 Snow falling, music playing, Santa is watching...")
