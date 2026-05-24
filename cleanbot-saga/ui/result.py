# cleanbot-saga/ui/result.py
"""Result screen showing score and stars after both phases."""
import pygame
import config as cfg
from core.game_state import state, Phase, GameMode
from core.storage import load_campaign, save_campaign
from ui.renderer import draw_button, draw_text, draw_panel, Modal


class ResultScreen:
    def __init__(self):
        self.continue_rect = None
        self.retry_rect = None
        self.modal = None

    def enter(self):
        self.modal = None
        if state.stars == 3:
            self.modal = Modal(
                title="CHÚC MỪNG!",
                body_lines=[
                    ("Bạn đã đạt ⭐⭐⭐ xuất sắc!", cfg.YELLOW),
                    (f"Tổng điểm: {state.score}", cfg.CYAN_BRIGHT),
                ],
                buttons=[("TUYỆT VỜI!", "close", cfg.GREEN)],
                height=220,
            )
        if state.mode == GameMode.CAMPAIGN:
            self._save_campaign_progress()

    def _save_campaign_progress(self):
        data = load_campaign()
        lvl = state.current_level
        old_stars = data["stars"].get(str(lvl), 0)
        if state.stars > old_stars:
            data["stars"][str(lvl)] = state.stars
        if state.stars >= 1 and data["level_completed"] < lvl:
            data["level_completed"] = lvl
        data["total_score"] = data.get("total_score", 0) + state.score
        save_campaign(data)
        state.total_stars = sum(data["stars"].values())

    def handle_click(self, pos):
        if self.modal:
            result = self.modal.handle_click(pos)
            if result:
                self.modal = None
            return None  # block underlying clicks while modal is open
        if self.continue_rect and self.continue_rect.collidepoint(pos):
            return "continue"
        if self.retry_rect and self.retry_rect.collidepoint(pos):
            return "retry"
        return None

    def draw(self, screen):
        mx, my = cfg.MARGIN_X, cfg.MARGIN_Y
        sw = screen.get_width()
        screen.fill(cfg.BG_DARK)
        draw_text(screen, "KẾT QUẢ", mx, my + 10, cfg.FONT_TITLE, cfg.CYAN)

        # ── Results card ──
        card_x, card_y = mx + cfg.PADDING_LARGE, my + 90
        card_w, card_h = 500, 320
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)
        draw_panel(screen, card_rect)

        y = card_y + cfg.PADDING_LARGE
        x = card_x + cfg.PADDING_XL + 10

        draw_text(screen, f"Bụi đã hút: {state.dust_cleaned} / {state.total_dust}", x, y, cfg.FONT_LARGE)
        y += cfg.PADDING_XL
        ap_remain = max(0, state.action_points - state.robot_steps_taken)
        draw_text(screen, f"AP còn dư: {ap_remain}", x, y, cfg.FONT_LARGE)
        y += cfg.PADDING_XL
        opt_text = "Có" if state.optimal_algo_chosen else "Không"
        opt_color = cfg.GREEN if state.optimal_algo_chosen else cfg.RED
        draw_text(screen, f"Thuật toán tối ưu: {opt_text}", x, y, cfg.FONT_LARGE, opt_color)
        y += cfg.PADDING_XL + 10
        draw_text(screen, f"TỔNG ĐIỂM: {state.score}", x, y, cfg.FONT_TITLE, cfg.ORANGE)
        y += 60
        stars_text = "⭐" * state.stars + "☆" * (3 - state.stars)
        draw_text(screen, stars_text, x, y, cfg.FONT_TITLE, cfg.YELLOW)

        if state.stars == 3:
            from ui.renderer import draw_star_burst
            draw_star_burst(screen, (sw // 2, 480), count=12, color=cfg.YELLOW, size=80)

        # ── Buttons ──
        cx = sw // 2
        bw, bh, gap = cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT, cfg.PADDING_MEDIUM
        btn_y = card_rect.bottom + 40
        self.continue_rect = pygame.Rect(cx - bw - gap, btn_y, bw, bh)
        self.retry_rect = pygame.Rect(cx + gap, btn_y, bw, bh)

        mouse = pygame.mouse.get_pos()
        draw_button(screen, self.continue_rect, "TIẾP TỤC",
                    cfg.GREEN, self.continue_rect.collidepoint(mouse))
        draw_button(screen, self.retry_rect, "CHƠI LẠI",
                    cfg.BLUE, self.retry_rect.collidepoint(mouse))

        if self.modal:
            self.modal.draw(screen)
