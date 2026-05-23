# cleanbot-saga/ui/daily.py
"""Daily Challenge mode — seeded puzzle + map from date."""
import random
from datetime import date
from core.game_state import state, GameMode
from core.storage import save_daily, has_daily_played_today
from puzzle.board import generate_board
from vacuum.grid import create_grid


def get_daily_seed():
    today = str(date.today())
    return sum(ord(c) for c in today)


def generate_daily_puzzle():
    seed = get_daily_seed()
    random.seed(seed)
    board = generate_board(shuffle_steps=15 + (seed % 10))
    random.seed()
    return board


def generate_daily_grid():
    seed = get_daily_seed()
    random.seed(seed + 1000)
    grid = create_grid(7, 9, 18 + (seed % 5))
    random.seed()
    return grid


def start_daily():
    if has_daily_played_today():
        return False, "Đã chơi hôm nay rồi!"
    state.mode = GameMode.DAILY
    state.current_level = 0
    return True, ""


def finish_daily(score, solver_id, algo_id):
    save_daily({
        "score": score,
        "solver": solver_id,
        "algo": algo_id
    })
