# cleanbot-saga/main.py
"""CleanBot Saga — Entry point."""
import pygame
import sys
import config as cfg


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
    running = True

    while running:
        dt = clock.tick(cfg.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(cfg.GRAY_DARK)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
