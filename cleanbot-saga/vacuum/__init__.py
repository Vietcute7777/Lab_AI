# cleanbot-saga/vacuum/__init__.py
"""Vacuum pathfinding registry — Strategy Pattern.
To add a new algorithm:
  1. Create vacuum/my_algo.py with find_path(grid, start) -> list[(r,c)]
  2. Add one line: registry.register(PathfindingInfo(id="...", ...))
"""

from dataclasses import dataclass, field
from typing import Callable, Optional, Any


@dataclass
class PathfindingInfo:
    id: str
    name: str
    description: str
    category: str          # 'optimal', 'uninformed', 'iterative'
    find_path: Callable = field(repr=False)
    unlocked_by_default: bool = True


class PathfindingRegistry:
    def __init__(self):
        self._algos: dict[str, PathfindingInfo] = {}

    def register(self, algo: PathfindingInfo):
        self._algos[algo.id] = algo

    def get(self, algo_id: str) -> Optional[PathfindingInfo]:
        return self._algos.get(algo_id)

    def list_all(self) -> list[PathfindingInfo]:
        return list(self._algos.values())

    def list_unlocked(self, unlocked_ids: set[str]) -> list[PathfindingInfo]:
        return [a for a in self._algos.values() if a.id in unlocked_ids]

    def get_optimal_ids(self) -> list[str]:
        return [a.id for a in self._algos.values() if a.category == 'optimal']


pathfinding_registry = PathfindingRegistry()
