# cleanbot-saga/vacuum/ids.py
"""IDS (Iterative Deepening Search) pathfinding."""
from vacuum import pathfinding_registry, PathfindingInfo


def find_path(grid, start_pos):
    rows, cols = grid.shape

    def dls(pos, path, limit):
        r, c = pos
        if grid[r][c] == 1:
            return path
        if limit <= 0:
            return None
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in path:
                result = dls((nr, nc), path + [(nr, nc)], limit - 1)
                if result is not None:
                    return result
        return None

    for depth_limit in range(rows * cols + 1):
        result = dls(start_pos, [start_pos], depth_limit)
        if result is not None:
            return result
    return []


pathfinding_registry.register(PathfindingInfo(
    id="ids", name="IDS (Iterative Deepening)",
    description="Ket hop uu diem BFS (toi uu) va DFS (it bo nho). Tang dan do sau.",
    category="iterative", unlocked_by_default=False, find_path=find_path
))
