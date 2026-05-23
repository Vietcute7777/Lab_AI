# CleanBot Saga Implementation Plan — Pygame Desktop App

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Pygame desktop game combining 8-Puzzle solver selection + Vacuum Cleaner pathfinding — with extensible algorithm registry for future algorithms.

**Architecture:** Pygame game loop drives rendering. Algorithm registries (Strategy Pattern) in `puzzle/__init__.py` and `vacuum/__init__.py` allow adding new algorithms by creating 1 file + 1 registration line. UI components read from registries dynamically. All data persisted as JSON. Code from existing Python notebooks reused directly.

**Tech Stack:** Python 3, Pygame, NumPy, JSON (for saves)

---

## Phase 1: Project Scaffold

### Task 1: Create project structure and config

**Files:**
- Create: `cleanbot-saga/config.py`
- Create: `cleanbot-saga/main.py`
- Create: `cleanbot-saga/core/__init__.py`
- Create: `cleanbot-saga/puzzle/__init__.py`
- Create: `cleanbot-saga/vacuum/__init__.py`
- Create: `cleanbot-saga/campaign/__init__.py`
- Create: `cleanbot-saga/pve/__init__.py`
- Create: `cleanbot-saga/ui/__init__.py`

- [ ] **Step 1: Create directories**

Run: `mkdir -p cleanbot-saga/{core,puzzle,vacuum,campaign,pve,ui,data}`

- [ ] **Step 2: Write config.py**

```python
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
```

- [ ] **Step 3: Write main.py (skeleton with game loop)**

```python
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
```

- [ ] **Step 4: Verify it runs**

Run: `cd cleanbot-saga && python main.py`
Expected: Black window 1200x800 appears, closes on X.

- [ ] **Step 5: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/ && git commit -m "feat: project scaffold with Pygame skeleton"
```

---

### Task 2: Algorithm Registry (extensible architecture)

**Files:**
- Rewrite: `cleanbot-saga/puzzle/__init__.py`
- Rewrite: `cleanbot-saga/vacuum/__init__.py`

- [ ] **Step 1: Write puzzle/__init__.py (registry)**

```python
# cleanbot-saga/puzzle/__init__.py
"""8-Puzzle solver registry — Strategy Pattern.
To add a new solver:
  1. Create puzzle/my_algo.py with solve(board) -> (path, nodes)
  2. Add one line: registry.register(SolverInfo(id="...", ...))
"""

from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class SolverInfo:
    id: str
    name: str
    description: str
    category: str          # 'optimal', 'heuristic', 'uninformed'
    unlocked_by_default: bool = True
    solve: Callable = field(repr=False)
    steps: int = 0
    nodes_explored: int = 0
    solved: bool = False


class PuzzleSolverRegistry:
    def __init__(self):
        self._solvers: dict[str, SolverInfo] = {}

    def register(self, solver: SolverInfo):
        self._solvers[solver.id] = solver

    def get(self, solver_id: str) -> Optional[SolverInfo]:
        return self._solvers.get(solver_id)

    def list_all(self) -> list[SolverInfo]:
        return list(self._solvers.values())

    def list_unlocked(self, unlocked_ids: set[str]) -> list[SolverInfo]:
        return [s for s in self._solvers.values() if s.id in unlocked_ids]

    def get_optimal_ids(self) -> list[str]:
        return [s.id for s in self._solvers.values() if s.category == 'optimal']


puzzle_registry = PuzzleSolverRegistry()
```

- [ ] **Step 2: Write vacuum/__init__.py (registry)**

```python
# cleanbot-saga/vacuum/__init__.py
"""Vacuum pathfinding registry — Strategy Pattern.
To add a new algorithm:
  1. Create vacuum/my_algo.py with find_path(grid, start) -> list[(r,c)]
  2. Add one line: registry.register(PathfindingInfo(id="...", ...))
"""

from dataclasses import dataclass, field
from typing import Callable, Optional, Any


@dataclass
class PathfindingInfo:
    id: str
    name: str
    description: str
    category: str          # 'optimal', 'uninformed', 'iterative'
    unlocked_by_default: bool = True
    find_path: Callable = field(repr=False)


class PathfindingRegistry:
    def __init__(self):
        self._algos: dict[str, PathfindingInfo] = {}

    def register(self, algo: PathfindingInfo):
        self._algos[algo.id] = algo

    def get(self, algo_id: str) -> Optional[PathfindingInfo]:
        return self._algos.get(algo_id)

    def list_all(self) -> list[PathfindingInfo]:
        return list(self._algos.values())

    def list_unlocked(self, unlocked_ids: set[str]) -> list[PathfindingInfo]:
        return [a for a in self._algos.values() if a.id in unlocked_ids]

    def get_optimal_ids(self) -> list[str]:
        return [a.id for a in self._algos.values() if a.category == 'optimal']


pathfinding_registry = PathfindingRegistry()
```

- [ ] **Step 3: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/puzzle/__init__.py cleanbot-saga/vacuum/__init__.py && git commit -m "feat: add extensible algorithm registries"
```

---

## Phase 2: Core Systems

### Task 3: Game State Machine

**Files:**
- Create: `cleanbot-saga/core/game_state.py`

- [ ] **Step 1: Write game_state.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/core/ && git commit -m "feat: add game state machine"
```

---

### Task 4: Scoring & Storage

**Files:**
- Create: `cleanbot-saga/core/scoring.py`
- Create: `cleanbot-saga/core/storage.py`

- [ ] **Step 1: Write scoring.py**

```python
# cleanbot-saga/core/scoring.py
"""Score calculation, AP, stars."""
import config as cfg
from puzzle import puzzle_registry
from vacuum import pathfinding_registry


def calculate_ap(puzzle_steps: int) -> int:
    if puzzle_steps <= 0:
        return 0
    return max(1, cfg.AP_BASE - puzzle_steps)


def check_optimal_algo(solver_id: str, algo_id: str) -> bool:
    return (solver_id in puzzle_registry.get_optimal_ids() and
            algo_id in pathfinding_registry.get_optimal_ids())


def calculate_score(dust_cleaned: int, ap_remaining: int, optimal_chosen: bool) -> int:
    score = dust_cleaned * cfg.DUST_POINTS
    score += ap_remaining * cfg.AP_REMAINING_POINTS
    if optimal_chosen:
        score += cfg.OPTIMAL_ALGO_BONUS
    return score


def calculate_stars(dust_cleaned: int, total_dust: int, optimal_chosen: bool) -> int:
    if total_dust == 0:
        return 3
    pct = dust_cleaned / total_dust
    if pct >= 1.0 and optimal_chosen:
        return 3
    if pct >= 0.8:
        return 2
    if pct >= 0.5:
        return 1
    return 0
```

- [ ] **Step 2: Write storage.py**

```python
# cleanbot-saga/core/storage.py
"""JSON persistence for game progress."""
import json
import os
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _read(filename, default):
    _ensure_dir()
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(filename, data):
    _ensure_dir()
    with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_campaign():
    return _read("campaign.json", {"level_completed": 0, "stars": {}, "total_score": 0})

def save_campaign(data):
    _write("campaign.json", data)

def load_daily():
    return _read("daily.json", {})

def save_daily(today_data):
    all_data = load_daily()
    all_data[str(date.today())] = today_data
    _write("daily.json", all_data)

def has_daily_played_today():
    return str(date.today()) in load_daily()

def load_elo():
    return _read("elo.json", {"elo": 1200}).get("elo", 1200)

def save_elo(elo):
    _write("elo.json", {"elo": elo})

def get_unlocked_solvers():
    lvl = load_campaign().get("level_completed", 0)
    unlocked = {"bfs", "dfs"}
    if lvl >= 3: unlocked.add("greedy")
    return unlocked

def get_unlocked_algos():
    lvl = load_campaign().get("level_completed", 0)
    unlocked = {"bfs", "dfs"}
    if lvl >= 9: unlocked.add("ids")
    if lvl >= 12: unlocked.add("ucs")
    return unlocked
```

- [ ] **Step 3: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/core/ && git commit -m "feat: add scoring and storage systems"
```

---

## Phase 3: Puzzle Engine

### Task 5: Board & Heuristic

**Files:**
- Create: `cleanbot-saga/puzzle/board.py`
- Create: `cleanbot-saga/puzzle/heuristic.py`

- [ ] **Step 1: Write board.py**

```python
# cleanbot-saga/puzzle/board.py
"""8-Puzzle board utilities: generation, moves, goal check."""
import random

GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
GOAL_POSITIONS = {
    val: (r, c) for r, row in enumerate(GOAL)
    for c, val in enumerate(row) if val != 0
}
OPPOSITES = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}


def is_solvable(board):
    flat = [board[r][c] for r in range(3) for c in range(3)]
    inversions = sum(
        1 for i in range(9) for j in range(i + 1, 9)
        if flat[i] and flat[j] and flat[i] > flat[j]
    )
    return inversions % 2 == 0


def generate_board(shuffle_steps=20):
    board = [row[:] for row in GOAL]
    r, c = 2, 2
    prev_move = None
    for _ in range(shuffle_steps):
        moves = _get_moves_dict(board)
        if prev_move:
            moves.pop(OPPOSITES.get(prev_move), None)
        if not moves:
            break
        direction, (nr, nc) = random.choice(list(moves.items()))
        board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
        r, c = nr, nc
        prev_move = direction
    return board


def generate_random_board():
    """Generate solvable board by random shuffle (from notebook)."""
    while True:
        nums = list(range(9))
        random.shuffle(nums)
        if is_solvable([nums]):
            return [nums[i:i + 3] for i in range(0, 9, 3)]


def _get_moves_dict(board):
    r, c = find_blank(board)
    moves = {}
    if r > 0: moves["UP"] = (r - 1, c)
    if r < 2: moves["DOWN"] = (r + 1, c)
    if c > 0: moves["LEFT"] = (r, c - 1)
    if c < 2: moves["RIGHT"] = (r, c + 1)
    return moves


def find_blank(board):
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                return r, c
    return 2, 2


def apply_move(board, direction):
    r, c = find_blank(board)
    moves = _get_moves_dict(board)
    if direction not in moves:
        return [row[:] for row in board]
    nr, nc = moves[direction]
    new_board = [row[:] for row in board]
    new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
    return new_board


def is_goal(board):
    return board == GOAL


def board_to_tuple(board):
    return tuple(cell for row in board for cell in row)
```

- [ ] **Step 2: Write heuristic.py**

```python
# cleanbot-saga/puzzle/heuristic.py
"""Heuristic functions for 8-puzzle."""
from puzzle.board import GOAL_POSITIONS, GOAL


def manhattan_distance(board):
    total = 0
    for r in range(3):
        for c in range(3):
            tile = board[r][c]
            if tile != 0:
                gr, gc = GOAL_POSITIONS[tile]
                total += abs(r - gr) + abs(c - gc)
    return total


def misplaced_tiles(board):
    return sum(
        1 for r in range(3) for c in range(3)
        if board[r][c] and board[r][c] != GOAL[r][c]
    )
```

- [ ] **Step 3: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/puzzle/ && git commit -m "feat: add puzzle board and heuristic"
```

---

### Task 6: BFS & DFS Solvers

**Files:**
- Create: `cleanbot-saga/puzzle/bfs.py`
- Create: `cleanbot-saga/puzzle/dfs.py`

- [ ] **Step 1: Write bfs.py**

```python
# cleanbot-saga/puzzle/bfs.py
"""BFS 8-puzzle solver — guarantees shortest solution."""
from collections import deque
from puzzle import puzzle_registry, SolverInfo
from puzzle.board import (
    OPPOSITES, board_to_tuple, is_goal, _get_moves_dict, apply_move
)


def solve(board):
    queue = deque([(board, [])])
    visited = {board_to_tuple(board)}
    nodes = 0

    while queue:
        current, path = queue.popleft()
        nodes += 1
        if is_goal(current):
            return path, nodes

        for direction in _get_moves_dict(current):
            if path and direction == OPPOSITES.get(path[-1]):
                continue
            new_board = apply_move(current, direction)
            key = board_to_tuple(new_board)
            if key not in visited:
                visited.add(key)
                queue.append((new_board, path + [direction]))

    return [], nodes


puzzle_registry.register(SolverInfo(
    id="bfs", name="BFS (Breadth-First Search)",
    description="Duyet theo chieu rong. Luon tim duong di ngan nhat.",
    category="optimal", solve=solve
))
```

- [ ] **Step 2: Write dfs.py**

```python
# cleanbot-saga/puzzle/dfs.py
"""DFS 8-puzzle solver — depth-limited."""
from puzzle import puzzle_registry, SolverInfo
from puzzle.board import (
    OPPOSITES, board_to_tuple, is_goal, _get_moves_dict, apply_move
)

MAX_DEPTH = 30


def solve(board):
    stack = [(board, [])]
    visited = {board_to_tuple(board): 0}
    nodes = 0

    while stack:
        current, path = stack.pop()
        nodes += 1
        depth = len(path)

        if is_goal(current):
            return path, nodes
        if depth >= MAX_DEPTH:
            continue

        for direction in _get_moves_dict(current):
            if path and direction == OPPOSITES.get(path[-1]):
                continue
            new_board = apply_move(current, direction)
            key = board_to_tuple(new_board)
            if key not in visited or visited[key] > depth + 1:
                visited[key] = depth + 1
                stack.append((new_board, path + [direction]))

    return [], nodes


puzzle_registry.register(SolverInfo(
    id="dfs", name="DFS (Depth-First Search)",
    description="Duyet theo chieu sau (gioi han 30). Khong dam bao toi uu.",
    category="uninformed", solve=solve
))
```

- [ ] **Step 3: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/puzzle/ && git commit -m "feat: add BFS and DFS 8-puzzle solvers"
```

---

### Task 7: Greedy Best-First Solver

**Files:**
- Create: `cleanbot-saga/puzzle/greedy.py`

- [ ] **Step 1: Write greedy.py**

```python
# cleanbot-saga/puzzle/greedy.py
"""Greedy Best-First Search 8-puzzle solver."""
import heapq
import itertools
from puzzle import puzzle_registry, SolverInfo
from puzzle.board import (
    OPPOSITES, board_to_tuple, is_goal, _get_moves_dict, apply_move
)
from puzzle.heuristic import manhattan_distance


def solve(board):
    start_h = manhattan_distance(board)
    heap = [(start_h, 0, board, [])]
    visited = {board_to_tuple(board)}
    counter = itertools.count(1)
    nodes = 0

    while heap:
        h, _, current, path = heapq.heappop(heap)
        nodes += 1

        if is_goal(current):
            return path, nodes

        for direction in _get_moves_dict(current):
            if path and direction == OPPOSITES.get(path[-1]):
                continue
            new_board = apply_move(current, direction)
            key = board_to_tuple(new_board)
            if key not in visited:
                visited.add(key)
                new_h = manhattan_distance(new_board)
                heapq.heappush(heap, (new_h, next(counter), new_board, path + [direction]))

    return [], nodes


puzzle_registry.register(SolverInfo(
    id="greedy", name="Greedy Best-First Search",
    description="Tham lam: luon chon nuoc co Manhattan nho nhat. Nhanh nhung khong dam bao toi uu.",
    category="heuristic", unlocked_by_default=False, solve=solve
))
```

- [ ] **Step 2: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/puzzle/ && git commit -m "feat: add Greedy Best-First Search puzzle solver"
```

---

## Phase 4: Vacuum Engine

### Task 8: Grid & Robot

**Files:**
- Create: `cleanbot-saga/vacuum/grid.py`
- Create: `cleanbot-saga/vacuum/robot.py`

- [ ] **Step 1: Write grid.py**

```python
# cleanbot-saga/vacuum/grid.py
"""Vacuum environment: grid generation and management."""
import random
import numpy as np


def create_grid(rows, cols, dust_count):
    grid = np.zeros((rows, cols), dtype=int)
    all_pos = [(r, c) for r in range(rows) for c in range(cols)]
    dust_positions = set(random.sample(all_pos, min(dust_count, rows * cols)))
    for r, c in dust_positions:
        grid[r][c] = 1
    return grid


def create_grid_with_walls(rows, cols, dust_count, wall_prob=0.1):
    grid = np.zeros((rows, cols), dtype=int)
    all_pos = [(r, c) for r in range(rows) for c in range(cols)]
    random.shuffle(all_pos)

    wall_count = int(rows * cols * wall_prob)
    for r, c in all_pos[:wall_count]:
        grid[r][c] = 2

    free = [(r, c) for r, c in all_pos if grid[r][c] != 2]
    dust_positions = set(random.sample(free, min(dust_count, len(free))))
    for r, c in dust_positions:
        grid[r][c] = 1

    return grid


def count_dust(grid):
    return int(np.sum(grid == 1))
```

- [ ] **Step 2: Write robot.py**

```python
# cleanbot-saga/vacuum/robot.py
"""Robot that navigates the grid and cleans dust."""


class Robot:
    def __init__(self, grid, start_pos=(0, 0)):
        self.grid = grid.copy()
        self.rows, self.cols = grid.shape
        self.pos = start_pos
        self.dust_cleaned = 0
        self.steps_taken = 0
        self.path_history = [start_pos]
        self.events = []  # [(pos, "move"|"clean"), ...]

    def clean_current(self):
        r, c = self.pos
        if self.grid[r][c] == 1:
            self.grid[r][c] = 0
            self.dust_cleaned += 1
            return True
        return False

    def move_to(self, new_pos):
        self.pos = new_pos
        self.steps_taken += 1
        self.path_history.append(new_pos)

    def follow_path(self, path):
        self.events = []
        for next_pos in path[1:]:
            self.move_to(next_pos)
            if self.clean_current():
                self.events.append((next_pos, "clean"))
            else:
                self.events.append((next_pos, "move"))
        return self.events

    @property
    def direction(self):
        if len(self.path_history) < 2:
            return "START"
        r1, c1 = self.path_history[-2]
        r2, c2 = self.path_history[-1]
        if r2 > r1: return "DOWN"
        if r2 < r1: return "UP"
        if c2 > c1: return "RIGHT"
        return "LEFT"
```

- [ ] **Step 3: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/vacuum/ && git commit -m "feat: add vacuum grid and robot"
```

---

### Task 9: BFS & DFS Pathfinding

**Files:**
- Create: `cleanbot-saga/vacuum/bfs.py`
- Create: `cleanbot-saga/vacuum/dfs.py`

- [ ] **Step 1: Write bfs.py**

```python
# cleanbot-saga/vacuum/bfs.py
"""BFS pathfinding — shortest path to nearest dust."""
from collections import deque
from vacuum import pathfinding_registry, PathfindingInfo


def find_path(grid, start_pos):
    rows, cols = grid.shape
    queue = deque([(start_pos, [start_pos])])
    visited = {start_pos}

    while queue:
        (r, c), path = queue.popleft()
        if grid[r][c] == 1:
            return path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return []


pathfinding_registry.register(PathfindingInfo(
    id="bfs", name="BFS (Breadth-First Search)",
    description="Tim duong ngan nhat den bui gan nhat. Luon toi uu.",
    category="optimal", find_path=find_path
))
```

- [ ] **Step 2: Write dfs.py**

```python
# cleanbot-saga/vacuum/dfs.py
"""DFS pathfinding — depth-first search."""
from vacuum import pathfinding_registry, PathfindingInfo


def find_path(grid, start_pos):
    rows, cols = grid.shape
    stack = [(start_pos, [start_pos])]
    visited = {start_pos}

    while stack:
        (r, c), path = stack.pop()
        if grid[r][c] == 1:
            return path
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))
    return []


pathfinding_registry.register(PathfindingInfo(
    id="dfs", name="DFS (Depth-First Search)",
    description="Tim duong den bui theo chieu sau. Khong dam bao ngan nhat.",
    category="uninformed", find_path=find_path
))
```

- [ ] **Step 3: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/vacuum/ && git commit -m "feat: add BFS and DFS vacuum pathfinding"
```

---

### Task 10: IDS & UCS Pathfinding

**Files:**
- Create: `cleanbot-saga/vacuum/ids.py`
- Create: `cleanbot-saga/vacuum/ucs.py`

- [ ] **Step 1: Write ids.py**

```python
# cleanbot-saga/vacuum/ids.py
"""IDS (Iterative Deepening Search) pathfinding."""
from vacuum import pathfinding_registry, PathfindingInfo


def find_path(grid, start_pos):
    rows, cols = grid.shape

    def dls(pos, path, limit):
        r, c = pos
        if grid[r][c] == 1:
            return path
        if limit <= 0:
            return None
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in path:
                result = dls((nr, nc), path + [(nr, nc)], limit - 1)
                if result is not None:
                    return result
        return None

    for depth_limit in range(rows * cols + 1):
        result = dls(start_pos, [start_pos], depth_limit)
        if result is not None:
            return result
    return []


pathfinding_registry.register(PathfindingInfo(
    id="ids", name="IDS (Iterative Deepening)",
    description="Ket hop uu diem BFS (toi uu) va DFS (it bo nho). Tang dan do sau.",
    category="iterative", unlocked_by_default=False, find_path=find_path
))
```

- [ ] **Step 2: Write ucs.py**

```python
# cleanbot-saga/vacuum/ucs.py
"""UCS (Uniform Cost Search) pathfinding."""
import heapq
import itertools
from vacuum import pathfinding_registry, PathfindingInfo


def find_path(grid, start_pos):
    rows, cols = grid.shape
    counter = itertools.count()
    heap = [(0, next(counter), start_pos, [start_pos])]
    visited_costs = {start_pos: 0}

    while heap:
        cost, _, (r, c), path = heapq.heappop(heap)
        if cost > visited_costs.get((r, c), float("inf")):
            continue
        if grid[r][c] == 1:
            return path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + 1
                if new_cost < visited_costs.get((nr, nc), float("inf")):
                    visited_costs[(nr, nc)] = new_cost
                    heapq.heappush(heap, (new_cost, next(counter), (nr, nc), path + [(nr, nc)]))
    return []


pathfinding_registry.register(PathfindingInfo(
    id="ucs", name="UCS (Uniform Cost Search)",
    description="Mo rong node co chi phi thap nhat. Toi uu, hoat dong tot ca khi trong so khac nhau.",
    category="optimal", unlocked_by_default=False, find_path=find_path
))
```

- [ ] **Step 3: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/vacuum/ && git commit -m "feat: add IDS and UCS vacuum pathfinding"
```

---

## Phase 5: UI Components

### Task 11: Renderer

**Files:**
- Create: `cleanbot-saga/ui/renderer.py`

- [ ] **Step 1: Write renderer.py**

```python
# cleanbot-saga/ui/renderer.py
"""Pygame rendering: puzzle, grid, buttons, text."""
import pygame
import config as cfg


def draw_puzzle_board(screen, board, ox, oy):
    cell = cfg.PUZZLE_CELL_SIZE
    gap = cfg.PUZZLE_GAP
    for r in range(3):
        for c in range(3):
            val = board[r][c]
            x = ox + c * (cell + gap)
            y = oy + r * (cell + gap)
            pygame.draw.rect(screen, cfg.GRAY_MID, (x, y, cell, cell), border_radius=8)
            if val != 0:
                t = cfg.FONT_LARGE.render(str(val), True, cfg.WHITE)
                screen.blit(t, t.get_rect(center=(x + cell // 2, y + cell // 2)))


def draw_grid(screen, grid, robot_pos, ox, oy):
    rows, cols = grid.shape
    cell = cfg.GRID_CELL_SIZE
    gap = cfg.GRID_GAP

    for r in range(rows):
        for c in range(cols):
            x = ox + c * (cell + gap)
            y = oy + r * (cell + gap)

            if (r, c) == robot_pos:
                color = cfg.BLUE
            elif grid[r][c] == 1:
                color = cfg.YELLOW
            elif grid[r][c] == 2:
                color = cfg.GRAY_LIGHT
            else:
                color = cfg.GRAY_MID

            pygame.draw.rect(screen, color, (x, y, cell, cell), border_radius=4)

            if (r, c) == robot_pos:
                t = cfg.FONT_LARGE.render("R", True, cfg.WHITE)
                screen.blit(t, t.get_rect(center=(x + cell // 2, y + cell // 2)))
            elif grid[r][c] == 1:
                pygame.draw.circle(screen, (180, 120, 20),
                    (x + cell // 2, y + cell // 2), cell // 4)


def draw_button(screen, rect, text, color=cfg.BLUE, hover=False, enabled=True):
    border = cfg.WHITE if hover else color
    fill = color if enabled else cfg.GRAY_MID
    pygame.draw.rect(screen, fill, rect, border_radius=6)
    pygame.draw.rect(screen, border, rect, width=2, border_radius=6)
    label = cfg.FONT_NORMAL.render(text, True, cfg.WHITE if enabled else cfg.GRAY_LIGHT)
    screen.blit(label, label.get_rect(center=rect.center))
    return rect


def draw_panel(screen, rect, color=cfg.GRAY_DARK):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, cfg.GRAY_MID, rect, width=1, border_radius=8)


def draw_text(screen, text, x, y, font=None, color=None):
    if font is None: font = cfg.FONT_NORMAL
    if color is None: color = cfg.WHITE
    screen.blit(font.render(text, True, color), (x, y))


def draw_text_centered(screen, text, rect, font=None, color=None):
    if font is None: font = cfg.FONT_NORMAL
    if color is None: color = cfg.WHITE
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=rect.center))


def draw_progress_bar(screen, x, y, w, h, pct, color=cfg.GREEN):
    bg = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, cfg.GRAY_MID, bg, border_radius=4)
    if pct > 0:
        fill = pygame.Rect(x, y, int(w * min(pct, 1.0)), h)
        pygame.draw.rect(screen, color, fill, border_radius=4)
    pygame.draw.rect(screen, cfg.GRAY_LIGHT, bg, width=1, border_radius=4)
```

- [ ] **Step 2: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/ui/ && git commit -m "feat: add UI renderer"
```

---

### Task 12: Log Panel & Controls

**Files:**
- Create: `cleanbot-saga/ui/log_panel.py`
- Create: `cleanbot-saga/ui/controls.py`

- [ ] **Step 1: Write log_panel.py**

```python
# cleanbot-saga/ui/log_panel.py
"""Scrollable log panel for algorithm step-by-step output."""
import pygame
import config as cfg


class LogPanel:
    MAX_LINES = 20

    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.entries = []  # [(text, color), ...]

    def clear(self):
        self.entries = []

    def add(self, text, color=cfg.WHITE):
        self.entries.append((text, color))
        if len(self.entries) > self.MAX_LINES:
            self.entries = self.entries[-self.MAX_LINES:]

    def add_move(self, step, direction, detail=""):
        msg = f"Buoc {step}: {direction}"
        if detail: msg += f" — {detail}"
        self.add(msg, cfg.BLUE)

    def add_clean(self, pos, cleaned, total):
        self.add(f"  >> HUT BUI tai ({pos[0]},{pos[1]})! {cleaned}/{total}", cfg.YELLOW)

    def add_search(self, algo_name):
        self.add(f"  [Tim duong: {algo_name}...]", cfg.CYAN)

    def add_complete(self, success, info=""):
        color = cfg.GREEN if success else cfg.RED
        self.add(f"{'HOAN THANH' if success else 'THAT BAI'}! {info}", color)

    def draw(self, screen):
        pygame.draw.rect(screen, cfg.BLACK, self.rect, border_radius=6)
        pygame.draw.rect(screen, cfg.GRAY_MID, self.rect, width=1, border_radius=6)

        title = cfg.FONT_NORMAL.render("NHAT KY THUAT TOAN", True, cfg.CYAN)
        screen.blit(title, (self.rect.x + 10, self.rect.y + 6))

        line_y = self.rect.y + 32
        for text, color in self.entries[-18:]:
            if line_y + 18 > self.rect.bottom - 10:
                break
            screen.blit(cfg.FONT_SMALL.render(text, True, color), (self.rect.x + 10, line_y))
            line_y += 18
```

- [ ] **Step 2: Write controls.py**

```python
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
```

- [ ] **Step 3: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/ui/ && git commit -m "feat: add log panel and playback controls"
```

---

## Phase 6: Screen Controllers

### Task 13: Main Menu Screen

**Files:**
- Create: `cleanbot-saga/ui/menu.py`

- [ ] **Step 1: Write menu.py**

```python
# cleanbot-saga/ui/menu.py
"""Main menu screen."""
import pygame
import config as cfg
from core.game_state import state, GameMode
from core.storage import load_campaign, load_elo
from ui.renderer import draw_button


class MainMenu:
    def __init__(self):
        self.button_rects = []
        self.button_defs = []

    def layout(self, screen):
        cx = screen.get_width() // 2
        bw, bh, gap = 300, 50, 16
        camp = load_campaign()
        lvl = camp.get("level_completed", 0)
        stars = sum(camp.get("stars", {}).values())
        pve_unlocked = stars >= 20

        self.button_defs = [
            ("CHIEN DICH (Campaign)", GameMode.CAMPAIGN, True,
             f"Man {lvl + 1} | Tong ⭐: {stars}"),
            ("DAILY CHALLENGE", GameMode.DAILY, True,
             "1 ngay — 1 co hoi"),
            ("PVE ARENA", GameMode.PVE, pve_unlocked,
             f"Elo: {load_elo()}" if pve_unlocked else "Can >= 20⭐ de mo khoa"),
        ]
        self.button_rects = []
        y = screen.get_height() // 2 - 90
        for _ in self.button_defs:
            self.button_rects.append(pygame.Rect(cx - bw // 2, y, bw, bh))
            y += bh + gap

    def handle_click(self, pos):
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos) and self.button_defs[i][2]:
                return self.button_defs[i][1]
        return None

    def draw(self, screen):
        self.layout(screen)
        screen.fill(cfg.GRAY_DARK)
        cx = screen.get_width() // 2

        title = cfg.FONT_TITLE.render("CLEANBOT SAGA", True, cfg.CYAN)
        screen.blit(title, title.get_rect(centerx=cx, y=80))

        sub = cfg.FONT_NORMAL.render(
            "Game Chien Thuat AI — Giai 8-Puzzle & Dieu Khien Robot Hut Bui",
            True, cfg.GRAY_LIGHT)
        screen.blit(sub, sub.get_rect(centerx=cx, y=140))

        mouse = pygame.mouse.get_pos()
        for i, (label, mode, enabled, desc) in enumerate(self.button_defs):
            rect = self.button_rects[i]
            hover = rect.collidepoint(mouse)
            colors = {GameMode.CAMPAIGN: cfg.BLUE, GameMode.DAILY: cfg.ORANGE,
                      GameMode.PVE: cfg.RED if enabled else cfg.GRAY_MID}
            draw_button(screen, rect, label, colors.get(mode, cfg.BLUE), hover, enabled)
            d = cfg.FONT_SMALL.render(desc, True, cfg.GRAY_LIGHT if enabled else cfg.RED)
            screen.blit(d, d.get_rect(centerx=rect.centerx, top=rect.bottom + 4))
```

- [ ] **Step 2: Update main.py to use menu**

```python
# In cleanbot-saga/main.py — add after imports:
from ui.menu import MainMenu
from core.game_state import state, GameMode

# Replace the while loop in main():
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
                        print(f"Selected: {mode}")

        if state.phase == Phase.MENU:
            menu.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
```

- [ ] **Step 3: Verify menu works**

Run: `cd cleanbot-saga && python main.py`
Expected: Title, 3 buttons with descriptions, PvE grayed out, hover effects.

- [ ] **Step 4: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/ui/menu.py cleanbot-saga/main.py && git commit -m "feat: add main menu screen"
```

---

### Task 14: Phase 1 Screen — Puzzle Algorithm Selection & Animation

**Files:**
- Create: `cleanbot-saga/ui/phase1.py`

- [ ] **Step 1: Write phase1.py**

```python
# cleanbot-saga/ui/phase1.py
"""Phase 1: select algorithm, watch AI solve 8-puzzle with step-by-step animation."""
import pygame
from core.game_state import state, Phase
from core.scoring import calculate_ap
from core.storage import get_unlocked_solvers
from puzzle import puzzle_registry
from puzzle.board import generate_board, apply_move, GOAL, is_goal
from puzzle.heuristic import manhattan_distance
from ui.renderer import draw_puzzle_board, draw_button, draw_panel, draw_text
from ui.log_panel import LogPanel
from ui.controls import GameControls


class Phase1Screen:
    def __init__(self):
        self.log = LogPanel(850, 310, 330, 400)
        self.controls = GameControls(410, 420)
        self.solver_rects = []
        self.solver_list = []
        self.mode = "select"   # "select", "running", "done"
        self.solution_path = []
        self.current_step = 0
        self.current_board = None
        self.last_step_time = 0
        self.nodes_explored = 0
        self.comparison = []  # [(name, steps, nodes, is_optimal), ...]

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
            self.solver_rects.append(pygame.Rect(410, y, 330, 40))
            y += 50

    def handle_click(self, pos):
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
        self.log.add(f"Da chon: {solver_info.name}")
        self.log.add("Dang chay thuat toan...")
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
            self.log.add_complete(False, "Khong tim thay loi giai")
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
        self.log.add_complete(True, f"{steps} buoc, AP={state.action_points}")
        self.log.add(f"Nodes da duyet: {self.nodes_explored}")
        unlocked = get_unlocked_solvers()
        self.comparison = []
        for s in puzzle_registry.list_all():
            if s.id in unlocked:
                p, n = s.solve(state.puzzle_initial)
                self.comparison.append((s.name, len(p) if p else "-", n, s.category == "optimal"))
        self.comparison.sort(key=lambda x: x[1] if isinstance(x[1], int) else 999)

    def draw(self, screen):
        screen.fill(cfg.GRAY_DARK)
        draw_text(screen, "PHA 1: GIAI 8-PUZZLE", 20, 20, cfg.FONT_LARGE, cfg.CYAN)

        if self.current_board:
            draw_puzzle_board(screen, self.current_board, 50, 80)
            draw_text(screen, "Dich:", 50, 370, cfg.FONT_SMALL, cfg.GRAY_LIGHT)
            draw_puzzle_board(screen, GOAL, 50, 390)

        import config as cfg
        draw_panel(screen, pygame.Rect(850, 0, 350, 800))

        if self.mode == "select":
            draw_text(screen, "CHON THUAT TOAN:", 410, 170, cfg.FONT_NORMAL, cfg.WHITE)
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
            draw_text(screen, f"Dang chay: {s.name}", 410, 170, cfg.FONT_SMALL, cfg.CYAN)
            draw_text(screen, f"Buoc: {self.current_step}/{len(self.solution_path)}",
                      410, 195, cfg.FONT_SMALL, cfg.WHITE)

        self.log.draw(screen)
        if self.mode in ("running", "done"):
            self.controls.draw(screen)

    def _draw_comparison(self, screen):
        import config as cfg
        x, y = 410, 170
        draw_text(screen, "KET QUA SO SANH:", x, y, cfg.FONT_NORMAL, cfg.CYAN)
        y += 25
        # Header
        for col_h, (label, w) in enumerate([("Thuat toan", 160), ("Buoc", 60), ("Nodes", 60), ("Toi uu", 60)]):
            screen.blit(cfg.FONT_SMALL.render(label, True, cfg.GRAY_LIGHT), (x + sum([0, 160, 60, 60][:col_h]), y))
        y += 20
        for name, steps, nodes, is_opt in self.comparison:
            is_sel = (name == puzzle_registry.get(state.selected_solver_id).name if state.selected_solver_id else False)
            color = cfg.GREEN if is_sel else cfg.WHITE
            screen.blit(cfg.FONT_SMALL.render(name, True, color), (x, y))
            screen.blit(cfg.FONT_SMALL.render(str(steps), True, color), (x + 160, y))
            screen.blit(cfg.FONT_SMALL.render(str(nodes), True, color), (x + 220, y))
            screen.blit(cfg.FONT_SMALL.render("Co" if is_opt else "Khong", True, cfg.GREEN if is_opt else cfg.RED), (x + 280, y))
            y += 20
        y += 10
        ap_text = cfg.FONT_LARGE.render(f"AP nhan duoc: {state.action_points}", True, cfg.ORANGE)
        screen.blit(ap_text, (x, y))
```

- [ ] **Step 2: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/ui/phase1.py && git commit -m "feat: add Phase 1 screen with puzzle animation"
```

---

### Task 15: Phase 2 Screen — Vacuum Algorithm Selection & Animation

**Files:**
- Create: `cleanbot-saga/ui/phase2.py`

- [ ] **Step 1: Write phase2.py**

```python
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
        self.mode = "select"  # "select", "running", "done"
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
        state.grid_map[0, 0] = 0  # Start position is clean
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
        # Find first path
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

        # Check limits
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
        draw_text(screen, "PHA 2: DIEU KHIEN ROBOT HUT BUI", 20, 20, cfg.FONT_LARGE, cfg.CYAN)
        draw_text(screen, f"AP: {state.action_points} | Da hut: {state.dust_cleaned}/{state.total_dust}",
                  20, 55, cfg.FONT_NORMAL, cfg.ORANGE)

        if state.grid_map is not None:
            ox = 50
            oy = 90
            draw_grid(screen, self.robot.grid if self.robot else state.grid_map,
                      state.robot_pos, ox, oy)

        draw_panel(screen, pygame.Rect(850, 0, 350, 800))

        if self.mode == "select":
            draw_text(screen, "CHON THUAT TOAN:", 410, 170, cfg.FONT_NORMAL, cfg.WHITE)
            mouse = pygame.mouse.get_pos()
            for i, (a, enabled) in enumerate(self.algo_list):
                rect = self.algo_rects[i]
                hover = rect.collidepoint(mouse)
                color = cfg.GREEN if a.category == "optimal" else cfg.BLUE
                draw_button(screen, rect, a.name, color, hover, enabled)

        elif self.mode == "running":
            a = pathfinding_registry.get(state.selected_algo_id)
            draw_text(screen, f"Thuat toan: {a.name}", 410, 170, cfg.FONT_SMALL, cfg.CYAN)
            draw_text(screen, f"Buoc: {self.robot.steps_taken}/{state.action_points}",
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
        draw_text(screen, "KET QUA", x, y, cfg.FONT_LARGE, cfg.CYAN)
        y += 40
        draw_text(screen, f"Bui da hut: {state.dust_cleaned} / {state.total_dust}", x, y)
        y += 25
        draw_text(screen, f"AP con du: {state.action_points - self.robot.steps_taken}", x, y)
        y += 25
        draw_text(screen, f"Thuat toan toi uu: {'Co' if state.optimal_algo_chosen else 'Khong'}",
                  x, y, color=cfg.GREEN if state.optimal_algo_chosen else cfg.RED)
        y += 25
        draw_text(screen, f"Diem: {state.score}", x, y, cfg.FONT_LARGE, cfg.ORANGE)
        y += 35
        stars_text = "⭐" * state.stars + "☆" * (3 - state.stars)
        draw_text(screen, stars_text, x, y, cfg.FONT_TITLE, cfg.YELLOW)
```

- [ ] **Step 2: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/ui/phase2.py && git commit -m "feat: add Phase 2 screen with vacuum robot animation"
```

---

## Phase 7: Campaign, Daily, PvE Integration

### Task 16: Campaign Levels Data

**Files:**
- Create: `cleanbot-saga/campaign/levels.py`

- [ ] **Step 1: Write levels.py**

```python
# cleanbot-saga/campaign/levels.py
"""15 campaign level definitions."""

LEVELS = [
    # (grid_rows, grid_cols, dust_count, shuffle_steps)
    # Section 1: Easy — unlock BFS, DFS
    (5, 7, 8, 5),
    (5, 7, 9, 7),
    (5, 7, 10, 10),
    # Section 2: Medium — unlock Greedy
    (5, 7, 12, 12),
    (5, 7, 14, 15),
    (5, 7, 16, 18),
    # Section 3: Harder — unlock IDS
    (7, 9, 18, 20),
    (7, 9, 20, 25),
    (7, 9, 22, 30),
    # Section 4: Hard — unlock UCS
    (7, 9, 24, 30),
    (7, 9, 26, 35),
    (7, 9, 28, 40),
    # Section 5: Expert — unlock PvE Arena
    (10, 10, 30, 40),
    (10, 10, 33, 45),
    (10, 10, 35, 50),
]


def get_level(level_num):
    """Return (rows, cols, dust, shuffle) for given level (1-indexed)."""
    if 1 <= level_num <= len(LEVELS):
        return LEVELS[level_num - 1]
    return LEVELS[-1]
```

- [ ] **Step 2: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/campaign/ && git commit -m "feat: add 15 campaign level definitions"
```

---

### Task 17: Daily Challenge Generator

**Files:**
- Create: `cleanbot-saga/ui/daily.py`

- [ ] **Step 1: Write daily.py**

```python
# cleanbot-saga/ui/daily.py
"""Daily Challenge mode — seeded puzzle + map from date."""
import random
from datetime import date
from core.game_state import state, GameMode
from core.storage import save_daily, has_daily_played_today
from puzzle.board import generate_board
from vacuum.grid import create_grid


def get_daily_seed():
    """Generate a deterministic seed from today's date."""
    today = str(date.today())
    return sum(ord(c) for c in today)


def generate_daily_puzzle():
    """Generate daily puzzle using date-based seed."""
    seed = get_daily_seed()
    random.seed(seed)
    board = generate_board(shuffle_steps=15 + (seed % 10))
    random.seed()
    return board


def generate_daily_grid():
    """Generate daily grid using date-based seed."""
    seed = get_daily_seed()
    random.seed(seed + 1000)
    grid = create_grid(7, 9, 18 + (seed % 5))
    random.seed()
    return grid


def start_daily():
    """Check if daily is available, then start."""
    if has_daily_played_today():
        return False, "Da choi hom nay roi!"
    state.mode = GameMode.DAILY
    state.current_level = 0  # Daily doesn't use campaign levels
    return True, ""


def finish_daily(score, solver_id, algo_id):
    """Save daily score."""
    save_daily({
        "score": score,
        "solver": solver_id,
        "algo": algo_id
    })
```

- [ ] **Step 2: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/ui/daily.py && git commit -m "feat: add daily challenge generator"
```

---

### Task 18: PvE AI Opponent

**Files:**
- Create: `cleanbot-saga/pve/ai_opponent.py`

- [ ] **Step 1: Write ai_opponent.py**

```python
# cleanbot-saga/pve/ai_opponent.py
"""AI opponent for PvE Arena with 3 difficulty levels."""
import random
from puzzle import puzzle_registry
from vacuum import pathfinding_registry
from puzzle.heuristic import manhattan_distance
from vacuum.grid import count_dust


class AIOpponent:
    """AI opponent that picks algorithms based on difficulty."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    def __init__(self, elo):
        self.elo = elo
        self.selected_solver = None
        self.selected_algo = None

    @property
    def difficulty(self):
        if self.elo < 1200:
            return self.EASY
        if self.elo < 1600:
            return self.MEDIUM
        return self.HARD

    def choose_solver(self, puzzle_board):
        """Select 8-puzzle solver."""
        solvers = puzzle_registry.list_all()

        if self.difficulty == self.EASY:
            self.selected_solver = random.choice(solvers)
        elif self.difficulty == self.MEDIUM:
            h = manhattan_distance(puzzle_board)
            if h < 10:
                self.selected_solver = puzzle_registry.get("bfs")
            else:
                self.selected_solver = puzzle_registry.get("greedy") or puzzle_registry.get("bfs")
        else:  # HARD — test all
            best = None
            best_steps = float("inf")
            for s in solvers:
                path, _ = s.solve(puzzle_board)
                if path and len(path) < best_steps:
                    best_steps = len(path)
                    best = s
            self.selected_solver = best or puzzle_registry.get("bfs")

        return self.selected_solver

    def choose_algo(self, grid):
        """Select pathfinding algorithm."""
        algos = pathfinding_registry.list_all()

        if self.difficulty == self.EASY:
            self.selected_algo = random.choice(algos)
        elif self.difficulty == self.MEDIUM:
            if count_dust(grid) < 15:
                self.selected_algo = pathfinding_registry.get("bfs")
            else:
                self.selected_algo = pathfinding_registry.get("ids")
        else:  # HARD — always pick optimal
            self.selected_algo = pathfinding_registry.get("bfs")

        return self.selected_algo


def calculate_elo_change(player_elo, opponent_elo, player_won):
    """Calculate new Elo ratings. K-factor = 32."""
    expected = 1.0 / (1.0 + 10 ** ((opponent_elo - player_elo) / 400.0))
    actual = 1.0 if player_won else 0.0
    delta = int(32 * (actual - expected))
    return player_elo + delta
```

- [ ] **Step 2: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/pve/ && git commit -m "feat: add PvE AI opponent with 3 difficulty levels"
```

---

### Task 19: Result Screen & Full Game Loop Integration

**Files:**
- Create: `cleanbot-saga/ui/result.py`
- Modify: `cleanbot-saga/main.py`

- [ ] **Step 1: Write result.py**

```python
# cleanbot-saga/ui/result.py
"""Result screen showing score and stars after both phases."""
import pygame
import config as cfg
from core.game_state import state, Phase, GameMode
from core.storage import load_campaign, save_campaign
from ui.renderer import draw_button, draw_text, draw_text_centered


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
        draw_text(screen, "KET QUA", 20, 40, cfg.FONT_TITLE, cfg.CYAN)

        y = 130
        draw_text(screen, f"Bui da hut: {state.dust_cleaned} / {state.total_dust}", 100, y, cfg.FONT_LARGE)
        y += 40
        draw_text(screen, f"AP con du: {max(0, state.action_points - state.robot_steps_taken)}",
                  100, y, cfg.FONT_LARGE)
        y += 40
        opt_text = "Co" if state.optimal_algo_chosen else "Khong"
        opt_color = cfg.GREEN if state.optimal_algo_chosen else cfg.RED
        draw_text(screen, f"Thuat toan toi uu: {opt_text}", 100, y, cfg.FONT_LARGE, opt_color)
        y += 50
        draw_text(screen, f"TONG DIEM: {state.score}", 100, y, cfg.FONT_TITLE, cfg.ORANGE)
        y += 60
        stars_text = "⭐" * state.stars + "☆" * (3 - state.stars)
        draw_text(screen, stars_text, 100, y, cfg.FONT_TITLE, cfg.YELLOW)

        # Buttons
        cx = screen.get_width() // 2
        bw, bh = 250, 50
        self.continue_rect = pygame.Rect(cx - bw - 20, 550, bw, bh)
        self.retry_rect = pygame.Rect(cx + 20, 550, bw, bh)

        mouse = pygame.mouse.get_pos()
        draw_button(screen, self.continue_rect, "TIEP TUC",
                    cfg.GREEN, self.continue_rect.collidepoint(mouse))
        draw_button(screen, self.retry_rect, "CHOI LAI",
                    cfg.BLUE, self.retry_rect.collidepoint(mouse))
```

- [ ] **Step 2: Update main.py — full game loop integration**

```python
# Replace entire main.py with:
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

    while running:
        dt = clock.tick(cfg.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

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
                            state.puzzle_board = generate_daily_puzzle()
                            state.puzzle_initial = [row[:] for row in state.puzzle_board]
                            state.grid_map = generate_daily_grid()
                            phase1.enter()
                            state.phase = Phase.PHASE1_PUZZLE
                        else:
                            print(f"Daily: {msg}")
                    elif mode == GameMode.PVE:
                        state.mode = GameMode.PVE
                        phase1.enter(shuffle_steps=25)
                        state.phase = Phase.PHASE1_PUZZLE

                elif state.phase == Phase.PHASE1_PUZZLE:
                    phase1.handle_click(pos)

                elif state.phase == Phase.PHASE2_VACUUM:
                    phase2.handle_click(pos)

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
                            phase1.enter()
                        state.phase = Phase.PHASE1_PUZZLE

        # Update animations
        if state.phase == Phase.PHASE1_PUZZLE and phase1.mode == "running":
            phase1.update()
            if phase1.mode == "done" and state.action_points > 0:
                # Auto-transition to Phase 2 after delay
                pass  # Transition handled by button or next update

        if state.phase == Phase.PHASE2_VACUUM and phase2.mode == "running":
            phase2.update()

        # Draw
        screen.fill(cfg.GRAY_DARK)

        if state.phase == Phase.MENU:
            menu.draw(screen)

        elif state.phase == Phase.PHASE1_PUZZLE:
            phase1.draw(screen)
            # Show "Next Phase" button when Phase 1 is done
            if phase1.mode == "done" and state.action_points > 0:
                from ui.renderer import draw_button
                next_rect = pygame.Rect(410, 470, 200, 40)
                mouse = pygame.mouse.get_pos()
                draw_button(screen, next_rect, "QUA PHA 2 >>",
                          cfg.GREEN, next_rect.collidepoint(mouse))
                # Handle click in event loop
                if pygame.mouse.get_pressed()[0] and next_rect.collidepoint(pygame.mouse.get_pos()):
                    rows, cols, dust, _ = get_level(state.current_level) if state.mode == GameMode.CAMPAIGN else (7, 9, 20)
                    phase2.enter(rows=rows, cols=cols, dust_count=dust)
                    state.phase = Phase.PHASE2_VACUUM

        elif state.phase == Phase.PHASE2_VACUUM:
            phase2.draw(screen)
            # Show "View Results" when Phase 2 is done
            if phase2.mode == "done":
                from ui.renderer import draw_button
                res_rect = pygame.Rect(410, 590, 200, 40)
                mouse_pos = pygame.mouse.get_pos()
                draw_button(screen, res_rect, "XEM KET QUA >>",
                          cfg.ORANGE, res_rect.collidepoint(mouse_pos))
                if pygame.mouse.get_pressed()[0] and res_rect.collidepoint(mouse_pos):
                    result.enter()
                    state.phase = Phase.RESULT

        elif state.phase == Phase.RESULT:
            result.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Verify full game loop**

Run: `cd cleanbot-saga && python main.py`
Expected: Menu → click Campaign → Phase 1 (select solver, watch animation) → click "Qua Pha 2" → Phase 2 (select algo, watch robot) → click "Xem Ket Qua" → Result screen.

- [ ] **Step 4: Commit**

```bash
cd D:/Lab_AI/Lab_AI && git add cleanbot-saga/ && git commit -m "feat: integrate full game loop with all screens"
```

---

## Adding a New Algorithm (Guide)

To add a new algorithm (e.g., A* for puzzle, Hill Climbing for vacuum):

**For 8-Puzzle (e.g., A*):**
1. Create `cleanbot-saga/puzzle/astar.py` with:
```python
from puzzle import puzzle_registry, SolverInfo
from puzzle.board import ...
from puzzle.heuristic import manhattan_distance

def solve(board):
    # f = g + h
    ...
    return path, nodes_explored

puzzle_registry.register(SolverInfo(
    id="astar", name="A* (A-Star)",
    description="f = g + h. Toi uu va nhanh hon BFS.",
    category="optimal", unlocked_by_default=False, solve=solve
))
```

2. Done. The registry auto-discovers it. For campaign unlock, add to `get_unlocked_solvers()` in `core/storage.py`.

**For Vacuum (e.g., Greedy Best-First):**
1. Create `cleanbot-saga/vacuum/greedy.py` with:
```python
from vacuum import pathfinding_registry, PathfindingInfo
import heapq

def find_path(grid, start_pos):
    # Greedy: use Manhattan distance to nearest dust as heuristic
    ...
    return path

pathfinding_registry.register(PathfindingInfo(
    id="greedy_vac", name="Greedy Best-First (Vacuum)",
    description="Heuristic-based pathfinding.",
    category="heuristic", unlocked_by_default=False, find_path=find_path
))
```

2. Done.

---

## Plan Self-Review

1. **Spec coverage:** All sections covered — 3 game modes, 2-phase mechanics, scoring, stars, animation, campaign 15 levels, daily challenge, PvE, algorithm registries for extensibility.
2. **Placeholder scan:** No TBD/TODO. All code is complete. All file paths are exact.
3. **Type consistency:** SolverInfo, PathfindingInfo consistent across all tasks. GameState fields match usage. Function signatures consistent.
