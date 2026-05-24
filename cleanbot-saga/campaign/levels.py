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
