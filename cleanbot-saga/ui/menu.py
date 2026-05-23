# cleanbot-saga/ui/menu.py
"""Main menu screen."""
import pygame
import config as cfg
from core.game_state import state, GameMode
from core.storage import load_campaign, load_elo
from ui.renderer import draw_button


class MainMenu:
    def __init__(self):
        self.button_rects = []
        self.button_defs = []

    def layout(self, screen):
        cx = screen.get_width() // 2
        bw, bh, gap = 300, 50, 16
        camp = load_campaign()
        lvl = camp.get("level_completed", 0)
        stars = sum(camp.get("stars", {}).values())
        pve_unlocked = stars >= 20

        self.button_defs = [
            ("CHIEN DICH (Campaign)", GameMode.CAMPAIGN, True,
             f"Man {lvl + 1} | Tong ⭐: {stars}"),
            ("DAILY CHALLENGE", GameMode.DAILY, True,
             "1 ngay — 1 co hoi"),
            ("PVE ARENA", GameMode.PVE, pve_unlocked,
             f"Elo: {load_elo()}" if pve_unlocked else "Can >= 20⭐ de mo khoa"),
        ]
        self.button_rects = []
        y = screen.get_height() // 2 - 90
        for _ in self.button_defs:
            self.button_rects.append(pygame.Rect(cx - bw // 2, y, bw, bh))
            y += bh + gap

    def handle_click(self, pos):
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos) and self.button_defs[i][2]:
                return self.button_defs[i][1]
        return None

    def draw(self, screen):
        self.layout(screen)
        screen.fill(cfg.GRAY_DARK)
        cx = screen.get_width() // 2

        title = cfg.FONT_TITLE.render("CLEANBOT SAGA", True, cfg.CYAN)
        screen.blit(title, title.get_rect(centerx=cx, y=80))

        sub = cfg.FONT_NORMAL.render(
            "Game Chien Thuat AI — Giai 8-Puzzle & Dieu Khien Robot Hut Bui",
            True, cfg.GRAY_LIGHT)
        screen.blit(sub, sub.get_rect(centerx=cx, y=140))

        mouse = pygame.mouse.get_pos()
        for i, (label, mode, enabled, desc) in enumerate(self.button_defs):
            rect = self.button_rects[i]
            hover = rect.collidepoint(mouse)
            colors = {GameMode.CAMPAIGN: cfg.BLUE, GameMode.DAILY: cfg.ORANGE,
                      GameMode.PVE: cfg.RED if enabled else cfg.GRAY_MID}
            draw_button(screen, rect, label, colors.get(mode, cfg.BLUE), hover, enabled)
            d = cfg.FONT_SMALL.render(desc, True, cfg.GRAY_LIGHT if enabled else cfg.RED)
            screen.blit(d, d.get_rect(centerx=rect.centerx, top=rect.bottom + 4))
