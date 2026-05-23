# cleanbot-saga/vacuum/dfs.py
"""DFS pathfinding — depth-first search."""
from vacuum import pathfinding_registry, PathfindingInfo


def find_path(grid, start_pos):
    rows, cols = grid.shape
    stack = [(start_pos, [start_pos])]
    visited = {start_pos}

    while stack:
        (r, c), path = stack.pop()
        if grid[r][c] == 1:
            return path
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))
    return []


pathfinding_registry.register(PathfindingInfo(
    id="dfs", name="DFS (Depth-First Search)",
    description="Tim duong den bui theo chieu sau. Khong dam bao ngan nhat.",
    category="uninformed", find_path=find_path
))
