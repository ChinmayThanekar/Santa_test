import streamlit as st
import time
from datetime import datetime
import streamlit.components.v1 as components

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
st.audio(
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    format="audio/mp3",
    start_time=0
)
# ---- Snowflakes ----
for i in range(25):
    st.markdown(
        f"<div class='snowflake' style='left:{i*4}%; animation-duration:{5+i%5}s'>❄️</div>",
        unsafe_allow_html=True
    )

# ---- GUARANTEED AUDIO (Streamlit-safe method) ----
# Uses iframe HTML component – this is the ONLY reliable way in Streamlit
components.html(
    """
    <audio id="bg" autoplay loop muted>
      <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
    </audio>

    <script>
      const audio = document.getElementById('bg');

      // Try autoplay muted
      audio.play().catch(() => {});

      // Unmute on first user interaction
      const enable = () => {
        audio.muted = false;
        audio.play();
        document.removeEventListener('click', enable);
        document.removeEventListener('keydown', enable);
      };

      document.addEventListener('click', enable);
      document.addEventListener('keydown', enable);
    </script>
    """,
    height=0,
)

st.title("🎁 Secret Santa 🎁")
st.subheader("Answer this to unlock your festive spirit 🎄")

st.info("🔊 Tap anywhere once to enable festive sound (browser requirement)")

question = "What gift would make you smile this Christmas?"
st.write(f"🎅 **Question:** {question}")

answer = st.text_input("🎄 Your Answer")

if st.button("Reveal Magic ✨") and answer:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_message = (
        f"[{timestamp}] | EVENT=SECRET_SANTA_RESPONSE | "
        f"QUESTION=\"{question}\" | ANSWER=\"{answer}\"\n"
    )

    with open("secret_santa.log", "a", encoding="utf-8") as f:
        f.write(log_message)

    st.success("Ho Ho Ho! 🎅 Your answer has been safely sent to Santa 🎁")
    time.sleep(1)

st.caption("🎶 Snow falling, Santa listening...")

