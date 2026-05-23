# cleanbot-saga/ui/controls.py
"""Play/Pause/Speed control buttons."""
import pygame
import config as cfg
from core.game_state import state


class GameControls:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.bw, self.bh = 90, 36

    def get_buttons(self):
        btns = []
        bx = self.x
        label = "Tam dung" if (state.animating and not state.anim_paused) else "Chay"
        btns.append((pygame.Rect(bx, self.y, self.bw, self.bh), label, "play"))
        bx += self.bw + 8
        for sp, lbl in [(1, "1x"), (2, "2x"), (4, "4x")]:
            btns.append((pygame.Rect(bx, self.y, 50, self.bh), lbl, f"speed_{sp}"))
            bx += 58
        return btns

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        from ui.renderer import draw_button
        for rect, text, _ in self.get_buttons():
            hover = rect.collidepoint(mouse)
            is_active = text == f"{state.anim_speed}x"
            color = cfg.GREEN if is_active else cfg.BLUE
            draw_button(screen, rect, text, color=color, hover=hover)

    def handle_click(self, pos):
        for rect, _, action in self.get_buttons():
            if rect.collidepoint(pos):
                return action
        return None
