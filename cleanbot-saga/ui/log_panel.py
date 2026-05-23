# cleanbot-saga/ui/log_panel.py
"""Scrollable log panel for algorithm step-by-step output."""
import pygame
import config as cfg


class LogPanel:
    MAX_LINES = 20

    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.entries = []  # [(text, color), ...]

    def clear(self):
        self.entries = []

    def add(self, text, color=cfg.WHITE):
        self.entries.append((text, color))
        if len(self.entries) > self.MAX_LINES:
            self.entries = self.entries[-self.MAX_LINES:]

    def add_move(self, step, direction, detail=""):
        msg = f"Buoc {step}: {direction}"
        if detail: msg += f" - {detail}"
        self.add(msg, cfg.BLUE)

    def add_clean(self, pos, cleaned, total):
        self.add(f"  >> HUT BUI tai ({pos[0]},{pos[1]})! {cleaned}/{total}", cfg.YELLOW)

    def add_search(self, algo_name):
        self.add(f"  [Tim duong: {algo_name}...]", cfg.CYAN)

    def add_complete(self, success, info=""):
        color = cfg.GREEN if success else cfg.RED
        self.add(f"{'HOAN THANH' if success else 'THAT BAI'}! {info}", color)

    def draw(self, screen):
        pygame.draw.rect(screen, cfg.BLACK, self.rect, border_radius=6)
        pygame.draw.rect(screen, cfg.GRAY_MID, self.rect, width=1, border_radius=6)

        title = cfg.FONT_NORMAL.render("NHAT KY THUAT TOAN", True, cfg.CYAN)
        screen.blit(title, (self.rect.x + 10, self.rect.y + 6))

        line_y = self.rect.y + 32
        for text, color in self.entries[-18:]:
            if line_y + 18 > self.rect.bottom - 10:
                break
            screen.blit(cfg.FONT_SMALL.render(text, True, color), (self.rect.x + 10, line_y))
            line_y += 18
