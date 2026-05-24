# cleanbot-saga/vacuum/ucs.py
"""UCS (Uniform Cost Search) pathfinding."""
import heapq
import itertools
from vacuum import pathfinding_registry, PathfindingInfo


def find_path(grid, start_pos):
    rows, cols = grid.shape
    counter = itertools.count()
    heap = [(0, next(counter), start_pos, [start_pos])]
    visited_costs = {start_pos: 0}

    while heap:
        cost, _, (r, c), path = heapq.heappop(heap)
        if cost > visited_costs.get((r, c), float("inf")):
            continue
        if grid[r][c] == 1:
            return path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + 1
                if new_cost < visited_costs.get((nr, nc), float("inf")):
                    visited_costs[(nr, nc)] = new_cost
                    heapq.heappush(heap, (new_cost, next(counter), (nr, nc), path + [(nr, nc)]))
    return []


pathfinding_registry.register(PathfindingInfo(
    id="ucs", name="UCS (Uniform Cost Search)",
    description="Mở rộng node có chi phí thấp nhất. Tối ưu, hoạt động tốt cả khi trọng số khác nhau.",
    category="optimal", unlocked_by_default=False, find_path=find_path
))
