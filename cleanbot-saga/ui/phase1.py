# cleanbot-saga/ui/phase1.py
"""Phase 1: select algorithm, watch AI solve 8-puzzle with step-by-step animation."""
import pygame
import config as cfg
from core.game_state import state, Phase
from core.scoring import calculate_ap
from core.storage import get_unlocked_solvers
from puzzle import puzzle_registry
from puzzle.board import generate_board, apply_move, GOAL, is_goal
from puzzle.heuristic import manhattan_distance
from ui.renderer import draw_puzzle_board, draw_button, draw_panel, draw_text, Modal
from ui.log_panel import LogPanel
from ui.controls import GameControls


class Phase1Screen:
    def __init__(self):
        self.log = LogPanel(cfg.PANEL_X, 310, cfg.PANEL_WIDTH - 20, 400)
        self.controls = GameControls(cfg.MID_X, 420)
        self.solver_rects = []
        self.solver_list = []
        self.mode = "select"
        self.solution_path = []
        self.current_step = 0
        self.current_board = None
        self.last_step_time = 0
        self.nodes_explored = 0
        self.comparison = []
        self.modal = None
        self.transition_confirmed = False

    def show_transition_modal(self):
        self.modal = Modal(
            title="XÁC NHẬN",
            body_lines=[
                ("Bạn có chắc muốn sang Phase 2?", cfg.WHITE),
                ("AP sẽ được dùng để điều khiển robot.", cfg.GRAY_LIGHT),
            ],
            buttons=[("HỦY", "cancel", cfg.RED), ("XÁC NHẬN", "confirm", cfg.GREEN)],
            height=240,
        )

    def enter(self, shuffle_steps=10):
        state.reset_phase1()
        state.puzzle_board = generate_board(shuffle_steps)
        state.puzzle_initial = [row[:] for row in state.puzzle_board]
        self.current_board = [row[:] for row in state.puzzle_board]
        self.mode = "select"
        self.solution_path = []
        self.current_step = 0
        self.log.clear()
        self._build_solver_list()

    def _build_solver_list(self):
        unlocked = get_unlocked_solvers()
        self.solver_list = []
        self.solver_rects = []
        y = 200
        for s in puzzle_registry.list_all():
            enabled = s.id in unlocked
            self.solver_list.append((s, enabled))
            self.solver_rects.append(pygame.Rect(cfg.MID_X, y, cfg.MID_WIDTH, cfg.BUTTON_HEIGHT))
            y += cfg.BUTTON_HEIGHT + cfg.BUTTON_GAP

    def handle_click(self, pos):
        if self.modal:
            result = self.modal.handle_click(pos)
            if result == "confirm":
                self.transition_confirmed = True
                self.modal = None
            elif result == "cancel":
                self.modal = None
            return
        if self.mode == "select":
            for i, rect in enumerate(self.solver_rects):
                if rect.collidepoint(pos) and self.solver_list[i][1]:
                    self._start_solver(self.solver_list[i][0])
                    return
        action = self.controls.handle_click(pos)
        if action == "play":
            state.anim_paused = not state.anim_paused
            self.last_step_time = pygame.time.get_ticks()
        elif action and action.startswith("speed_"):
            state.anim_speed = int(action.split("_")[1])
            self.last_step_time = pygame.time.get_ticks()

    def _start_solver(self, solver_info):
        state.selected_solver_id = solver_info.id
        self.log.clear()
        self.log.add(f"Đã chọn: {solver_info.name}")
        self.log.add("Đang chạy thuật toán...")
        path, nodes = solver_info.solve(state.puzzle_initial)
        self.solution_path = path
        self.nodes_explored = nodes
        self.current_step = 0
        self.current_board = [row[:] for row in state.puzzle_initial]
        if path:
            self.mode = "running"
            state.animating = True
            state.anim_paused = False
            self.last_step_time = pygame.time.get_ticks()
        else:
            self.log.add_complete(False, "Không tìm thấy lời giải")
            self.mode = "done"
            state.action_points = 0

    def update(self):
        if self.mode != "running" or state.anim_paused:
            return
        if self.current_step >= len(self.solution_path):
            return
        now = pygame.time.get_ticks()
        if now - self.last_step_time < state.speed_ms:
            return
        self.last_step_time = now

        direction = self.solution_path[self.current_step]
        self.current_board = apply_move(self.current_board, direction)
        self.current_step += 1

        h = manhattan_distance(self.current_board)
        self.log.add_move(self.current_step, direction, f"h={h}")

        if self.current_step >= len(self.solution_path):
            self._finish()

    def _finish(self):
        self.mode = "done"
        state.animating = False
        steps = len(self.solution_path)
        state.action_points = calculate_ap(steps)
        self.log.add_complete(True, f"{steps} bước, AP={state.action_points}")
        self.log.add(f"Nodes đã duyệt: {self.nodes_explored}")
        unlocked = get_unlocked_solvers()
        self.comparison = []
        for s in puzzle_registry.list_all():
            if s.id in unlocked:
                p, n = s.solve(state.puzzle_initial)
                self.comparison.append((s.name, len(p) if p else "-", n, s.category == "optimal"))
        self.comparison.sort(key=lambda x: x[1] if isinstance(x[1], int) else 999)

    def draw(self, screen):
        screen.fill(cfg.BG_DARK)
        mx, my = cfg.MARGIN_X, cfg.MARGIN_Y
        draw_text(screen, "PHA 1: GIẢI 8-PUZZLE", mx, my, cfg.FONT_LARGE, cfg.CYAN)

        if self.current_board:
            draw_puzzle_board(screen, self.current_board, mx + 10, my + 50)
            draw_text(screen, "Đích:", mx + 10, my + 340, cfg.FONT_SMALL, cfg.GRAY_LIGHT)
            draw_puzzle_board(screen, GOAL, mx + 10, my + 360)

        draw_panel(screen, pygame.Rect(cfg.PANEL_X, 0, cfg.PANEL_WIDTH, cfg.SCREEN_HEIGHT))

        if self.mode == "select":
            draw_text(screen, "CHỌN THUẬT TOÁN:", cfg.MID_X, 170, cfg.FONT_NORMAL, cfg.WHITE)
            mouse = pygame.mouse.get_pos()
            for i, (s, enabled) in enumerate(self.solver_list):
                rect = self.solver_rects[i]
                hover = rect.collidepoint(mouse)
                color = cfg.GREEN if s.category == "optimal" else cfg.BLUE
                draw_button(screen, rect, s.name, color, hover, enabled)

        if self.mode == "done":
            self._draw_comparison(screen)

        elif self.mode == "running":
            s = puzzle_registry.get(state.selected_solver_id)
            draw_text(screen, f"Đang chạy: {s.name}", cfg.MID_X, 170, cfg.FONT_SMALL, cfg.CYAN)
            draw_text(screen, f"Bước: {self.current_step}/{len(self.solution_path)}",
                      cfg.MID_X, 195, cfg.FONT_SMALL, cfg.WHITE)

        self.log.draw(screen)
        if self.mode in ("running", "done"):
            self.controls.draw(screen)

        if self.modal:
            self.modal.draw(screen)

    def _draw_comparison(self, screen):
        x, y = cfg.MID_X, 170
        draw_text(screen, "KẾT QUẢ SO SÁNH:", x, y, cfg.FONT_NORMAL, cfg.CYAN)
        y += cfg.PADDING_LARGE
        headers = ["Thuật toán", "Bước", "Nodes", "Tối ưu"]
        col_starts = [0, 160, 220, 280]
        for label, cs in zip(headers, col_starts):
            screen.blit(cfg.FONT_SMALL.render(label, True, cfg.GRAY_LIGHT), (x + cs, y))
        y += 20
        for name, steps, nodes, is_opt in self.comparison:
            is_sel = (name == puzzle_registry.get(state.selected_solver_id).name if state.selected_solver_id else False)
            color = cfg.GREEN if is_sel else cfg.WHITE
            screen.blit(cfg.FONT_SMALL.render(name, True, color), (x, y))
            screen.blit(cfg.FONT_SMALL.render(str(steps), True, color), (x + 160, y))
            screen.blit(cfg.FONT_SMALL.render(str(nodes), True, color), (x + 220, y))
            screen.blit(cfg.FONT_SMALL.render("Có" if is_opt else "Không", True, cfg.GREEN if is_opt else cfg.RED), (x + 280, y))
            y += 20
        y += cfg.PADDING_MEDIUM
        ap_text = cfg.FONT_LARGE.render(f"AP nhận được: {state.action_points}", True, cfg.ORANGE)
        screen.blit(ap_text, (x, y))
