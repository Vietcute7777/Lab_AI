# cleanbot-saga/ui/renderer.py
"""Enhanced Pygame rendering with gradients, glow, and animations."""
import pygame
import math
import config as cfg


# ── Primitives ──

def draw_rect_gradient(screen, rect, color_top, color_bottom):
    """Draw a vertical gradient rectangle."""
    x, y, w, h = rect
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * t)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * t)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * t)
        pygame.draw.line(screen, (r, g, b), (x, y + i), (x + w, y + i))


def draw_shadow(screen, rect, color=(0, 0, 0, 80), offset=3, radius=8):
    """Draw a shadow under a rounded rect."""
    sr = rect.move(offset, offset)
    shadow = pygame.Surface((rect.width + offset * 2, rect.height + offset * 2), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (*color[:3], 60), shadow.get_rect(), border_radius=radius)
    screen.blit(shadow, (rect.x - offset // 2, rect.y - offset // 2))


def draw_glow(screen, center, radius, color, alpha=80):
    """Draw a glowing circle."""
    for i in range(3, 0, -1):
        r = radius + i * 4
        a = alpha // (i + 1)
        glow = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*color[:3], a), (r, r), r)
        screen.blit(glow, (center[0] - r, center[1] - r))


# ── Puzzle ──

def draw_puzzle_board(screen, board, ox, oy, highlight=None, correct_tiles=None):
    """Draw 3x3 puzzle with colored tiles. correct_tiles = set of (r,c) that are in goal position."""
    if correct_tiles is None:
        correct_tiles = set()
    cell = cfg.PUZZLE_CELL_SIZE
    gap = cfg.PUZZLE_GAP

    # Draw shadow under board
    board_rect = pygame.Rect(ox - 2, oy - 2, 3 * (cell + gap) + 4, 3 * (cell + gap) + 4)
    draw_shadow(screen, board_rect)

    for r in range(3):
        for c in range(3):
            val = board[r][c]
            x = ox + c * (cell + gap)
            y = oy + r * (cell + gap)

            # Choose tile color
            if val == 0:
                color = cfg.TILE_EMPTY
                border_color = cfg.GRAY_MID
            elif (r, c) in correct_tiles:
                color_light = (70, 180, 80)
                color_dark = cfg.TILE_CORRECT
                color = color_light
                border_color = cfg.GREEN_BRIGHT
            elif (r, c) == highlight:
                color = cfg.TILE_HIGHLIGHT
                border_color = cfg.BLUE_BRIGHT
            else:
                color_light = (75, 75, 110)
                color_dark = cfg.TILE_DEFAULT
                color = color_light
                border_color = cfg.GRAY_MID

            rect = pygame.Rect(x, y, cell, cell)
            draw_shadow(screen, rect, offset=2, radius=8)
            draw_rect_gradient(screen, rect, color_light if 'color_light' in dir() else color, color_dark if 'color_dark' in dir() else color)
            pygame.draw.rect(screen, border_color, rect, width=2, border_radius=8)

            if val != 0:
                text = cfg.FONT_LARGE.render(str(val), True, cfg.WHITE)
                screen.blit(text, text.get_rect(center=(x + cell // 2, y + cell // 2)))


# ── Grid ──

def draw_grid(screen, grid, robot_pos, ox, oy, dust_particles=None):
    """Draw vacuum grid with enhanced visuals."""
    rows, cols = grid.shape
    cell = cfg.GRID_CELL_SIZE
    gap = cfg.GRID_GAP

    for r in range(rows):
        for c in range(cols):
            x = ox + c * (cell + gap)
            y = oy + r * (cell + gap)

            if (r, c) == robot_pos:
                color = cfg.BLUE
            elif grid[r][c] == 1:
                color = cfg.DUST_COLOR
            elif grid[r][c] == 2:
                color = cfg.GRAY_LIGHT
            else:
                color = cfg.BG_MID

            rect = pygame.Rect(x, y, cell, cell)
            pygame.draw.rect(screen, color, rect, border_radius=4)
            pygame.draw.rect(screen, cfg.BG_LIGHT, rect, width=1, border_radius=4)

            if (r, c) == robot_pos:
                draw_robot(screen, (x + cell // 2, y + cell // 2), cell // 2 - 4, cfg.ROBOT_PLAYER)
            elif grid[r][c] == 1:
                # Animated dust dot
                pulse = 1.0 + 0.15 * math.sin(pygame.time.get_ticks() / 300)
                r_dot = int((cell // 4) * pulse)
                center = (x + cell // 2, y + cell // 2)
                draw_glow(screen, center, r_dot + 2, cfg.DUST_COLOR, 40)
                pygame.draw.circle(screen, cfg.DUST_GLOW, center, r_dot)


def draw_robot(screen, center, radius, color):
    """Draw a vacuum cleaner robot with wheels, body, and details."""
    cx, cy = center
    r = radius

    # ── Shadow ──
    pygame.draw.ellipse(screen, (0, 0, 0, 60),
        (cx - r + 2, cy + r // 3, r * 2 - 4, r // 2))

    # ── Rear wheels ──
    wheel_w, wheel_h = r // 3, r // 2
    wheel_y = cy + r // 4
    # Left wheel
    pygame.draw.rect(screen, (30, 30, 40),
        (cx - r + r // 5, wheel_y, wheel_w, wheel_h), border_radius=3)
    pygame.draw.rect(screen, cfg.GRAY_MID,
        (cx - r + r // 5 + 2, wheel_y + 2, wheel_w - 4, wheel_h - 4), border_radius=2)
    # Right wheel
    pygame.draw.rect(screen, (30, 30, 40),
        (cx + r - r // 5 - wheel_w, wheel_y, wheel_w, wheel_h), border_radius=3)
    pygame.draw.rect(screen, cfg.GRAY_MID,
        (cx + r - r // 5 - wheel_w + 2, wheel_y + 2, wheel_w - 4, wheel_h - 4), border_radius=2)

    # ── Main body (rounded polygon) ──
    body_points = [
        (cx - r, cy - r // 3),        # top-left
        (cx - r + r // 4, cy - r),     # upper-left
        (cx + r - r // 4, cy - r),     # upper-right
        (cx + r, cy - r // 3),         # top-right
        (cx + r, cy + r // 2),         # bottom-right
        (cx - r, cy + r // 2),         # bottom-left
    ]
    # Body gradient layers
    for i, (darken) in enumerate([0, 10, 20]):
        body_color = tuple(max(0, c - darken) for c in color)
        offset_body = [(px, py + i) for px, py in body_points]
        pygame.draw.polygon(screen, body_color, offset_body)

    # Body border
    pygame.draw.polygon(screen, tuple(min(255, c + 40) for c in color), body_points, width=2)

    # ── Front bumper ──
    bumper_y = cy + r // 2
    bumper_rect = pygame.Rect(cx - r + 3, bumper_y - 2, r * 2 - 6, r // 5)
    pygame.draw.rect(screen, (50, 50, 60), bumper_rect, border_radius=3)

    # ── Dust container (top rectangle) ──
    container_w = r * 2 // 3
    container_h = r // 4
    container_rect = pygame.Rect(cx - container_w // 2, cy - r - container_h + 2,
                                  container_w, container_h)
    pygame.draw.rect(screen, (60, 60, 75), container_rect, border_radius=3)
    pygame.draw.rect(screen, color, container_rect, width=1, border_radius=3)

    # ── LED indicator ──
    led_x, led_y = cx, cy - r // 2
    blink = 0.6 + 0.4 * math.sin(pygame.time.get_ticks() / 200)
    led_color = (int(255 * blink), int(100 * blink), 0)
    draw_glow(screen, (led_x, led_y), r // 5, led_color, 60)
    pygame.draw.circle(screen, led_color, (led_x, led_y), r // 6)

    # ── Eyes (on the body) ──
    eye_y = cy - r // 4
    eye_r = max(2, r // 6)
    eye_spacing = r // 3
    # Left eye
    pygame.draw.circle(screen, cfg.WHITE, (cx - eye_spacing, eye_y), eye_r)
    pygame.draw.circle(screen, cfg.BLACK, (cx - eye_spacing, eye_y), eye_r // 2)
    # Right eye
    pygame.draw.circle(screen, cfg.WHITE, (cx + eye_spacing, eye_y), eye_r)
    pygame.draw.circle(screen, cfg.BLACK, (cx + eye_spacing, eye_y), eye_r // 2)


def draw_vacuum_large(screen, center, size, direction="right"):
    """Draw a large detailed vacuum cleaner for title screens."""
    cx, cy = center
    # Simple scale: size is roughly the body width
    draw_robot(screen, center, size, cfg.BLUE)
    # Add suction effect particles below
    if pygame.time.get_ticks() % 500 < 300:
        for i in range(3):
            px = cx - size // 3 + i * size // 3
            py = cy + size // 2 + 5 + i * 4
            pygame.draw.circle(screen, cfg.CYAN_BRIGHT, (int(px), int(py)), 2)


def draw_scientist(screen, center, size):
    """Draw a scientist/researcher character for the menu."""
    cx, cy = center
    s = size  # scale

    # Lab coat (body)
    coat_color = (220, 225, 235)
    coat_rect = pygame.Rect(cx - s // 2, cy - s // 3, s, s // 2 + s // 3)
    pygame.draw.rect(screen, coat_color, coat_rect, border_radius=s // 4)
    pygame.draw.rect(screen, (180, 185, 195), coat_rect, width=2, border_radius=s // 4)

    # Head
    head_r = s // 3
    head_y = cy - s // 3 - head_r // 2
    pygame.draw.circle(screen, (255, 220, 180), (cx, int(head_y)), head_r)
    pygame.draw.circle(screen, (200, 170, 140), (cx, int(head_y)), head_r, width=2)

    # Glasses
    glass_r = head_r // 2
    glass_y = int(head_y - 2)
    pygame.draw.circle(screen, (50, 50, 60), (cx - glass_r // 2, glass_y), glass_r // 2, width=2)
    pygame.draw.circle(screen, (50, 50, 60), (cx + glass_r // 2, glass_y), glass_r // 2, width=2)
    # Bridge
    pygame.draw.line(screen, (50, 50, 60),
        (cx - glass_r // 2 + glass_r // 2, glass_y),
        (cx + glass_r // 2 - glass_r // 2, glass_y), 2)

    # Clipboard
    board_rect = pygame.Rect(cx - s, cy - s // 4, s // 2, s // 2 + s // 6)
    pygame.draw.rect(screen, (180, 160, 120), board_rect, border_radius=4)
    pygame.draw.rect(screen, (140, 120, 90), board_rect, width=2, border_radius=4)
    # Paper lines
    for i in range(3):
        ly = board_rect.y + s // 6 + i * s // 8
        pygame.draw.line(screen, (160, 140, 110),
            (board_rect.x + 6, ly), (board_rect.x + board_rect.width - 6, ly), 1)


# ── Buttons ──

def draw_button(screen, rect, text, color=cfg.BLUE, hover=False, enabled=True):
    """Draw a styled button with gradient and glow."""
    if not enabled:
        color = cfg.GRAY_MID

    # Shadow (hidden on hover)
    if not hover:
        draw_shadow(screen, rect, offset=3, radius=8)

    # Glow on hover
    if hover and enabled:
        glow_rect = rect.inflate(6, 6)
        draw_glow(screen, glow_rect.center, max(rect.width, rect.height) // 2 + 4, color, 50)

    # Gradient fill
    color_top = color
    color_bottom = tuple(max(0, c - 40) for c in color)
    if hover and enabled:
        color_top = tuple(min(255, c + 30) for c in color)
        color_bottom = tuple(max(0, c - 20) for c in color)

    draw_rect_gradient(screen, rect, color_top, color_bottom)

    # Border
    border_color = cfg.WHITE if hover else tuple(min(255, c + 40) for c in color)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=8)

    # Text
    text_color = cfg.WHITE if enabled else (120, 120, 130)
    label = cfg.FONT_NORMAL.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=rect.center))


# ── Panels ──

def draw_panel(screen, rect, color=None):
    """Draw a panel background with gradient."""
    if color is None:
        color = cfg.SIDEBAR_BG
    draw_rect_gradient(screen, rect, color, tuple(max(0, c - 15) for c in color))
    pygame.draw.rect(screen, cfg.BG_LIGHT, rect, width=1, border_radius=8)


# ── Text ──

def draw_text(screen, text, x, y, font=None, color=None, shadow=True):
    """Draw text with optional shadow for readability."""
    if font is None: font = cfg.FONT_NORMAL
    if color is None: color = cfg.WHITE
    if shadow:
        shadow_surf = font.render(text, True, (0, 0, 0, 120))
        screen.blit(shadow_surf, (x + 1, y + 1))
    screen.blit(font.render(text, True, color), (x, y))


def draw_text_centered(screen, text, rect, font=None, color=None):
    """Draw text centered in a rect."""
    if font is None: font = cfg.FONT_NORMAL
    if color is None: color = cfg.WHITE
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=rect.center))


# ── Progress ──

def draw_progress_bar(screen, x, y, w, h, pct, color=cfg.GREEN, bg_color=None):
    """Draw a styled progress bar."""
    if bg_color is None:
        bg_color = cfg.BG_MID
    bg = pygame.Rect(x, y, w, h)

    # Background with gradient
    draw_rect_gradient(screen, bg, bg_color, tuple(max(0, c - 10) for c in bg_color))
    pygame.draw.rect(screen, cfg.GRAY_MID, bg, width=1, border_radius=4)

    if pct > 0:
        fill_w = int(w * min(pct, 1.0))
        if fill_w > 4:
            fill_rect = pygame.Rect(x, y, fill_w, h)
            color_top = color
            color_bottom = tuple(max(0, c - 30) for c in color)
            draw_rect_gradient(screen, fill_rect, color_top, color_bottom)
            pygame.draw.rect(screen, tuple(min(255, c + 50) for c in color), fill_rect, width=1, border_radius=4)


# ── Modal ──

class Modal:
    """Reusable modal overlay with title, body text, and action buttons."""

    def __init__(self, title, body_lines, buttons, width=420, height=None):
        """
        title: str
        body_lines: list of (text, color) tuples
        buttons: list of (label, action_key, color) tuples
        """
        self.title = title
        self.body_lines = body_lines
        self.buttons = buttons
        self.width = width
        self.height = height or (120 + len(body_lines) * 24 + len(buttons) * 50)
        self.rect = None
        self.button_rects = []
        self.result = None

    def layout(self, screen):
        sw, sh = screen.get_width(), screen.get_height()
        mw, mh = self.width, self.height
        self.rect = pygame.Rect((sw - mw) // 2, (sh - mh) // 2, mw, mh)

        self.button_rects = []
        total_bw = len(self.buttons) * 180 + max(0, len(self.buttons) - 1) * 16
        bx = self.rect.centerx - total_bw // 2
        by = self.rect.bottom - 60
        for label, action, color in self.buttons:
            r = pygame.Rect(bx, by, 180, 40)
            self.button_rects.append((r, action, color))
            bx += 196

    def handle_click(self, pos):
        for rect, action, _ in self.button_rects:
            if rect.collidepoint(pos):
                self.result = action
                return action
        return None

    def draw(self, screen):
        sw, sh = screen.get_width(), screen.get_height()
        self.layout(screen)

        # Backdrop
        backdrop = pygame.Surface((sw, sh), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 160))
        screen.blit(backdrop, (0, 0))

        # Modal background
        draw_rect_gradient(screen, self.rect, (30, 30, 50), (20, 20, 35))
        pygame.draw.rect(screen, (60, 60, 80), self.rect, width=2, border_radius=12)
        draw_shadow(screen, self.rect, offset=6, radius=12)

        # Title
        title_surf = cfg.FONT_LARGE.render(self.title, True, cfg.CYAN_BRIGHT)
        screen.blit(title_surf, title_surf.get_rect(centerx=self.rect.centerx, top=self.rect.y + 20))

        # Separator
        pygame.draw.line(screen, cfg.GRAY_MID,
            (self.rect.x + 30, self.rect.y + 60),
            (self.rect.right - 30, self.rect.y + 60), 1)

        # Body
        y = self.rect.y + 80
        for text, color in self.body_lines:
            if not text.strip():
                y += 12  # spacer line
                continue
            font = cfg.FONT_SMALL if text.startswith("  ") else cfg.FONT_NORMAL
            surf = font.render(text, True, color)
            screen.blit(surf, surf.get_rect(centerx=self.rect.centerx, y=y))
            y += 28

        # Buttons
        mouse = pygame.mouse.get_pos()
        for rect, _, color in self.button_rects:
            hover = rect.collidepoint(mouse)
            draw_button(screen, rect, "", color, hover)
            label = [b[0] for b in self.buttons if b[1] == _][0]
            lbl = cfg.FONT_NORMAL.render(label, True, cfg.WHITE)
            screen.blit(lbl, lbl.get_rect(center=rect.center))


# ── Particles ──

def draw_star_burst(screen, center, count=8, color=None, size=15):
    """Draw a star burst effect."""
    if color is None:
        color = cfg.YELLOW
    cx, cy = center
    t = pygame.time.get_ticks() / 200
    for i in range(count):
        angle = (i / count) * math.pi * 2 + t
        dist = size * (0.6 + 0.4 * math.sin(t * 3 + i))
        px = cx + math.cos(angle) * dist
        py = cy + math.sin(angle) * dist
        s = max(1, int(3 * (1.0 - dist / size)))
        pygame.draw.circle(screen, color, (int(px), int(py)), s)
