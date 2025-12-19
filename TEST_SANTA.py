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

    /* Floating sound button */
    #sound-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #ffd633;
        color: #333;
        border: none;
        border-radius: 30px;
        padding: 12px 18px;
        font-weight: bold;
        cursor: pointer;
        z-index: 10000;
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
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

# ---- Guaranteed Autoplay Music with Enhancements ----
st.markdown(
    """
    <audio id="bg-music" loop hidden>
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
    </audio>

    <button id="sound-btn">🔊 Enable Sound</button>

    <script>
        const audio = document.getElementById('bg-music');
        const btn = document.getElementById('sound-btn');

        // Restore preference
        const savedPref = localStorage.getItem('santa_sound');
        if (savedPref === 'on') {
            audio.volume = 0;
            audio.play().then(() => fadeIn());
            btn.style.display = 'none';
        }

        function fadeIn() {
            let vol = 0;
            audio.volume = vol;
            const fade = setInterval(() => {
                if (vol < 1) {
                    vol += 0.05;
                    audio.volume = Math.min(vol, 1);
                } else {
                    clearInterval(fade);
                }
            }, 120);
        }

        btn.addEventListener('click', () => {
            audio.volume = 0;
            audio.play().then(() => {
                fadeIn();
                localStorage.setItem('santa_sound', 'on');
                btn.style.display = 'none';
            });
        });
    </script>
    """,
    unsafe_allow_html=True
)

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

    with open("secret_santa.log", "a", encoding="utf-8") as f:
        f.write(log_message)

    st.success("Ho Ho Ho! 🎅 Your answer has been safely sent to Santa 🎁")
    time.sleep(1)

st.caption("🎶 Snow falling, music fading in, Santa is listening...")
