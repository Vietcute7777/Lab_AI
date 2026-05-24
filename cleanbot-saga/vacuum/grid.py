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
