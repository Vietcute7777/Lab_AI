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
