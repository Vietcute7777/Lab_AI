# cleanbot-saga/ui/menu.py
"""Main menu screen."""
import math
import pygame
import config as cfg
from core.game_state import state, GameMode
from core.storage import load_campaign, load_elo
from ui.renderer import draw_button, draw_scientist, draw_glow, Modal


class MainMenu:
    def __init__(self):
        self.button_rects = []
        self.button_defs = []
        self.modal = None
        self.info_rect = None

    def layout(self, screen):
        cx = screen.get_width() // 2
        bw, bh, gap = cfg.BUTTON_WIDTH + 40, cfg.BUTTON_HEIGHT, cfg.BUTTON_GAP + 4
        camp = load_campaign()
        lvl = camp.get("level_completed", 0)
        stars = sum(camp.get("stars", {}).values())
        pve_unlocked = stars >= 20

        self.button_defs = [
            ("CHIẾN DỊCH (Campaign)", GameMode.CAMPAIGN, True,
             f"Màn {lvl + 1} | Tổng ⭐: {stars}"),
            ("DAILY CHALLENGE", GameMode.DAILY, True,
             "1 ngày — 1 cơ hội"),
            ("PVE ARENA", GameMode.PVE, pve_unlocked,
             f"Elo: {load_elo()}" if pve_unlocked else "Cần >= 20⭐ để mở khóa"),
        ]
        self.button_rects = []
        y = screen.get_height() // 2 - 40
        for _ in self.button_defs:
            self.button_rects.append(pygame.Rect(cx - bw // 2, y, bw, bh))
            y += bh + gap

        # Info button in top-right corner
        self.info_rect = pygame.Rect(screen.get_width() - 50, 12, 36, 36)

    def _show_info_modal(self):
        self.modal = Modal(
            title="HƯỚNG DẪN",
            body_lines=[
                ("🧩 Phase 1: Giải 8-Puzzle", cfg.CYAN),
                ("  Chọn thuật toán AI, xem nó giải.", cfg.GRAY_LIGHT),
                ("  Nhận AP để dùng ở Phase 2.", cfg.GRAY_LIGHT),
                ("", cfg.GRAY_LIGHT),
                ("🤖 Phase 2: Hút bụi bằng Robot", cfg.CYAN),
                ("  Dùng AP để điều khiển robot.", cfg.GRAY_LIGHT),
                ("  Chọn thuật toán tìm đường tối ưu.", cfg.GRAY_LIGHT),
                ("", cfg.GRAY_LIGHT),
                ("🏆 Kết quả: Tính điểm và xếp hạng sao.", cfg.CYAN),
                ("  Tối ưu hóa để đạt 3⭐!", cfg.YELLOW),
            ],
            buttons=[("ĐÃ HIỂU", "close", cfg.GREEN)],
            width=480,
            height=420,
        )

    def handle_click(self, pos):
        if self.modal:
            result = self.modal.handle_click(pos)
            if result:
                self.modal = None
            return None
        if self.info_rect and self.info_rect.collidepoint(pos):
            self._show_info_modal()
            return None
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos) and self.button_defs[i][2]:
                return self.button_defs[i][1]
        return None

    def draw(self, screen):
        self.layout(screen)
        # Animated gradient background
        t = pygame.time.get_ticks() / 3000
        for y in range(screen.get_height()):
            r = int(18 + 3 * math.sin(y * 0.01 + t))
            g = int(18 + 3 * math.sin(y * 0.015 + t + 1))
            b = int(30 + 5 * math.sin(y * 0.02 + t + 2))
            pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))

        cx = screen.get_width() // 2

        # ── Decorative characters ──
        # Scientist on the left
        draw_scientist(screen, (100, screen.get_height() - 250), 100)
        # Glow behind title
        draw_glow(screen, (cx, 105), 200, cfg.CYAN, 30)

        # ── Title ──
        title_shadow = cfg.FONT_TITLE.render("CLEANBOT SAGA", True, (0, 0, 0))
        screen.blit(title_shadow, title_shadow.get_rect(centerx=cx + 2, y=82))
        title = cfg.FONT_TITLE.render("CLEANBOT SAGA", True, cfg.CYAN_BRIGHT)
        screen.blit(title, title.get_rect(centerx=cx, y=80))

        # ── Subtitle ──
        sub = cfg.FONT_NORMAL.render(
            "Game Chiến Thuật AI — Giải 8-Puzzle & Điều Khiển Robot Hút Bụi",
            True, cfg.GRAY_LIGHT)
        screen.blit(sub, sub.get_rect(centerx=cx, y=145))

        # ── Separator line ──
        sep_y = 175
        pygame.draw.line(screen, cfg.GRAY_MID, (cx - 220, sep_y), (cx + 220, sep_y), 1)

        # ── Buttons ──
        mouse = pygame.mouse.get_pos()
        for i, (label, mode, enabled, desc) in enumerate(self.button_defs):
            rect = self.button_rects[i]
            hover = rect.collidepoint(mouse)
            colors = {GameMode.CAMPAIGN: cfg.BLUE, GameMode.DAILY: cfg.ORANGE,
                      GameMode.PVE: cfg.RED if enabled else cfg.GRAY_MID}
            draw_button(screen, rect, label, colors.get(mode, cfg.BLUE), hover, enabled)
            d = cfg.FONT_SMALL.render(desc, True, cfg.GRAY_LIGHT if enabled else cfg.RED)
            screen.blit(d, d.get_rect(centerx=rect.centerx, top=rect.bottom + 4))

        # ── Info button (top right) ──
        if self.info_rect:
            mouse = pygame.mouse.get_pos()
            hover = self.info_rect.collidepoint(mouse)
            pygame.draw.rect(screen, cfg.GRAY_MID if not hover else cfg.BLUE,
                             self.info_rect, border_radius=8)
            pygame.draw.rect(screen, cfg.WHITE if hover else cfg.GRAY_LIGHT,
                             self.info_rect, width=2, border_radius=8)
            lbl = cfg.FONT_NORMAL.render("?", True, cfg.WHITE)
            screen.blit(lbl, lbl.get_rect(center=self.info_rect.center))

        # ── Version / footer ──
        footer = cfg.FONT_SMALL.render("AI Lab 2026 — CleanBot Saga v1.0", True, cfg.GRAY_MID)
        screen.blit(footer, footer.get_rect(centerx=cx, bottom=screen.get_height() - cfg.MARGIN_Y))

        # ── Modal on top ──
        if self.modal:
            self.modal.draw(screen)
