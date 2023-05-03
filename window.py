from game import Game, Action
import pygame, sys
from pygame.locals import *
import numpy as np

pygame.init()


class Window:
    BACKGROUND_COLOR = (255, 0, 0)
    BORDER_COLOR = (188, 172, 158)
    DARK_TEXT_COLOR = (124, 116, 107)
    LIGHT_TEXT_COLOR = (251, 247, 241)
    TILE_COLORS = {
        0: {
            "TEXT": (204, 193, 178),
            "BACKGROUND": (204, 193, 178),
        },
        2: {
            "TEXT": DARK_TEXT_COLOR,
            "BACKGROUND": (236, 225, 215),
        },
        4: {
            "TEXT": DARK_TEXT_COLOR,
            "BACKGROUND": (237, 223, 199),
        },
        8: {
            "TEXT": LIGHT_TEXT_COLOR,
            "BACKGROUND": (242, 177, 120),
        },
        16: {
            "TEXT": LIGHT_TEXT_COLOR,
            "BACKGROUND": (245, 149, 98),
        },
        32: {
            "TEXT": LIGHT_TEXT_COLOR,
            "BACKGROUND": (246, 124, 94),
        },
        64: {
            "TEXT": LIGHT_TEXT_COLOR,
            "BACKGROUND": (246, 94, 60),
        },
        128: {
            "TEXT": LIGHT_TEXT_COLOR,
            "BACKGROUND": (238, 208, 114),
        },
        256: {
            "TEXT": LIGHT_TEXT_COLOR,
            "BACKGROUND": (238, 204, 95),
        },
        512: {
            "TEXT": LIGHT_TEXT_COLOR,
            "BACKGROUND": (236, 200, 79),
        },
        1024: {
            "TEXT": LIGHT_TEXT_COLOR,
            "BACKGROUND": (238, 196, 64),
        },
        2048: {
            "TEXT": LIGHT_TEXT_COLOR,
            "BACKGROUND": (226, 191, 73),
        },
    }

    def __init__(self, tile_size=200, border_size=20, font_size=80):
        self.game = Game()
        self.tile_size = tile_size
        self.border_size = border_size
        self._set_keybindings()

        self.font = pygame.font.Font(None, font_size)

        self.width = tile_size * self.game.width + (self.game.width + 1) * border_size
        self.height = (
            tile_size * self.game.height + (self.game.height + 1) * border_size
        )

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("2048")

    def _set_keybindings(self):
        self.keybindings = {
            pygame.K_LEFT: Action.TO_LEFT,
            pygame.K_RIGHT: Action.TO_RIGHT,
            pygame.K_UP: Action.TO_TOP,
            pygame.K_DOWN: Action.TO_BOTTOM,
        }

    def _draw_tile(self, value, i, j):
        pygame.draw.rect(
            self.window,
            self.TILE_COLORS[value]["BACKGROUND"],
            [
                (j + 1) * self.border_size + j * self.tile_size,
                (i + 1) * self.border_size + i * self.tile_size,
                self.tile_size,
                self.tile_size,
            ],
        )

    def _draw_tile_border(self, i, j):
        pygame.draw.rect(
            self.window,
            self.BORDER_COLOR,
            [
                j * self.border_size + j * self.tile_size,
                i * self.border_size + i * self.tile_size,
                self.border_size,
                self.tile_size + self.border_size,
            ],
        )
        pygame.draw.rect(
            self.window,
            self.BORDER_COLOR,
            [
                j * self.border_size + j * self.tile_size,
                i * self.border_size + i * self.tile_size,
                self.tile_size + self.border_size,
                self.border_size,
            ],
        )

    def _draw_window_border(self):
        pygame.draw.rect(
            self.window,
            self.BORDER_COLOR,
            [self.width - self.border_size, 0, self.border_size, self.height],
        )
        pygame.draw.rect(
            self.window,
            self.BORDER_COLOR,
            [
                0,
                self.height - self.border_size,
                self.width,
                self.border_size,
            ],
        )

    def _draw_tile_text(self, value, i, j):
        text = self.font.render(str(value), True, self.TILE_COLORS[value]["TEXT"])

        w = (j + 1) * self.border_size + j * self.tile_size + self.tile_size / 2
        h = (i + 1) * self.border_size + i * self.tile_size + self.tile_size / 2

        text_rect = text.get_rect(center=(w, h))
        self.window.blit(text, text_rect)

    def render(self):
        self.window.fill(self.BACKGROUND_COLOR)

        for i, row in enumerate(self.game.board):
            for j, item in enumerate(row):
                value = int(item)
                self._draw_tile(value, i, j)
                self._draw_tile_border(i, j)
                self._draw_tile_text(value, i, j)

        self._draw_window_border()
        pygame.display.update()

    def _handle_keydown(self, key):
        try:
            action = self.keybindings[key]
        except:
            action = None

        if action:
            self.game.move(action)

    def loop(self):
        self.render()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self._handle_keydown(event.key)
                    self.render()
