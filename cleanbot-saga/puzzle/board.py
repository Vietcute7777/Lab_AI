# cleanbot-saga/puzzle/board.py
"""8-Puzzle board utilities: generation, moves, goal check."""
import random

GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
GOAL_POSITIONS = {
    val: (r, c) for r, row in enumerate(GOAL)
    for c, val in enumerate(row) if val != 0
}
OPPOSITES = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}


def is_solvable(board):
    flat = [board[r][c] for r in range(3) for c in range(3)]
    inversions = sum(
        1 for i in range(9) for j in range(i + 1, 9)
        if flat[i] and flat[j] and flat[i] > flat[j]
    )
    return inversions % 2 == 0


def generate_board(shuffle_steps=20):
    board = [row[:] for row in GOAL]
    r, c = 2, 2
    prev_move = None
    for _ in range(shuffle_steps):
        moves = _get_moves_dict(board)
        if prev_move:
            moves.pop(OPPOSITES.get(prev_move), None)
        if not moves:
            break
        direction, (nr, nc) = random.choice(list(moves.items()))
        board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
        r, c = nr, nc
        prev_move = direction
    return board


def generate_random_board():
    while True:
        nums = list(range(9))
        random.shuffle(nums)
        if is_solvable([nums]):
            return [nums[i:i + 3] for i in range(0, 9, 3)]


def _get_moves_dict(board):
    r, c = find_blank(board)
    moves = {}
    if r > 0: moves["UP"] = (r - 1, c)
    if r < 2: moves["DOWN"] = (r + 1, c)
    if c > 0: moves["LEFT"] = (r, c - 1)
    if c < 2: moves["RIGHT"] = (r, c + 1)
    return moves


def find_blank(board):
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                return r, c
    return 2, 2


def apply_move(board, direction):
    r, c = find_blank(board)
    moves = _get_moves_dict(board)
    if direction not in moves:
        return [row[:] for row in board]
    nr, nc = moves[direction]
    new_board = [row[:] for row in board]
    new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
    return new_board


def is_goal(board):
    return board == GOAL


def board_to_tuple(board):
    return tuple(cell for row in board for cell in row)
