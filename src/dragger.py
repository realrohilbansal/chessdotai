import pygame
from const import *

class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.MouseX = 0
        self.MouseY = 0
        self.InitialRow = 0
        self.InitialCol = 0

    def update_blit(self, surface):
        self.piece.set_texture(128)
        texture = self.piece.texture
        img = pygame.image.load(texture)
        img_centre = self.MouseX, self.MouseY
        self.piece.texture_rect = img.get_rect(center = img_centre)
        surface.blit(img, self.piece.texture_rect)

    def update_mouse(self, pos):
        self.MouseX, self.MouseY = pos

    def save_initial(self, pos):
        self.InitialRow = pos[1] // SQUARE_SIZE
        self.InitialCol = pos[0] // SQUARE_SIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False