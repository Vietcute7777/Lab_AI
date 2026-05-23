# cleanbot-saga/main.py
"""CleanBot Saga — Entry point with full game loop."""
import pygame
import sys
import config as cfg
from core.game_state import state, GameMode, Phase
from core.storage import load_elo
from ui.menu import MainMenu
from ui.phase1 import Phase1Screen
from ui.phase2 import Phase2Screen
from ui.result import ResultScreen
from ui.daily import generate_daily_puzzle, generate_daily_grid, start_daily
from campaign.levels import get_level


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

    # Screens
    menu = MainMenu()
    phase1 = Phase1Screen()
    phase2 = Phase2Screen()
    result = ResultScreen()

    # Load saved state
    state.pve_elo = load_elo()

    # "Next Phase" button tracking
    next_phase_rect = pygame.Rect(410, 470, 200, 40)
    view_result_rect = pygame.Rect(410, 590, 200, 40)

    while running:
        dt = clock.tick(cfg.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                # ── MENU ──
                if state.phase == Phase.MENU:
                    mode = menu.handle_click(pos)
                    if mode == GameMode.CAMPAIGN:
                        state.mode = GameMode.CAMPAIGN
                        rows, cols, dust, shuffle = get_level(state.current_level)
                        phase1.enter(shuffle_steps=shuffle)
                        state.phase = Phase.PHASE1_PUZZLE
                    elif mode == GameMode.DAILY:
                        ok, msg = start_daily()
                        if ok:
                            board = generate_daily_puzzle()
                            state.puzzle_board = board
                            state.puzzle_initial = [row[:] for row in board]
                            state.grid_map = generate_daily_grid()
                            phase1.enter()
                            state.phase = Phase.PHASE1_PUZZLE
                        else:
                            print(f"Daily: {msg}")
                    elif mode == GameMode.PVE:
                        state.mode = GameMode.PVE
                        phase1.enter(shuffle_steps=25)
                        state.phase = Phase.PHASE1_PUZZLE

                # ── PHASE 1 ──
                elif state.phase == Phase.PHASE1_PUZZLE:
                    phase1.handle_click(pos)
                    # Check for "Next Phase" button
                    if phase1.mode == "done" and state.action_points > 0:
                        if next_phase_rect.collidepoint(pos):
                            if state.mode == GameMode.CAMPAIGN:
                                rows, cols, dust, _ = get_level(state.current_level)
                            elif state.mode == GameMode.PVE:
                                rows, cols, dust = 7, 9, 20
                            else:  # DAILY
                                rows, cols, dust = 7, 9, 20
                            phase2.enter(rows=rows, cols=cols, dust_count=dust)
                            state.phase = Phase.PHASE2_VACUUM

                # ── PHASE 2 ──
                elif state.phase == Phase.PHASE2_VACUUM:
                    phase2.handle_click(pos)
                    # Check for "View Results" button
                    if phase2.mode == "done":
                        if view_result_rect.collidepoint(pos):
                            result.enter()
                            state.phase = Phase.RESULT

                # ── RESULT ──
                elif state.phase == Phase.RESULT:
                    action = result.handle_click(pos)
                    if action == "continue":
                        state.phase = Phase.MENU
                        if state.mode == GameMode.CAMPAIGN and state.stars >= 1:
                            if state.current_level < 15:
                                state.current_level += 1
                    elif action == "retry":
                        if state.mode == GameMode.CAMPAIGN:
                            rows, cols, dust, shuffle = get_level(state.current_level)
                            phase1.enter(shuffle_steps=shuffle)
                        elif state.mode == GameMode.DAILY:
                            board = generate_daily_puzzle()
                            state.puzzle_board = board
                            state.puzzle_initial = [row[:] for row in board]
                            phase1.enter()
                        elif state.mode == GameMode.PVE:
                            phase1.enter(shuffle_steps=25)
                        state.phase = Phase.PHASE1_PUZZLE

        # ── UPDATE ANIMATIONS ──
        if state.phase == Phase.PHASE1_PUZZLE and phase1.mode == "running":
            phase1.update()
        if state.phase == Phase.PHASE2_VACUUM and phase2.mode == "running":
            phase2.update()

        # ── DRAW ──
        screen.fill(cfg.GRAY_DARK)

        if state.phase == Phase.MENU:
            menu.draw(screen)

        elif state.phase == Phase.PHASE1_PUZZLE:
            phase1.draw(screen)
            # "Next Phase" transition button
            if phase1.mode == "done" and state.action_points > 0:
                from ui.renderer import draw_button as db2
                mouse = pygame.mouse.get_pos()
                db2(screen, next_phase_rect, "QUA PHA 2 >>",
                    cfg.GREEN, next_phase_rect.collidepoint(mouse))

        elif state.phase == Phase.PHASE2_VACUUM:
            phase2.draw(screen)
            # "View Results" transition button
            if phase2.mode == "done":
                from ui.renderer import draw_button as db3
                mouse = pygame.mouse.get_pos()
                db3(screen, view_result_rect, "XEM KET QUA >>",
                    cfg.ORANGE, view_result_rect.collidepoint(mouse))

        elif state.phase == Phase.RESULT:
            result.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
