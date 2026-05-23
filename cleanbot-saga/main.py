# cleanbot-saga/main.py
"""CleanBot Saga — Entry point with Menu."""
import pygame
import sys
import config as cfg
from core.game_state import state, GameMode, Phase
from ui.menu import MainMenu


def init_pygame():
    pygame.init()
    cfg.FONT_SMALL = pygame.font.Font(None, 18)
    cfg.FONT_NORMAL = pygame.font.Font(None, 24)
    cfg.FONT_LARGE = pygame.font.Font(None, 32)
    cfg.FONT_TITLE = pygame.font.Font(None, 48)
    return pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))


def main():
    screen = init_pygame()
    pygame.display.set_caption(cfg.TITLE)
    clock = pygame.time.Clock()
    menu = MainMenu()
    running = True

    while running:
        dt = clock.tick(cfg.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state.phase == Phase.MENU:
                    mode = menu.handle_click(event.pos)
                    if mode:
                        state.mode = mode
                        print(f"Selected mode: {mode}")

        if state.phase == Phase.MENU:
            menu.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
