# cleanbot-saga/puzzle/bfs.py
"""BFS 8-puzzle solver -- guarantees shortest solution."""
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
    description="Duyệt theo chiều rộng. Luôn tìm đường đi ngắn nhất.",
    category="optimal", solve=solve
))
