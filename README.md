# ✊ Rock Paper Scissors Game

A feature-rich Rock Paper Scissors game built with Python — available in two versions: a desktop Pygame edition and a live web app built with Streamlit.

---

## 🌐 Live Demo

▶️ **[Play it here → Rock Paper Scissors ](https://progya-rps-game.streamlit.app/)**

---

## 📁 Project Structure

```
rps-game/
├── app-streamlit.py      # Streamlit web app (live on Streamlit Cloud)
├── rps-game.py           # Original desktop version using Pygame
├── requirements.txt      # Dependencies for Streamlit deployment
├── rock.png              # Rock icon
├── paper.png             # Paper icon
├── scissor.png           # Scissors icon
└── README.md
```

---

## ✨ Features

- Score tracking for Player, Computer, Draws and Rounds
- Win / loss streak tracker with live badge
- Round history showing last 15 results with win rate progress bar
- Custom PNG icons for Rock, Paper and Scissors
- Balloon celebration on win
- Reset scores anytime

---

## 🗂️ Two Versions

### Version 1 — Streamlit Web App `app-streamlit.py`

| Detail | Info |
| --- | --- |
| Language | Python 3 |
| Library | Streamlit |
| Runs on | Browser — no installation needed |
| Deployed | Streamlit Cloud |

**How to run locally:**

```bash
pip install streamlit
streamlit run app-streamlit.py
```

---

### Version 2 — Pygame Desktop App `rps-game.py`

| Detail | Info |
| --- | --- |
| Language | Python 3 |
| Library | Pygame |
| Window Size | 950 x 680 |
| Frame Rate | 60 FPS |

**Extra features in the Pygame version:**
- Animated gradient background with twinkling stars
- Particle explosion effects on every round result
- Smooth button hover animations with glow effects
- Keyboard shortcuts (R to reset, ESC to quit)

**How to run locally:**

```bash
pip install pygame
python rps-game.py
```

**Controls:**

| Input | Action |
| --- | --- |
| Click Rock button | Choose Rock |
| Click Paper button | Choose Paper |
| Click Scissors button | Choose Scissors |
| Click Reset button | Reset all scores |
| R key | Reset all scores |
| ESC key | Quit the game |

---

## ⚙️ Requirements

**For Streamlit version:**
```
streamlit
```

**For Pygame version:**
```
pygame
```

---

## 📄 License

This project is free to use for personal and educational purposes.

---

## 👩‍💻 Author

**Progya Paromita Saha**  
B.Sc. in Computing and Information Systems — Daffodil International University  
Summer 2026