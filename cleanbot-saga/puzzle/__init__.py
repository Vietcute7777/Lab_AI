# cleanbot-saga/puzzle/__init__.py
"""8-Puzzle solver registry — Strategy Pattern.
To add a new solver:
  1. Create puzzle/my_algo.py with solve(board) -> (path, nodes)
  2. Add one line: registry.register(SolverInfo(id="...", ...))
"""

from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class SolverInfo:
    id: str
    name: str
    description: str
    category: str          # 'optimal', 'heuristic', 'uninformed'
    solve: Callable = field(repr=False)
    unlocked_by_default: bool = True
    steps: int = 0
    nodes_explored: int = 0
    solved: bool = False


class PuzzleSolverRegistry:
    def __init__(self):
        self._solvers: dict[str, SolverInfo] = {}

    def register(self, solver: SolverInfo):
        self._solvers[solver.id] = solver

    def get(self, solver_id: str) -> Optional[SolverInfo]:
        return self._solvers.get(solver_id)

    def list_all(self) -> list[SolverInfo]:
        return list(self._solvers.values())

    def list_unlocked(self, unlocked_ids: set[str]) -> list[SolverInfo]:
        return [s for s in self._solvers.values() if s.id in unlocked_ids]

    def get_optimal_ids(self) -> list[str]:
        return [s.id for s in self._solvers.values() if s.category == 'optimal']


puzzle_registry = PuzzleSolverRegistry()
