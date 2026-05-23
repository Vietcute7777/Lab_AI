# cleanbot-saga/ui/phase2.py
"""Phase 2: select pathfinding algorithm, watch robot clean step by step."""
import pygame
import config as cfg
from core.game_state import state, Phase
from core.storage import get_unlocked_algos
from vacuum import pathfinding_registry
from vacuum.grid import create_grid, count_dust
from vacuum.robot import Robot
from ui.renderer import draw_grid, draw_button, draw_panel, draw_text, draw_progress_bar
from ui.log_panel import LogPanel
from ui.controls import GameControls


class Phase2Screen:
    def __init__(self):
        self.log = LogPanel(850, 310, 330, 400)
        self.controls = GameControls(410, 540)
        self.algo_rects = []
        self.algo_list = []
        self.mode = "select"
        self.robot = None
        self.current_event_idx = 0
        self.all_events = []
        self.last_step_time = 0
        self.grid_rows = 5
        self.grid_cols = 7

    def enter(self, rows=5, cols=7, dust_count=10):
        state.reset_phase2()
        self.grid_rows, self.grid_cols = rows, cols
        state.grid_map = create_grid(rows, cols, dust_count)
        state.total_dust = count_dust(state.grid_map)
        state.grid_map[0, 0] = 0
        state.robot_pos = (0, 0)
        self.robot = Robot(state.grid_map, (0, 0))
        self.mode = "select"
        self.all_events = []
        self.current_event_idx = 0
        self.log.clear()
        self._build_algo_list()

    def _build_algo_list(self):
        unlocked = get_unlocked_algos()
        self.algo_list = []
        self.algo_rects = []
        y = 200
        for a in pathfinding_registry.list_all():
            enabled = a.id in unlocked
            self.algo_list.append((a, enabled))
            self.algo_rects.append(pygame.Rect(410, y, 330, 40))
            y += 50

    def handle_click(self, pos):
        if self.mode == "select":
            for i, rect in enumerate(self.algo_rects):
                if rect.collidepoint(pos) and self.algo_list[i][1]:
                    self._start_algo(self.algo_list[i][0])
                    return
        action = self.controls.handle_click(pos)
        if action == "play":
            state.anim_paused = not state.anim_paused
            self.last_step_time = pygame.time.get_ticks()
        elif action and action.startswith("speed_"):
            state.anim_speed = int(action.split("_")[1])
            self.last_step_time = pygame.time.get_ticks()

    def _start_algo(self, algo_info):
        state.selected_algo_id = algo_info.id
        self.log.clear()
        self.log.add(f"Da chon: {algo_info.name}")
        self.log.add(f"AP: {state.action_points} | Bui: {state.total_dust}")
        self.mode = "running"
        state.animating = True
        state.anim_paused = False
        self.last_step_time = pygame.time.get_ticks()
        self._find_and_queue_next_path()

    def _find_and_queue_next_path(self):
        remain = count_dust(self.robot.grid)
        if remain == 0 or self.robot.steps_taken >= state.action_points:
            self._finish()
            return
        algo = pathfinding_registry.get(state.selected_algo_id)
        self.log.add_search(algo.name)
        path = algo.find_path(self.robot.grid, self.robot.pos)
        if not path:
            self._finish()
            return
        events = self.robot.follow_path(path)
        self.all_events.extend(events)
        self.current_event_idx = 0

    def update(self):
        if self.mode != "running" or state.anim_paused:
            return
        if self.current_event_idx >= len(self.all_events):
            self._find_and_queue_next_path()
            return
        now = pygame.time.get_ticks()
        if now - self.last_step_time < state.speed_ms:
            return
        self.last_step_time = now

        pos, evt_type = self.all_events[self.current_event_idx]
        self.current_event_idx += 1
        state.robot_pos = pos
        state.robot_steps_taken = self.robot.steps_taken

        direction = self.robot.direction
        if evt_type == "clean":
            state.dust_cleaned = self.robot.dust_cleaned
            self.log.add_clean(pos, state.dust_cleaned, state.total_dust)
        else:
            self.log.add_move(self.robot.steps_taken, direction)

        if self.robot.steps_taken >= state.action_points:
            self._finish()
        elif state.dust_cleaned >= state.total_dust:
            self._finish()

    def _finish(self):
        self.mode = "done"
        state.animating = False
        state.dust_cleaned = self.robot.dust_cleaned
        ap_remain = state.action_points - self.robot.steps_taken
        from core.scoring import check_optimal_algo, calculate_score, calculate_stars
        state.optimal_algo_chosen = check_optimal_algo(state.selected_solver_id, state.selected_algo_id)
        state.score = calculate_score(state.dust_cleaned, max(0, ap_remain), state.optimal_algo_chosen)
        state.stars = calculate_stars(state.dust_cleaned, state.total_dust, state.optimal_algo_chosen)
        self.log.add_complete(state.dust_cleaned >= state.total_dust,
            f"Bui: {state.dust_cleaned}/{state.total_dust} | Diem: {state.score} | ⭐{state.stars}")

    def draw(self, screen):
        screen.fill(cfg.GRAY_DARK)
        draw_text(screen, "PHA 2: ĐIỀU KHIỂN ROBOT HÚT BỤI", 20, 20, cfg.FONT_LARGE, cfg.CYAN)
        draw_text(screen, f"AP: {state.action_points} | Đã hút: {state.dust_cleaned}/{state.total_dust}",
                  20, 55, cfg.FONT_NORMAL, cfg.ORANGE)

        if state.grid_map is not None:
            ox = 50
            oy = 90
            draw_grid(screen, self.robot.grid if self.robot else state.grid_map,
                      state.robot_pos, ox, oy)

        draw_panel(screen, pygame.Rect(850, 0, 350, 800))

        if self.mode == "select":
            draw_text(screen, "CHỌN THUẬT TOÁN:", 410, 170, cfg.FONT_NORMAL, cfg.WHITE)
            mouse = pygame.mouse.get_pos()
            for i, (a, enabled) in enumerate(self.algo_list):
                rect = self.algo_rects[i]
                hover = rect.collidepoint(mouse)
                color = cfg.GREEN if a.category == "optimal" else cfg.BLUE
                draw_button(screen, rect, a.name, color, hover, enabled)

        elif self.mode == "running":
            a = pathfinding_registry.get(state.selected_algo_id)
            draw_text(screen, f"Thuật toán: {a.name}", 410, 170, cfg.FONT_SMALL, cfg.CYAN)
            draw_text(screen, f"Bước: {self.robot.steps_taken}/{state.action_points}",
                      410, 195, cfg.FONT_SMALL, cfg.WHITE)
            pct = state.dust_cleaned / max(state.total_dust, 1)
            draw_progress_bar(screen, 410, 215, 250, 16, pct, cfg.YELLOW)

        elif self.mode == "done":
            self._draw_result(screen)

        self.log.draw(screen)
        if self.mode in ("running", "done"):
            self.controls.draw(screen)

    def _draw_result(self, screen):
        x, y = 410, 170
        draw_text(screen, "KẾT QUẢ", x, y, cfg.FONT_LARGE, cfg.CYAN)
        y += 40
        draw_text(screen, f"Bụi đã hút: {state.dust_cleaned} / {state.total_dust}", x, y)
        y += 25
        draw_text(screen, f"AP còn dư: {state.action_points - self.robot.steps_taken}", x, y)
        y += 25
        draw_text(screen, f"Thuật toán tối ưu: {'Có' if state.optimal_algo_chosen else 'Không'}",
                  x, y, color=cfg.GREEN if state.optimal_algo_chosen else cfg.RED)
        y += 25
        draw_text(screen, f"Điểm: {state.score}", x, y, cfg.FONT_LARGE, cfg.ORANGE)
        y += 35
        stars_text = "⭐" * state.stars + "☆" * (3 - state.stars)
        draw_text(screen, stars_text, x, y, cfg.FONT_TITLE, cfg.YELLOW)
