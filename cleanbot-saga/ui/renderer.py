# cleanbot-saga/ui/renderer.py
"""Pygame rendering: puzzle, grid, buttons, text."""
import pygame
import config as cfg


def draw_puzzle_board(screen, board, ox, oy):
    cell = cfg.PUZZLE_CELL_SIZE
    gap = cfg.PUZZLE_GAP
    for r in range(3):
        for c in range(3):
            val = board[r][c]
            x = ox + c * (cell + gap)
            y = oy + r * (cell + gap)
            pygame.draw.rect(screen, cfg.GRAY_MID, (x, y, cell, cell), border_radius=8)
            if val != 0:
                t = cfg.FONT_LARGE.render(str(val), True, cfg.WHITE)
                screen.blit(t, t.get_rect(center=(x + cell // 2, y + cell // 2)))


def draw_grid(screen, grid, robot_pos, ox, oy):
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
                color = cfg.YELLOW
            elif grid[r][c] == 2:
                color = cfg.GRAY_LIGHT
            else:
                color = cfg.GRAY_MID

            pygame.draw.rect(screen, color, (x, y, cell, cell), border_radius=4)

            if (r, c) == robot_pos:
                t = cfg.FONT_LARGE.render("R", True, cfg.WHITE)
                screen.blit(t, t.get_rect(center=(x + cell // 2, y + cell // 2)))
            elif grid[r][c] == 1:
                pygame.draw.circle(screen, (180, 120, 20),
                    (x + cell // 2, y + cell // 2), cell // 4)


def draw_button(screen, rect, text, color=cfg.BLUE, hover=False, enabled=True):
    border = cfg.WHITE if hover else color
    fill = color if enabled else cfg.GRAY_MID
    pygame.draw.rect(screen, fill, rect, border_radius=6)
    pygame.draw.rect(screen, border, rect, width=2, border_radius=6)
    label = cfg.FONT_NORMAL.render(text, True, cfg.WHITE if enabled else cfg.GRAY_LIGHT)
    screen.blit(label, label.get_rect(center=rect.center))
    return rect


def draw_panel(screen, rect, color=cfg.GRAY_DARK):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, cfg.GRAY_MID, rect, width=1, border_radius=8)


def draw_text(screen, text, x, y, font=None, color=None):
    if font is None: font = cfg.FONT_NORMAL
    if color is None: color = cfg.WHITE
    screen.blit(font.render(text, True, color), (x, y))


def draw_text_centered(screen, text, rect, font=None, color=None):
    if font is None: font = cfg.FONT_NORMAL
    if color is None: color = cfg.WHITE
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=rect.center))


def draw_progress_bar(screen, x, y, w, h, pct, color=cfg.GREEN):
    bg = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, cfg.GRAY_MID, bg, border_radius=4)
    if pct > 0:
        fill = pygame.Rect(x, y, int(w * min(pct, 1.0)), h)
        pygame.draw.rect(screen, color, fill, border_radius=4)
    pygame.draw.rect(screen, cfg.GRAY_LIGHT, bg, width=1, border_radius=4)
