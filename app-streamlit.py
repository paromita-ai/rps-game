import streamlit as st
import random

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="✊",
    layout="centered",
)

st.markdown("""
<style>
[data-testid="stHeadingWithActionElements"] a { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
DEFAULTS = {
    "player_score": 0,
    "cpu_score":    0,
    "draws":        0,
    "history":      [],     # list of "W" / "L" / "D"
    "streak":       0,      # +N = player streak, -N = CPU streak
    "player_choice": None,
    "cpu_choice":    None,
    "result_type":   None,  # "win" | "lose" | "draw"
    "result_msg":    "",
    "show_result":   False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Constants ────────────────────────────────────────────────────────────────
CHOICES = ["rock", "paper", "scissor"]

LABEL = {
    "rock":    "Rock",
    "paper":   "Paper",
    "scissor": "Scissors",
}

EMOJI = {
    "rock":    "✊",
    "paper":   "✋",
    "scissor": "✌️",
}

# Raw GitHub PNG URLs from your own repo
IMG_URL = {
    "rock":    "https://raw.githubusercontent.com/progya-ai/rps-game/main/rock.png",
    "paper":   "https://raw.githubusercontent.com/progya-ai/rps-game/main/paper.png",
    "scissor": "https://raw.githubusercontent.com/progya-ai/rps-game/main/scissor.png",
}

WINS = {("rock", "scissor"), ("paper", "rock"), ("scissor", "paper")}

# ─── Game Logic ───────────────────────────────────────────────────────────────
def check_winner(player, cpu):
    if player == cpu:
        return "draw"
    return "win" if (player, cpu) in WINS else "lose"

def play_round(choice):
    s   = st.session_state
    cpu = random.choice(CHOICES)
    result = check_winner(choice, cpu)

    s.player_choice = choice
    s.cpu_choice    = cpu
    s.result_type   = result

    
    
    if result == "win":
         s.player_score += 1
         s.streak        = max(1, s.streak + 1)
         s.result_msg    = "🎉 You Win!"
    elif result == "lose":
            s.cpu_score += 1
            s.streak    = min(-1, s.streak - 1)
            s.result_msg = "💻 CPU Wins!"
    else:
            s.draws    += 1
            s.streak    = 0
            s.result_msg = "🤝 It's a Draw!"

    tag = {"win": "W", "lose": "L", "draw": "D"}[result]
    s.history.append(tag)
    if len(s.history) > 15:
        s.history.pop(0)

    s.show_result = True

def reset_game():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v

# ─── Shorthand ────────────────────────────────────────────────────────────────
s = st.session_state

# ═══════════════════════════════════════════════════════════════════════════════
# UI
# ═══════════════════════════════════════════════════════════════════════════════

# ── Title ──────────────────────────────────────────────────────────────────────
_, col_m, _ = st.columns([1, 2.95, 1])
with col_m:
 st.title("Rock Paper Scissors")
_, col_m, _ = st.columns([1, 2.4, 1])
with col_m:
 st.caption("Built with Streamlit · by Progya Paromita Saha · DIU CIS 2025")

# ── Reset button ───────────────────────────────────────────────────────────────
_, col_m, _ = st.columns([1, 0.7, 1])
with col_m:
 if st.button("↺  Reset All Scores", use_container_width=False):
    reset_game()
    st.rerun()



# ── Scoreboard ─────────────────────────────────────────────────────────────────
_, col_m, _ = st.columns([1, 3, 1])
with col_m:
 c1, c2, c3, c4 = st.columns(4)

c1.metric("🧑 You",      s.player_score, delta=None)
c2.metric("🤝 Draws",    s.draws,        delta=None)
c3.metric("🔢 Rounds",   len(s.history), delta=None)
c4.metric("💻 Computer", s.cpu_score,    delta=None)

# ── Streak badge ───────────────────────────────────────────────────────────────
if s.streak > 0:
    st.success(f"🔥 You are on a **{s.streak}-win streak!**")
elif s.streak < 0:
    st.error(f"🤖 Computer is on a **{abs(s.streak)}-win streak!**")



# ── Result display ─────────────────────────────────────────────────────────────
if s.show_result and s.player_choice and s.cpu_choice:

    # Icons side by side
    spacer, left, mid, right = st.columns([0.25, 2, 2, 2])

    with left:
        _, col_m, _ = st.columns([1, 6, 1])
        with col_m:
            st.image(IMG_URL[s.player_choice], width=70)
            st.subheader(f"{EMOJI[s.player_choice]} {LABEL[s.player_choice]}")
            st.caption("Your choice")


    with mid:
        _, col_m, _ = st.columns([1, 1, 1])
        with col_m:
            st.write("")
            st.write("")
            st.write("")
            st.write("### VS")

    with right:
        _, col_m, _ = st.columns([1, 6, 1])
        with col_m:
            st.image(IMG_URL[s.cpu_choice], width=70)
            st.subheader(f"{EMOJI[s.cpu_choice]} {LABEL[s.cpu_choice]}")
            st.caption("CPU's choice")


    st.write("")

    # Result banner
    _, col_m, _ = st.columns([1, 1.45, 1])
    with col_m:
        if s.result_type == "win":
            st.success(f"## {s.result_msg}")
            st.balloons()
        elif s.result_type == "lose":
            st.error(f"## {s.result_msg}")
        else:
            st.warning(f"## {s.result_msg}")
    st.write("")

    # Play again
    # if st.button("▶  Play Again", use_container_width=True, type="primary"):
    #     s.show_result    = False
    #     s.player_choice  = None
    #     s.cpu_choice     = None
    #     s.result_type    = None
    #     s.result_msg     = ""
        #st.rerun()

# ── Choice buttons (shown when not in result phase) ────────────────────────────
_, col_m, _ = st.columns([1, 1.03, 1])
with col_m:
    
    st.subheader("Make your move!")
    st.write("")

b1, b2, b3 = st.columns(3)

with b1:
        _, col_m, _ = st.columns([1, 1, 1])
        with col_m:

            st.image(IMG_URL["rock"], width=70)
        if st.button("✊  Rock",     use_container_width=True, type="secondary"):
            play_round("rock");    st.rerun()

with b2:
        _, col_m, _ = st.columns([1, 1, 1])
        with col_m:

            st.image(IMG_URL["paper"], width=70)
        if st.button("✋  Paper",   use_container_width=True, type="secondary"):
            play_round("paper");   st.rerun()

with b3:
        _, col_m, _ = st.columns([1, 1, 1])
        with col_m:

            st.image(IMG_URL["scissor"], width=70)
        if st.button("✌️  Scissors", use_container_width= True, type="secondary"):
            play_round("scissor"); st.rerun()



# ── Round history ──────────────────────────────────────────────────────────────
if s.history:
    st.write("**Round history** (last 15)")

    # Map tags to readable symbols
    symbol = {"W": "🟢", "L": "🔴", "D": "🟡"}
    history_line = "  ".join(symbol[tag] for tag in s.history)
    st.write(history_line)

    # Win rate
    wins   = s.history.count("W")
    total  = len(s.history)
    pct    = int(wins / total * 100)
    st.progress(pct / 100, text=f"Win rate: {pct}%  ({wins}/{total})")

st.write("")

