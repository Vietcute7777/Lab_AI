# cleanbot-saga/vacuum/robot.py
"""Robot that navigates the grid and cleans dust."""


class Robot:
    def __init__(self, grid, start_pos=(0, 0)):
        self.grid = grid.copy()
        self.rows, self.cols = grid.shape
        self.pos = start_pos
        self.dust_cleaned = 0
        self.steps_taken = 0
        self.path_history = [start_pos]
        self.events = []  # [(pos, "move"|"clean"), ...]

    def clean_current(self):
        r, c = self.pos
        if self.grid[r][c] == 1:
            self.grid[r][c] = 0
            self.dust_cleaned += 1
            return True
        return False

    def move_to(self, new_pos):
        self.pos = new_pos
        self.steps_taken += 1
        self.path_history.append(new_pos)

    def follow_path(self, path):
        self.events = []
        for next_pos in path[1:]:
            self.move_to(next_pos)
            if self.clean_current():
                self.events.append((next_pos, "clean"))
            else:
                self.events.append((next_pos, "move"))
        return self.events

    @property
    def direction(self):
        if len(self.path_history) < 2:
            return "START"
        r1, c1 = self.path_history[-2]
        r2, c2 = self.path_history[-1]
        if r2 > r1: return "DOWN"
        if r2 < r1: return "UP"
        if c2 > c1: return "RIGHT"
        return "LEFT"
