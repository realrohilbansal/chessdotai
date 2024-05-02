import pygame

from const import *
from board import *
from dragger import *

class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.hovered_sq = None        

        self.action_size = 218

    def set_bg(self, surface):
        for row in range(NROWS):
            for col in range(NCOLS):
                if (row+col)%2 == 0:
                    color = MAIN_COLOR[0] # (229, 228, 200)
                else:
                    color = MAIN_COLOR[1] # (60, 95, 135)

                pygame.draw.rect(surface, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def show_pieces(self, surface):
        for row in range(NROWS):
            for col in range(NCOLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture()
                        img = pygame.image.load(piece.texture)
                        img_centre = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center = img_centre)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = VALID_MOVE_COLOR[0] if (move.final.row + move.final.col) % 2 == 0 else VALID_MOVE_COLOR[1]

                rect = (move.final.col*SQUARE_SIZE, move.final.row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def next_turn(self):
        # self.next_player = 'white' if self.next_player == 'black' else 'black'
        self.board.next_player = 'white' if self.board.next_player == 'black' else 'black'

    def show_lastmove(self, surface):
        if self.board.last_move:
            lastmove = self.board.last_move
            for pos in [lastmove.initial, lastmove.final]:
                color = LAST_MOVE_COLOR[0] if (pos.row + pos.col) % 2 == 0 else LAST_MOVE_COLOR[1] # (123, 187, 227), (43, 119, 191)
                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sq:
            color = (180, 180, 180)
            rect = (self.hovered_sq.col * SQUARE_SIZE, self.hovered_sq.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def set_hover(self, row, col):
        self.hovered_sq = self.board.squares[row][col]

    def reset(self):
        self.__init__()