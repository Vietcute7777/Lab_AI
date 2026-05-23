# cleanbot-saga/ui/result.py
"""Result screen showing score and stars after both phases."""
import pygame
import config as cfg
from core.game_state import state, Phase, GameMode
from core.storage import load_campaign, save_campaign
from ui.renderer import draw_button, draw_text


class ResultScreen:
    def __init__(self):
        self.continue_rect = None
        self.retry_rect = None

    def enter(self):
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
        if self.continue_rect and self.continue_rect.collidepoint(pos):
            return "continue"
        if self.retry_rect and self.retry_rect.collidepoint(pos):
            return "retry"
        return None

    def draw(self, screen):
        screen.fill(cfg.GRAY_DARK)
        draw_text(screen, "KẾT QUẢ", 20, 40, cfg.FONT_TITLE, cfg.CYAN)

        y = 130
        draw_text(screen, f"Bụi đã hút: {state.dust_cleaned} / {state.total_dust}", 100, y, cfg.FONT_LARGE)
        y += 40
        ap_remain = max(0, state.action_points - state.robot_steps_taken)
        draw_text(screen, f"AP còn dư: {ap_remain}", 100, y, cfg.FONT_LARGE)
        y += 40
        opt_text = "Có" if state.optimal_algo_chosen else "Không"
        opt_color = cfg.GREEN if state.optimal_algo_chosen else cfg.RED
        draw_text(screen, f"Thuật toán tối ưu: {opt_text}", 100, y, cfg.FONT_LARGE, opt_color)
        y += 50
        draw_text(screen, f"TỔNG ĐIỂM: {state.score}", 100, y, cfg.FONT_TITLE, cfg.ORANGE)
        y += 60
        stars_text = "⭐" * state.stars + "☆" * (3 - state.stars)
        draw_text(screen, stars_text, 100, y, cfg.FONT_TITLE, cfg.YELLOW)

        # Buttons
        cx = screen.get_width() // 2
        bw, bh = 250, 50
        self.continue_rect = pygame.Rect(cx - bw - 20, 550, bw, bh)
        self.retry_rect = pygame.Rect(cx + 20, 550, bw, bh)

        mouse = pygame.mouse.get_pos()
        draw_button(screen, self.continue_rect, "TIẾP TỤC",
                    cfg.GREEN, self.continue_rect.collidepoint(mouse))
        draw_button(screen, self.retry_rect, "CHƠI LẠI",
                    cfg.BLUE, self.retry_rect.collidepoint(mouse))
