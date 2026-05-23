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
    """Draw a cute robot icon."""
    cx, cy = center
    # Body
    pygame.draw.circle(screen, color, (cx, cy), radius)
    # Eyes
    eye_r = max(2, radius // 4)
    pygame.draw.circle(screen, cfg.WHITE, (cx - radius // 3, cy - radius // 3), eye_r)
    pygame.draw.circle(screen, cfg.WHITE, (cx + radius // 3, cy - radius // 3), eye_r)
    # Pupils
    pygame.draw.circle(screen, cfg.BLACK, (cx - radius // 3, cy - radius // 3), eye_r // 2)
    pygame.draw.circle(screen, cfg.BLACK, (cx + radius // 3, cy - radius // 3), eye_r // 2)
    # Antenna
    antenna_y = cy - radius - 2
    pygame.draw.line(screen, color, (cx, cy - radius), (cx, antenna_y), 2)
    pygame.draw.circle(screen, cfg.YELLOW, (cx, antenna_y), 3)


# ── Buttons ──

def draw_button(screen, rect, text, color=cfg.BLUE, hover=False, enabled=True):
    """Draw a styled button with gradient and glow."""
    if not enabled:
        color = cfg.GRAY_MID

    # Shadow
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
