import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from streamlit_autorefresh import st_autorefresh

BACKEND = "http://localhost:5000"

API_KEY = "dev-secret-key" 
HEADERS = {"X-API-KEY": API_KEY}

st.set_page_config(page_title="Tennis for Two", layout="centered")
st.title("🎾 Tennis for Two")

st_autorefresh(interval=100, key="game_refresh")  # ~10 ticks/sec

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("P1 ⬆️"):
        requests.post(f"{BACKEND}/move", json={"player": 1, "direction": "up"}, headers=HEADERS)
    if st.button("P1 ⬇️"):
        requests.post(f"{BACKEND}/move", json={"player": 1, "direction": "down"}, headers=HEADERS)
with col2:
    if st.button("Reset"):
        requests.post(f"{BACKEND}/reset", headers=HEADERS)
with col3:
    if st.button("P2 ⬆️"):
        requests.post(f"{BACKEND}/move", json={"player": 2, "direction": "up"}, headers=HEADERS)
    if st.button("P2 ⬇️"):
        requests.post(f"{BACKEND}/move", json={"player": 2, "direction": "down"}, headers=HEADERS)

state = requests.post(f"{BACKEND}/update", headers=HEADERS).json()

st.subheader(f"Player 1: {state['score1']}  —  Player 2: {state['score2']}")

fig, ax = plt.subplots(figsize=(6, 4))
ax.set_xlim(0, state["width"])
ax.set_ylim(0, state["height"])
ax.invert_yaxis()
ax.set_facecolor("black")
fig.patch.set_facecolor("black")
ax.axis("off")

ax.add_patch(patches.Rectangle((0, state["paddle1_y"]), state["paddle_width"], state["paddle_height"], color="white"))
ax.add_patch(patches.Rectangle((state["width"] - state["paddle_width"], state["paddle2_y"]),
                                state["paddle_width"], state["paddle_height"], color="white"))
ax.add_patch(patches.Circle((state["ball_x"], state["ball_y"]), state["ball_size"] / 2, color="white"))

st.pyplot(fig)