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
    description="Tham lam: luôn chọn nước đi có Manhattan nhỏ nhất. Nhanh nhưng không đảm bảo tối ưu.",
    category="heuristic", unlocked_by_default=False, solve=solve
))
