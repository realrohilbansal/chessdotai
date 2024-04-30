from const import *
from square import Square
from piece import *
from move import Move
import copy
import pygame


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(NCOLS)]
        self.valid_moves_list = []
        self.next_player = 'white'

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move = None

    def _create(self):
        for row in range(NROWS):
            for col in range(NCOLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_others = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(NCOLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # rooks
        self.squares[row_others][0] = Square(row_others, 0, Rook(color))
        self.squares[row_others][7] = Square(row_others, 7, Rook(color))

        # knights
        self.squares[row_others][1] = Square(row_others, 1, Knight(color))
        self.squares[row_others][6] = Square(row_others, 6, Knight(color))

        # bishops
        self.squares[row_others][2] = Square(row_others, 2, Bishop(color))
        self.squares[row_others][5] = Square(row_others, 5, Bishop(color))

        # queen
        self.squares[row_others][3] = Square(row_others, 3, Queen(color))

        # king
        self.squares[row_others][4] = Square(row_others, 4, King(color))

    def calc_moves(self, row, col, piece, bool=True):

        def knight_moves():

            possible_moves = [
                (row+2, col+1),
                (row-2, col+1),
                (row+2, col-1),
                (row-2, col-1),
                (row+1, col+2),
                (row-1, col+2),
                (row+1, col-2),
                (row-1, col-2),
            ]

            for possible_move in possible_moves:
                pm_row, pm_col = possible_move
                if Square.in_range(pm_row, pm_col):
                    if self.squares[pm_row][pm_col].isempty_or_rival(piece.color):

                        initial = Square(row, col)
                        final_piece = self.squares[pm_row][pm_col].piece
                        final = Square(pm_row, pm_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

        def pawn_moves():

            # TODO: Implement en passant

            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (steps + 1))

            for move_row in range(start, end, piece.dir):
                # print(move_row)
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        # print("EMPTY")
                        initial = Square(row, col)
                        final_piece = self.squares[move_row][col].piece
                        final = Square(move_row, col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

                    else:
                        break
                else:
                    break

            # diagonal moves
            possible_moves = [
                (row + piece.dir, col - 1),
                (row + piece.dir, col + 1)
            ]

            for possible_move in possible_moves:
                pm_row, pm_col = possible_move
                if Square.in_range(pm_row, pm_col):
                    if self.squares[pm_row][pm_col].has_rivalpiece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[pm_row][pm_col].piece
                        final = Square(pm_row, pm_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def bishop_rook_queen_moves(movedirs):
            for movedir in movedirs:
                row_dir, col_dir = movedir
                pm_row = row + row_dir
                pm_col = col + col_dir

                while True:
                    if Square.in_range(pm_row, pm_col):

                        initial = Square(row, col)
                        final_piece = self.squares[pm_row][pm_col].piece
                        final = Square(pm_row, pm_col, final_piece)

                        move = Move(initial, final)

                        if self.squares[pm_row][pm_col].is_empty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        elif self.squares[pm_row][pm_col].has_rivalpiece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break

                        else:
                            break

                    else:
                        break

                    pm_row = pm_row + row_dir
                    pm_col = pm_col + col_dir

        def king_moves():

            movedirs = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1)
            ]

            # normal moves
            for movedir in movedirs:
                row_dir, col_dir = movedir
                pm_row = row + row_dir
                pm_col = col + col_dir

                if Square.in_range(pm_row, pm_col):
                    if self.squares[pm_row][pm_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[pm_row][pm_col].piece
                        final = Square(pm_row, pm_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:

                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            movedirs = [
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1)
            ]

            bishop_rook_queen_moves(movedirs)

        elif isinstance(piece, Rook):
            movedirs = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ]

            bishop_rook_queen_moves(movedirs)

        elif isinstance(piece, Queen):
            movedirs = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1)
            ]

            bishop_rook_queen_moves(movedirs)

        elif isinstance(piece, King):
            king_moves()

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # castling
        if isinstance(piece, King) and not testing:
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        piece.moved = True

        piece.clear_moves()

        self.last_move = move

    def valid_moves(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)

        for row in range(NROWS):
            for col in range(NCOLS):
                if temp_board.squares[row][col].has_rivalpiece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(row, col, p, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False
    
    def checked(self, color):
        temp_board = copy.deepcopy(self)
        for row in range(NROWS):
            for col in range(NCOLS):
                if temp_board.squares[row][col].has_rivalpiece(color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(row, col, p, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def all_valid_moves(self):
        temp_board = copy.deepcopy(self)
        self.valid_moves_list = []

        for row in range(NROWS):
            for col in range(NCOLS):
                if temp_board.squares[row][col].has_teampiece(self.next_player):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(row, col, p, bool=True)
                    self.valid_moves_list.extend(p.moves)
        
        return
                    

    def piece_opp(self, color):
        return 'black' if color == 'white' else 'white'
    
    def checkmate(self):
        if not self.valid_moves_list and self.checked(self.next_player):
            print("CHECKMATE!")
            print(f"{self.piece_opp(self.next_player).upper()} WON!")
            font = pygame.font.Font(None, 100)
            text = font.render(f"CHECKMATE!  {self.piece_opp(self.next_player).upper()} WON!", True, (255,255,255))
            return (text, 1)
        return
    
    def stalemate(self):
        if not self.valid_moves_list and not self.checked(self.next_player):
            print("STALEMATE!")
            print("MATCH IS DRAW")
            font = pygame.font.Font(None, 100)
            text = font.render(f'STALEMATE!  MATCH IS DRAW!', True, (255,255,255))
            return (text, 0)
        return 

