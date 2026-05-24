# cleanbot-saga/pve/ai_opponent.py
"""AI opponent for PvE Arena with 3 difficulty levels."""
import random
from puzzle import puzzle_registry
from vacuum import pathfinding_registry
from puzzle.heuristic import manhattan_distance
from vacuum.grid import count_dust


class AIOpponent:
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
        solvers = puzzle_registry.list_all()
        if self.difficulty == self.EASY:
            self.selected_solver = random.choice(solvers)
        elif self.difficulty == self.MEDIUM:
            h = manhattan_distance(puzzle_board)
            if h < 10:
                self.selected_solver = puzzle_registry.get("bfs")
            else:
                self.selected_solver = puzzle_registry.get("greedy") or puzzle_registry.get("bfs")
        else:
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
        algos = pathfinding_registry.list_all()
        if self.difficulty == self.EASY:
            self.selected_algo = random.choice(algos)
        elif self.difficulty == self.MEDIUM:
            if count_dust(grid) < 15:
                self.selected_algo = pathfinding_registry.get("bfs")
            else:
                self.selected_algo = pathfinding_registry.get("ids")
        else:
            self.selected_algo = pathfinding_registry.get("bfs")
        return self.selected_algo


def calculate_elo_change(player_elo, opponent_elo, player_won):
    expected = 1.0 / (1.0 + 10 ** ((opponent_elo - player_elo) / 400.0))
    actual = 1.0 if player_won else 0.0
    delta = int(32 * (actual - expected))
    return player_elo + delta
