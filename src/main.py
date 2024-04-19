import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()
        

    def mainloop(self):

        board = self.game.board
        dragger = self.game.dragger

        while True:
            self.game.set_bg(self.screen)
            self.game.show_lastmove(self.screen)
            self.game.show_moves(self.screen)
            self.game.show_pieces(self.screen)
            self.game.show_hover(self.screen)

            if dragger.dragging:
                dragger.update_blit(self.screen)
            
            for event in pygame.event.get():
                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.MouseY // SQUARE_SIZE
                    clicked_col = dragger.MouseX // SQUARE_SIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece

                        if piece.color == self.game.next_player:
                            board.calc_moves(clicked_row, clicked_col, piece, bool = True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            self.game.set_bg(self.screen)
                            self.game.show_lastmove(self.screen)

                            self.game.show_moves(self.screen)
                            self.game.show_pieces(self.screen)
                        
                # Move mouse
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQUARE_SIZE
                    motion_col = event.pos[0] // SQUARE_SIZE

                    if -1 < motion_row < 8 and -1 < motion_col < 8:
                        self.game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # self.game.set_bg(self.screen)
                        # self.game.show_moves(self.screen)
                        # self.game.show_pieces(self.screen)
                        dragger.update_blit(self.screen) 

                # Release click
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.MouseY // SQUARE_SIZE
                        released_col = dragger.MouseX // SQUARE_SIZE

                        initial_row = dragger.InitialRow
                        initial_col = dragger.InitialCol

                        initial = Square(initial_row, initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_moves(dragger.piece, move):
                            board.move(dragger.piece, move)
                            self.game.set_bg(self.screen)
                            self.game.show_lastmove(self.screen)
                            self.game.show_pieces(self.screen)
                            self.game.next_turn()

                    dragger.undrag_piece()

                # Key press
                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_r:
                #         self.game.reset()
                #         board = self.game.board
                #         dragger = self.game.dragger

                #     elif event.key == pygame.K_ESCAPE:
                #         pygame.quit()
                #         sys.exit()

                # Quit game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop()