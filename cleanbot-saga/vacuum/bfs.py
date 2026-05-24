# cleanbot-saga/vacuum/bfs.py
"""BFS pathfinding — shortest path to nearest dust."""
from collections import deque
from vacuum import pathfinding_registry, PathfindingInfo


def find_path(grid, start_pos):
    rows, cols = grid.shape
    queue = deque([(start_pos, [start_pos])])
    visited = {start_pos}

    while queue:
        (r, c), path = queue.popleft()
        if grid[r][c] == 1:
            return path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return []


pathfinding_registry.register(PathfindingInfo(
    id="bfs", name="BFS (Breadth-First Search)",
    description="Tìm đường ngắn nhất đến bụi gần nhất. Luôn tối ưu.",
    category="optimal", find_path=find_path
))
