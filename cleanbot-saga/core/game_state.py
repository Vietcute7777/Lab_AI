# cleanbot-saga/core/game_state.py
"""Game state machine."""
from enum import Enum, auto


class GameMode(Enum):
    MENU = auto()
    CAMPAIGN = auto()
    DAILY = auto()
    PVE = auto()


class Phase(Enum):
    MENU = auto()
    PHASE1_PUZZLE = auto()
    PHASE2_VACUUM = auto()
    RESULT = auto()


class GameState:
    def __init__(self):
        self.mode = GameMode.MENU
        self.phase = Phase.MENU
        self.current_level = 1
        self.total_stars = 0

        # Phase 1
        self.puzzle_board = None
        self.puzzle_initial = None
        self.selected_solver_id = None
        self.action_points = 0

        # Phase 2
        self.grid_map = None
        self.robot_pos = (0, 0)
        self.selected_algo_id = None
        self.dust_cleaned = 0
        self.total_dust = 0
        self.robot_steps_taken = 0

        # Result
        self.score = 0
        self.stars = 0
        self.optimal_algo_chosen = False

        # Animation
        self.animating = False
        self.anim_speed = 2
        self.anim_paused = False

        # PvE
        self.pve_elo = 1200

    @property
    def speed_ms(self):
        from config import SPEEDS
        return SPEEDS.get(self.anim_speed, 200)

    def reset_phase1(self):
        self.puzzle_board = None
        self.selected_solver_id = None
        self.action_points = 0

    def reset_phase2(self):
        self.grid_map = None
        self.robot_pos = (0, 0)
        self.selected_algo_id = None
        self.dust_cleaned = 0
        self.total_dust = 0
        self.robot_steps_taken = 0

    def reset_result(self):
        self.score = 0
        self.stars = 0
        self.optimal_algo_chosen = False


state = GameState()
