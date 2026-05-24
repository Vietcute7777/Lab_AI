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
