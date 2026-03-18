# Rock Paper Scissors Game
A feature-rich, animated Rock Paper Scissors game built with Python and Pygame.

---

## Preview

| Feature | Description |
|--------|-------------|
| Window Size | 950 x 680 |
| Frame Rate | 60 FPS |
| Language | Python 3 |
| Library | Pygame |

---

## Features

- Animated gradient background with twinkling stars
- Particle explosion effects on every round result
- Smooth button hover animations with glow effects
- Win / loss streak tracker with live badge
- Round history bar showing last 15 results
- Score cards for Player, Computer, Draws and Rounds
- Support for custom PNG icons for Rock, Paper and Scissors
- Reset scores with button click or keyboard shortcut
- Locked button state during result animation to prevent misclicks

---

## Requirements

- Python 3.7 or higher
- Pygame library

Install Pygame using pip:

```
pip install pygame
```

---

## How to Run

1. Download or clone the project folder
2. Open a terminal inside the folder
3. Run the following command:

```
python rps-game-anim.py
```

---

## Controls

| Input | Action |
|-------|--------|
| Click Rock button | Choose Rock |
| Click Paper button | Choose Paper |
| Click Scissors button | Choose Scissors |
| Click Reset button | Reset all scores |
| R key | Reset all scores |
| ESC key | Quit the game |

---

## Adding Custom Icons (Optional)

You can replace the default drawn icons with your own PNG images.

**Step 1** — Get 3 PNG files with transparent backgrounds and name them exactly:

```
rock.png
paper.png
scissor.png
```

**Step 2** — Place all 3 files in the same folder as `rps-game-anim.py`

```
your_folder/
├── rps-game-anim.py
├── rock.png
├── paper.png
└── scissor.png
```

**Step 3** — Add the following image loading block in your script after the fonts section:

```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHOICE_IMAGES = {}
for _name in ["rock", "paper", "scissor"]:
    try:
        path = os.path.join(BASE_DIR, f"{_name}.png")
        img = pygame.image.load(path).convert_alpha()
        CHOICE_IMAGES[_name] = img
    except FileNotFoundError:
        CHOICE_IMAGES[_name] = None
```

**Recommended sites for free transparent PNG icons:**
- [opengameart.org](https://opengameart.org) — Free, no attribution required
- [flaticon.com](https://flaticon.com) — Large library, attribution required on free plan
- [icons8.com](https://icons8.com) — Clean modern icons

---

## Project Structure

```
your_folder/
├── rps-game-anim.py          # Main game file
├── rock.png                  # (Optional) Custom rock icon
├── paper.png                 # (Optional) Custom paper icon
├── scissor.png               # (Optional) Custom scissors icon
└── README.md                 # This file
```

---

## Customization

### Changing Colors
All colors are defined at the top of the file under the `Palette` section. You can change the background, button colors, glow effects and text colors from there.

### Changing Button Icon Size
Find this line inside the `draw_choice_button` function and adjust the number:
```python
icon_size = int(38 * scale)
```

### Changing Icon Position Inside Button
Find this line and adjust the offset value:
```python
draw_choice_icon(surf, choice, cx, cy - int(10 * scale), icon_size, icon_color)
```

---

## Known Notes

- Emoji characters such as fire or lightning may not display correctly on Windows due to font limitations. Plain ASCII symbols are used instead for compatibility.
- The image loader falls back to drawn shapes automatically if PNG files are missing, so the game always runs.

---

## License

This project is free to use for personal and educational purposes.

---

## Author

**Progya Paromita Saha**
Built with Python and Pygame.