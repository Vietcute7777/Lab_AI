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
    unlocked = {"bfs", "dfs", "greedy"}
    return unlocked

def get_unlocked_algos():
    lvl = load_campaign().get("level_completed", 0)
    unlocked = {"bfs", "dfs"}
    if lvl >= 9: unlocked.add("ids")
    if lvl >= 12: unlocked.add("ucs")
    return unlocked
