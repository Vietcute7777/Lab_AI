# cleanbot-saga/config.py
"""Constants for CleanBot Saga."""

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TITLE = "CleanBot Saga"

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_DARK = (30, 30, 40)
GRAY_MID = (60, 60, 75)
GRAY_LIGHT = (180, 180, 190)
BLUE = (74, 144, 217)
BLUE_DARK = (40, 80, 140)
GREEN = (80, 200, 80)
RED = (220, 60, 60)
YELLOW = (240, 180, 30)
ORANGE = (255, 150, 30)
PURPLE = (160, 80, 220)
CYAN = (60, 200, 200)

# Layout
SIDEBAR_WIDTH = 350
MAIN_AREA_X = SIDEBAR_WIDTH + 20

# Puzzle
PUZZLE_CELL_SIZE = 80
PUZZLE_GAP = 4

# Grid (Vacuum)
GRID_CELL_SIZE = 50
GRID_GAP = 2

# Animation (ms per step)
SPEEDS = {1: 400, 2: 200, 4: 50}

# Scoring
AP_BASE = 20
DUST_POINTS = 200
AP_REMAINING_POINTS = 50
OPTIMAL_ALGO_BONUS = 500

# Fonts (loaded at runtime)
FONT_SMALL = None
FONT_NORMAL = None
FONT_LARGE = None
FONT_TITLE = None
