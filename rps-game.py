import pygame
import random
import sys
import math

pygame.init()

# ─── Screen Display ───────────────────────────────────────────────
WIDTH, HEIGHT = 950, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock  Paper  Scissors")
clock = pygame.time.Clock()
FPS = 60

# ─── Color Palette ──────────────────────────────────────────────────────
BG_TOP         = (8,  10, 28)
BG_BOT         = (22, 8,  44)
WHITE          = (255, 255, 255)
OFF_WHITE      = (220, 220, 240)
YELLOW         = (255, 210,  60)
GREEN          = ( 60, 220, 130)
RED            = (230,  70,  70)
CYAN           = ( 80, 200, 255)
PURPLE         = (150,  80, 240)
DARK_CARD      = ( 20,  20,  50)
MID_CARD       = ( 30,  30,  65)
GRAY           = (100, 100, 130)
LIGHT_GRAY     = (180, 180, 210)
BLUEISH_PURPLE = (153,  51, 255)
EMERALD_GREEN  = (50,  170, 130)
WARM_CORAL     = (210, 90,  80)
PINK           = (255, 105, 180)
BLUE           = (50, 150, 255)



CHOICE_COLOR = {
    "rock":    BLUEISH_PURPLE,  
    "paper":   EMERALD_GREEN,  
    "scissor": WARM_CORAL ,   
}
CHOICE_GLOW = {
    "rock":    (130, 140, 255),
    "paper":   (80,  220, 170),
    "scissor": (255, 130, 120),
}

CHOICE_LABEL = {"rock": "Rock", "paper": "Paper", "scissor": "Scissors"}
CHOICES = ["rock", "paper", "scissor"]

# ─── Fonts ────────────────────────────────────────────────────────
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_BOLD    = os.path.join(BASE_DIR, "Nunito-Bold.ttf")
FONT_REGULAR = os.path.join(BASE_DIR, "Nunito-Regular.ttf")

f_title  = pygame.font.Font(FONT_BOLD, 52)
f_big    = pygame.font.Font(FONT_BOLD, 38)
f_med    = pygame.font.Font(FONT_REGULAR, 26)
f_small  = pygame.font.Font(FONT_REGULAR, 21)
f_tiny   = pygame.font.Font(FONT_REGULAR, 16)

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHOICE_IMAGES = {}
for _name in ["rock", "paper", "scissor"]:
    try:
        path = os.path.join(BASE_DIR, f"{_name}.png")
        img = pygame.image.load(path).convert_alpha()
        CHOICE_IMAGES[_name] = img
        print(f"Loaded: {path}")
    except FileNotFoundError:
        CHOICE_IMAGES[_name] = None
        print(f"Not found: {path}")

print(CHOICE_IMAGES)


# ─── Helpers ──────────────────────────────────────────────────────
def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def draw_rounded_rect(surf, color, rect, r=28, alpha=128, border=0, bc=None):
    rx, ry, rw, rh = rect
    if alpha < 255:
        tmp = pygame.Surface((rw, rh), pygame.SRCALPHA)
        pygame.draw.rect(tmp, (*color[:3], alpha), (0, 0, rw, rh), border_radius=r)
        surf.blit(tmp, (rx, ry))
    else:
        pygame.draw.rect(surf, color, rect, border_radius=r)
    if border and bc:
        pygame.draw.rect(surf, bc, rect, border, border_radius=r)

def draw_glow_circle(surf, color, cx, cy, radius, layers=4, max_alpha=60):
    for i in range(layers, 0, -1):
        r = radius * i
        a = max_alpha // i
        tmp = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(tmp, (*color[:3], a), (r, r), r)
        surf.blit(tmp, (cx - r, cy - r))

def draw_text_centered(surf, text, font, color, cx, cy, alpha=255):
    rendered = font.render(text, True, color)
    if alpha < 255:
        rendered.set_alpha(alpha)
    surf.blit(rendered, rendered.get_rect(center=(cx, cy)))
    return rendered

# ─── Animated Gradient Background ────────────────────────────────
_bg_cache = {}
def draw_bg(surf, offset):
    key = int(offset) % 400
    if key not in _bg_cache:
        tmp = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            t = y / HEIGHT
            wave = math.sin((y + key) * 0.015) * 8
            t2 = max(0, min(1, t + wave / HEIGHT))
            c = lerp_color(BG_TOP, BG_BOT, t2)
            pygame.draw.line(tmp, c, (0, y), (WIDTH, y))
        _bg_cache[key] = tmp
    surf.blit(_bg_cache[key], (0, 0))

# ─── Glittering Stars ────────────────────────────────────────────────────────
stars = [
    (random.randint(0, WIDTH), random.randint(0, HEIGHT),
     random.uniform(0.3, 1.5), random.uniform(0, math.pi * 2))
    for _ in range(100)
]

def draw_stars(surf, t):
    for sx, sy, sr, phase in stars:
        brightness = int(120 + 100 * math.sin(t * 3.5 + phase))
        brightness = max(40, min(220, brightness))
        pygame.draw.circle(surf, (brightness, brightness, brightness + 20),
                           (sx, sy), max(1, int(sr)))
        
# ─── Particle Explosion System ──────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(5, 10)
        self.x, self.y = float(x), float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - random.uniform(1, 3)
        self.color = color
        self.life = 1.0
        self.decay = random.uniform(0.018, 0.045)
        self.size = random.randint(4, 9)
        self.gravity = random.uniform(0.1, 0.25)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.98
        self.life -= self.decay

    def draw(self, surf):
        if self.life <= 0:
            return
        a = int(255 * self.life)
        sz = max(1, int(self.size * self.life))
        tmp = pygame.Surface((sz*2, sz*2), pygame.SRCALPHA)
        pygame.draw.circle(tmp, (*self.color[:3], a), (sz, sz), sz)
        surf.blit(tmp, (int(self.x)-sz, int(self.y)-sz))

particles = []

def spawn_particles(x, y, color, n=30):
    for _ in range(n):
        particles.append(Particle(x, y, color))

# ─── Button Icons ───────────────────────────────────────────────────
def draw_rock(surf, cx, cy, radius, color, outline=None):
    """Fist shape"""
    if outline is None:
        outline = tuple(min(255, c + 60) for c in color)
    # Main fist
    pygame.draw.circle(surf, color, (cx, cy + radius//6), radius)
    # Flat bottom (palm stub)
    pygame.draw.rect(surf, color, (cx - radius//2, cy + radius//4,
                                   radius, radius//2), border_radius=8)
    # Knuckle highlights
    for i, dx in enumerate([-radius//3, 0, radius//3]):
        ky = cy - radius//2
        pygame.draw.circle(surf, outline, (cx + dx, ky), radius//8)
    pygame.draw.circle(surf, outline, (cx, cy + radius//6), radius, 3)

def draw_paper(surf, cx, cy, size, color, outline=None):
    """Open flat hand"""
    if outline is None:
        outline = tuple(min(255, c + 60) for c in color)
    fw, fh = size//5, size
    # 5 fingers
    offsets = [-2, -1, 0, 1, 2]
    for i, ox in enumerate(offsets):
        fx = cx + ox * (fw + 2)
        fy = cy - fh//2
        flen = fh - abs(ox) * (size//12)
        pygame.draw.rect(surf, color,
                         (fx - fw//2, fy - flen//2 + size//6, fw, flen),
                         border_radius=fw//2)
    # Palm
    pw = size + 8
    pygame.draw.rect(surf, color,
                     (cx - pw//2, cy + size//8, pw, size//2), border_radius=12)
    # Outline hint
    pygame.draw.rect(surf, outline,
                     (cx - pw//2, cy + size//8, pw, size//2), 2, border_radius=12)

def draw_scissor(surf, cx, cy, size, color, outline=None):
    """Peace / scissors fingers"""
    if outline is None:
        outline = tuple(min(255, c + 60) for c in color)
    fw = size // 4
    # Two extended fingers (V)
    spread = size // 5
    for dx, angle in [(-spread, -0.18), (spread, 0.18)]:
        fx = cx + dx
        fy = cy - size // 2
        pts = [
            (fx - fw//2, cy),
            (fx + fw//2, cy),
            (fx + fw//2 + int(size * math.sin(angle) * 0.5), fy),
            (fx - fw//2 + int(size * math.sin(angle) * 0.5), fy),
        ]
        pygame.draw.polygon(surf, color, pts)
        pygame.draw.polygon(surf, outline, pts, 2)
        pygame.draw.circle(surf, color, (fx + int(size * math.sin(angle) * 0.5), fy), fw//2)
    # Remaining 3 fingers curled (small)
    for dx in [-size//3, 0, size//3]:
        pygame.draw.rect(surf, color,
                         (cx + dx - fw//3, cy, fw*2//3, size//4), border_radius=6)
    # Palm
    pygame.draw.rect(surf, color,
                     (cx - size//2, cy + size//5, size, size//3), border_radius=10)

DRAW_FN = {"rock": draw_rock, "paper": draw_paper, "scissor": draw_scissor}

def draw_choice_icon(surf, choice, cx, cy, size, color):
    img = CHOICE_IMAGES.get(choice)
    if img is not None:
        scaled = pygame.transform.smoothscale(img, (size * 2, size * 2))
        if color != WHITE:
            # set_alpha dims the image without destroying transparency
            scaled.set_alpha(150)
        surf.blit(scaled, scaled.get_rect(center=(cx, cy)))
    else:
        DRAW_FN[choice](surf, cx, cy, size, color)

# ─── Button Icon Drawing ───────────────────────────────────────────────
def draw_choice_button(surf, choice, rect, scale, hovered, locked):
    cx, cy = rect.centerx, rect.centery
    w  = int(rect.width  * scale)
    h  = int(rect.height * scale)
    r  = pygame.Rect(cx - w//2, cy - h//2, w, h)

    base  = CHOICE_COLOR[choice]
    glow  = CHOICE_GLOW[choice]
    dark  = tuple(max(0, c - 70) for c in base)

    if locked:
        base = tuple(int(c * 0.45) for c in base)
        dark = tuple(int(c * 0.3)  for c in base)

    # Outer glow when hovered
    if hovered and not locked:
        draw_glow_circle(surf, glow, cx, cy + 5, w // 2, layers=3, max_alpha=55)

    # Drop shadow
    shadow = r.inflate(0, 0)
    shadow.y += 8
    draw_rounded_rect(surf, dark, shadow, r=22, alpha=140)

    # Button body
    draw_rounded_rect(surf, base, r, r=22)

    # Shine stripe
    shine = (r.x + 14, r.y + 8, r.width - 28, r.height // 3)
    draw_rounded_rect(surf, WHITE, shine, r=14, alpha=28)

    # Border
    bc = glow if hovered and not locked else tuple(min(255, c + 40) for c in base)
    pygame.draw.rect(surf, bc, r, 2 if hovered else 1, border_radius=22)

    # Icon
    icon_size = int(38 * scale)
    icon_color = WHITE if not locked else (90, 90, 110)
    draw_choice_icon(surf, choice, cx, cy - int(10 * scale), icon_size, icon_color)

    # Label
    lbl = f_small.render(CHOICE_LABEL[choice], True,
                         WHITE if not locked else (90, 90, 110))
    surf.blit(lbl, lbl.get_rect(center=(cx, cy + int(38 * scale))))

# ─── Score Board ───────────────────────────────────────────────────
def draw_score_card(surf, x, y, w, h, label, value, color, leading=False, t=0):
    # Pulsing border if leading
    alpha = 255
    bc = tuple(int(c * (0.7 + 0.3 * math.sin(t * 2))) for c in color) if leading else (50, 50, 80)
    bw = 3 if leading else 1
    draw_rounded_rect(surf, DARK_CARD, (x, y, w, h), r=16, alpha=230)
    pygame.draw.rect(surf, bc, (x, y, w, h), bw, border_radius=16)
    # Label
    ls = f_tiny.render(label, True, WHITE)
    surf.blit(ls, ls.get_rect(center=(x + w//2, y + 20)))
    # Value
    vs = f_big.render(str(value), True, color)
    surf.blit(vs, vs.get_rect(center=(x + w//2, y + h - 28)))

# ─── Round History ────────────────────────────────────────────────
history = []   # list of ("W"/"L"/"D", round_num)

def add_history(result_str):
    tag = "W" if "You Win" in result_str else ("L" if "Computer" in result_str else "D")
    history.append(tag)
    if len(history) > 15:
        history.pop(0)

def draw_history(surf, x, y):
    label = f_tiny.render("Round history:", True, WHITE)
    surf.blit(label, (x, y))
    for i, tag in enumerate(history):
        col = GREEN if tag == "W" else (RED if tag == "L" else YELLOW)
        bx = x + i * 28
        draw_rounded_rect(surf, col, (bx, y + 20, 18, 18), r=6, alpha=200)
        ts = f_tiny.render(tag, True, DARK_CARD)
        surf.blit(ts, ts.get_rect(center=(bx + 9, y + 29)))

# ─── Game State ───────────────────────────────────────────────────
player_score    = 0
cpu_score       = 0
draws           = 0
streak          = 0        # positive = player streak, negative = cpu streak
player_choice   = None
cpu_choice      = None
result_str      = ""
phase           = "idle"   # "idle" | "showing"
phase_timer     = 0.0      # seconds
result_alpha    = 0

hover_scale = {c: 1.0 for c in CHOICES}
pulse_t = 0.0
bg_offset = 0.0

BTN_Y = 487
BTN_W, BTN_H = 210, 110
btn_rects = {
    "rock":    pygame.Rect(100, BTN_Y, BTN_W, BTN_H),
    "paper":   pygame.Rect(370, BTN_Y, BTN_W, BTN_H),
    "scissor": pygame.Rect(640, BTN_Y, BTN_W, BTN_H),
}

reset_rect  = pygame.Rect(WIDTH - 155, 15, 140, 36)

def check_winner(p, c):
    if p == c:
        return "Draw!"
    if (p == "rock"    and c == "scissor") or \
       (p == "paper"   and c == "rock")    or \
       (p == "scissor" and c == "paper"):
        return "You Win!"
    return "Computer Wins!"

# ─── Main Loop ────────────────────────────────────────────────────
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    pulse_t   += dt
    bg_offset += dt * 18

    mouse = pygame.mouse.get_pos()

    # ── Events ──
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:
                player_score = cpu_score = draws = streak = 0
                history.clear()
                particles.clear()
                phase = "idle"

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Reset button
            if reset_rect.collidepoint(mouse):
                player_score = cpu_score = draws = streak = 0
                history.clear()
                particles.clear()
                phase = "idle"
                player_choice = cpu_choice = None
                result_str = ""

            # Choice buttons
            if phase == "idle":
                for choice, rect in btn_rects.items():
                    if rect.collidepoint(mouse):
                        player_choice = choice
                        cpu_choice    = random.choice(CHOICES)
                        result_str    = check_winner(player_choice, cpu_choice)

                        cx, cy = WIDTH // 2, HEIGHT // 2 - 40
                        if "You Win" in result_str:
                            player_score += 1
                            streak = max(1, streak + 1)
                            spawn_particles(cx, cy, GREEN,  45)
                            spawn_particles(cx, cy, YELLOW, 20)
                            spawn_particles(cx, cy, PINK, 20)
                        elif "Computer" in result_str:
                            cpu_score += 1
                            streak = min(-1, streak - 1)
                            spawn_particles(cx, cy, RED,   35)
                            spawn_particles(cx, cy, PURPLE, 15)
                            spawn_particles(cx, cy, BLUE,   35)
                        else:
                            draws += 1
                            streak = 0
                            spawn_particles(cx, cy, CYAN,   25)
                            spawn_particles(cx, cy, YELLOW, 10)

                        add_history(result_str)
                        phase = "showing"
                        phase_timer  = 0.0
                        result_alpha = 0

    # ── Phase logic ──
    if phase == "showing":
        phase_timer  += dt
        result_alpha  = min(255, result_alpha + int(dt * 800))
        if phase_timer >= 2.6:
            phase         = "idle"
            player_choice = None
            cpu_choice    = None
            result_str    = ""

    # ── Hover scales ──
    for c, rect in btn_rects.items():
        target = 1.08 if (rect.collidepoint(mouse) and phase == "idle") else 1.0
        hover_scale[c] += (target - hover_scale[c]) * 0.15

    # ── Particles ──
    particles[:] = [p for p in particles if p.life > 0]
    for p in particles:
        p.update()

    # DRAW
    # ═══════════════════════════════════════════════
    draw_bg(screen, bg_offset)
    draw_stars(screen, pulse_t)
    # ═══════════════════════════════════════════════

    # ── Glowing orbs ────────────────────────────
    glow_y = HEIGHT // 2 + int(60 * math.sin(pulse_t * 1.0))
    draw_glow_circle(screen, CYAN, 120, glow_y, 90, layers=3, max_alpha=18)
    draw_glow_circle(screen, CYAN, 830, glow_y, 90, layers=3, max_alpha=18)

    # ── Heading Title ──────────────────────────────────────────────────────
    title_shadow = f_title.render("Rock  Paper  Scissors", True, (20, 10, 50))
    title_surf   = f_title.render("Rock  Paper  Scissors", True, WHITE)
    screen.blit(title_shadow, title_shadow.get_rect(center=(WIDTH//2 + 3, 37)))
    screen.blit(title_surf,   title_surf  .get_rect(center=(WIDTH//2,     35)))

    # Subtitle line
    sub = f_tiny.render("Press  R  or  Reset  to  clear  scores", True, WHITE)
    screen.blit(sub, sub.get_rect(center=(WIDTH//2, 82)))

    # ── Score Row ──
    p_lead = player_score > cpu_score
    c_lead = cpu_score > player_score

    draw_score_card(screen, 60,  102, 160, 82, "YOU",       player_score, GREEN,  p_lead, pulse_t)
    draw_score_card(screen, 240, 102, 120, 82, "DRAWS",     draws,        YELLOW, False,  pulse_t)
    draw_score_card(screen, 380, 102, 110, 82, "ROUNDS",    len(history), BLUE,   False,  pulse_t)
    draw_score_card(screen, 720, 102, 170, 82, "COMPUTER",  cpu_score,    RED,    c_lead, pulse_t)

    # Streak badge
    if streak != 0:
        scol  = GREEN if streak > 0 else RED
        slabel = f"{abs(streak)}-streak  {'(you)' if streak > 0 else '(CPU)'}"
        st = f_small.render(f"{'>>>' if streak > 0 else '<<<'} Streak", True, scol)
        sn = f_med.render(f"×{abs(streak)}", True, scol)
        screen.blit(st, st.get_rect(center=(605, 128)))
        screen.blit(sn, sn.get_rect(center=(605, 155)))

        # ── Middle Display Card ──
    card_rect = (60, 210, WIDTH - 120, 250)
    draw_rounded_rect(screen, MID_CARD, card_rect, r=24, alpha=220)
    pygame.draw.rect(screen, (55, 55, 100), card_rect, 1, border_radius=24)

    if phase == "showing" and player_choice and cpu_choice:
        pc  = CHOICE_COLOR[player_choice]
        cc  = CHOICE_COLOR[cpu_choice]
        pcx, pcy = 230, 330
        ccx, ccy = 720, 330

        # Player side
        draw_glow_circle(screen, pc, pcx, pcy, 55, layers=3, max_alpha=35)
        draw_choice_icon(screen, player_choice, pcx, pcy, 55, pc)
        draw_text_centered(screen, "YOU",
                           f_tiny, WHITE, pcx, pcy - 78)
        draw_text_centered(screen, CHOICE_LABEL[player_choice],
                           f_small, pc, pcx, pcy + 72, alpha=result_alpha)

        # CPU side
        draw_glow_circle(screen, cc, ccx, ccy, 55, layers=3, max_alpha=35)
        draw_choice_icon(screen, cpu_choice, ccx, ccy, 55, cc)
        draw_text_centered(screen, "CPU",
                           f_tiny, WHITE, ccx, ccy - 78)
        draw_text_centered(screen, CHOICE_LABEL[cpu_choice],
                           f_small, cc, ccx, ccy + 72, alpha=result_alpha)

        # VS
        vs_scale = 1.0 + 0.06 * math.sin(pulse_t * 4)
        vs_surf  = f_med.render("~ VS ~", True, YELLOW)
        vs_surf  = pygame.transform.rotozoom(vs_surf, 0, vs_scale)
        screen.blit(vs_surf, vs_surf.get_rect(center=(WIDTH//2, 330)))

        # Result banner
        if "You Win" in result_str:
            rcol = GREEN
        elif "Computer" in result_str:
            rcol = RED
        else:
            rcol = YELLOW

        # Animated banner bg
        bw = int(320 + 10 * math.sin(pulse_t * 5))
        draw_rounded_rect(screen, tuple(c//5 for c in rcol),
                          (WIDTH//2 - bw//2, 383, bw, 50), r=14, alpha=result_alpha)
        pygame.draw.rect(screen, rcol,
                         (WIDTH//2 - bw//2, 383, bw, 50), 2, border_radius=14)

        r_surf = f_big.render(result_str, True, rcol)
        r_surf.set_alpha(result_alpha)
        screen.blit(r_surf, r_surf.get_rect(center=(WIDTH//2, 408)))

    else:
        # Idle prompt
        pulse_val = 0.5 + 0.5 * math.sin(pulse_t * 1.5)
        icol = lerp_color(CYAN, WHITE, pulse_val)
        draw_text_centered(screen, "Make your move!", f_big, icol, WIDTH//2, 310)
        draw_text_centered(screen, "Choose  Rock,  Paper  or  Scissors  below",
                           f_small, WHITE, WIDTH//2, 355)

        # Animated mini icons (floating)
        for i, ch in enumerate(CHOICES):
            fx = WIDTH//2 + (i - 1) * 110
            fy = 415 + int(6 * math.sin(pulse_t * 1.8 + i * 1.2))
            mini_col = tuple(int(c * 0.6) for c in CHOICE_COLOR[ch])
            draw_choice_icon(screen, ch, fx, fy, 22, mini_col)

    # ── Particles ──
    for p in particles:
        p.draw(screen)

    # ── History ──
    if history:
        draw_history(screen, 62, HEIGHT - 80)

    # ── Choice Buttons ──
    locked = (phase == "showing")
    for choice, rect in btn_rects.items():
        hovered = rect.collidepoint(mouse) and not locked
        draw_choice_button(screen, choice, rect,
                           scale=hover_scale[choice],
                           hovered=hovered,
                           locked=locked)

    # ── Keyboard hints under buttons ──
    # (cosmetic only)
    hint_keys = {"rock": "← Left", "paper": "↓ Middle", "scissor": "→ Right"}

    # ── Reset button ──
    rh = reset_rect.collidepoint(mouse)
    rc = (70, 70, 120) if rh else (40, 40, 80)
    draw_rounded_rect(screen, rc, reset_rect, r=10)
    pygame.draw.rect(screen, (90, 90, 150), reset_rect, 1, border_radius=10)
    rt = f_tiny.render(" Reset Scores", True, WHITE)
    screen.blit(rt, rt.get_rect(center=reset_rect.center))

    # ── Footer ──
    ft = f_tiny.render("ESC to quit", True, (55, 55, 80))
    screen.blit(ft, ft.get_rect(bottomright=(WIDTH - 12, HEIGHT - 8)))

    pygame.display.flip()

pygame.quit()