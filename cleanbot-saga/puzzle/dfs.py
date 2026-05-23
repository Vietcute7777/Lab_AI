# cleanbot-saga/puzzle/dfs.py
"""DFS 8-puzzle solver -- depth-limited."""
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
