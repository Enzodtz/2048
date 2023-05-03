import itertools
import numpy as np
from enum import Enum


class Action(Enum):
    TO_LEFT = 1
    TO_RIGHT = 2
    TO_TOP = 3
    TO_BOTTOM = 4


class Game:
    def __init__(
        self,
        width=4,
        height=4,
        prob_of_new_4_piece=0.1,
        starting_pieces=2,
    ):
        self.prob_of_new_4_piece = prob_of_new_4_piece

        self.board = np.zeros((height, width))
        self.height = height
        self.width = width
        self.ended = False

        for _ in range(starting_pieces):
            self._new_piece()

    def _random_pos(self):
        h = np.random.randint(self.board.shape[0])
        w = np.random.randint(self.board.shape[1])

        return (h, w)

    def _new_piece(self):
        pos = self._random_pos()
        while self.board[pos] != 0:
            pos = self._random_pos()

        if np.random.random() < self.prob_of_new_4_piece:
            self.board[pos] = 4
        else:
            self.board[pos] = 2

    def _rotate_board(self, action, board, backward=False):
        if action == Action.TO_TOP:
            return board
        elif action == Action.TO_BOTTOM:
            return np.rot90(board, k=2)
        elif action == Action.TO_LEFT:
            k = 1 if backward else -1
            return np.rot90(board, k=k)
        elif action == Action.TO_RIGHT:
            k = -1 if backward else 1
            return np.rot90(board, k=k)

    def _check_ended(self):
        self.ended = (0 not in self.board) or (2048 in self.board)

    def move(self, action):
        """
        The idea is to have a main loop to move the pieces from bottom to top
        Following this logic, we will rotate the matrix in order for the target side
        to be on top and then de-rotate
        """
        if self.ended:
            return

        # Rotate
        new_board = np.array(self.board)  # unlink
        new_board = self._rotate_board(action, new_board)
        already_summed_board = np.zeros(self.board.shape, dtype=bool)
        board_changed = False

        # Main loop
        for i, row in enumerate(new_board):
            for j, item in enumerate(row):
                if item != 0:
                    pos = (i, j)
                    for k in itertools.count(1):
                        # Possible optimization: start verifying from first line if == 0
                        # Possible optimization: iterate through j for left instead of rotating
                        new_pos = (i - k, j)

                        if -1 in new_pos:
                            break
                        elif already_summed_board[new_pos]:
                            break
                        elif new_board[new_pos] == item:
                            new_board[new_pos] = item * 2
                            already_summed_board[new_pos] = True
                            board_changed = True
                            new_board[pos] = 0
                            break
                        elif new_board[new_pos] != 0:
                            break

                        board_changed = True
                        new_board[new_pos] = item
                        new_board[pos] = 0
                        pos = new_pos

        # De rotate
        self.board = self._rotate_board(action, new_board, backward=True)

        self._check_ended()

        if not self.ended and board_changed:
            self._new_piece()
