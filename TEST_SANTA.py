import streamlit as st
import time
import os
from datetime import datetime
import streamlit.components.v1 as components

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

# ---- Ensure log directory inside git repo ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "secret_santa.log")
os.makedirs(LOG_DIR, exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8"):
        pass

# ================= ANIMATION = START PAGE =================
if not st.session_state.started:
    components.html(
        """
<!DOCTYPE html>
<html>
<head>
  <script type="module">
    import { Application, Controller } from "https://cdn.jsdelivr.net/npm/@hotwired/stimulus@3.2.2/+esm";
    import confetti from "https://cdn.skypack.dev/canvas-confetti";

    const application = Application.start();

    class GiftBoxController extends Controller {
      static targets = ["emoji", "claimBtn", "message"];
      claim() {
        this.emojiTarget.classList.remove("joggle");
        void this.emojiTarget.offsetWidth;
        this.emojiTarget.classList.add("gift-box__emoji--claimed");
        this.claimBtnTarget.hidden = true;
        setTimeout(() => {
          this.messageTarget.classList.remove("gift-box__message--hidden");
          this.emojiTarget.hidden = true;
          confetti({ particleCount: 200, spread: 100, origin: { y: 0.25 } });
          window.parent.postMessage("START_APP", "*");
        }, 800);
      }
    }
    application.register("gift-box", GiftBoxController);
  </script>

  <style>
    body { font-family: Lucida Grande; background: transparent; }
    .text-center { text-align: center; margin-top: 3em; }
    .joggle { animation: joggle 4.5s ease-in-out infinite; }
    .gift-box__emoji { font-size: 9em; }
    .gift-box__btn { font-size: 2em; margin-top: 1em; }
    .gift-box__emoji--claimed { transition: transform 500ms ease; transform: scale(1.5) rotate(12deg); }
    .gift-box__message { margin-top: 2em; font-size: 2em; transition: all 500ms ease; }
    .gift-box__message--hidden { opacity: 0; transform: scale(0.95); }
    @keyframes joggle {
      0%, 33%, 100% { transform: rotate(0deg); }
      3.33% { transform: rotate(-10deg); }
      6.67% { transform: rotate(12deg); }
      10% { transform: rotate(-10deg); }
      13.33% { transform: rotate(9deg); }
      16.67% { transform: rotate(0deg); }
    }
  </style>
</head>
<body>
  <div class="text-center" data-controller="gift-box">
    <h2>🎄 Claim your gift 🎄</h2>
    <div class="gift-box__emoji joggle" data-gift-box-target="emoji">🎁</div>
    <div>
      <button class="gift-box__btn" data-action="gift-box#claim" data-gift-box-target="claimBtn">Claim</button>
    </div>
    <div class="gift-box__message gift-box__message--hidden" data-gift-box-target="message">✨ Let the magic begin ✨</div>
  </div>
</body>
</html>
        """,
        height=450,
    )

    # listen for iframe message
    st.markdown(
        """
        <script>
        window.addEventListener("message", (event) => {
            if (event.data === "START_APP") {
                fetch("/?start=true");
            }
        });
        </script>
        """,
        unsafe_allow_html=True
    )

    if st.query_params.get("start"):
        st.session_state.started = True
        st.rerun()

# ================= MAIN PAGE =================
if st.session_state.started:
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

    st.caption("❄️ Snow falling, Santa is watching...")

