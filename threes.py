#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


def getcolor(colorname):
    # thanks http://d.hatena.ne.jp/e_c_e_t/20110411
    colors = {
        'clear': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m'
        }

    def func2(c):
        return colors[colorname] + c + colors['clear']

    return func2


class Direction(object):
    LEFT = "Left Direction Enum"
    RIGHT = "Right Direction Enum"
    UP = "Up Direction Enum"
    DOWN = "Down Direction Enum"

    @classmethod
    def get_direction_delta(cls, direction):
        # return direction delta of (x, y)
        if direction == Direction.LEFT:
            return (-1, 0)
        elif direction == Direction.RIGHT:
            return (1, 0)
        elif direction == Direction.UP:
            return (0, -1)
        elif direction == Direction.DOWN:
            return (0, 1)


class Board(object):
    def __init__(self):
        self.width = 4
        self.height = self.width
        self.init_prob = [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3]
        self.board = [[Tile(x, y, random.choice(self.init_prob)) for x in range(self.width)] for y in range(self.height)]

    def get_score(self):
        pass

    def show(self):
        print ""
        print ""
        for row in self.board:
            for tile in row:
                tile = str(tile)
                if tile == "0":
                    color = getcolor("white")
                elif tile == "1":
                    color = getcolor("blue")
                elif tile == "2":
                    color = getcolor("red")
                else:
                    color = getcolor("black")
                print color(tile.center(5)),
            print ""
            print ""
            print ""

    def is_gameover(self):
        return True

    def get_tile_by_xy(self, x, y):
        if x < 0 or self.width - 1 < x or y < 0 or self.height - 1 < y:
            return NullTile()
        else:
            return self.board[y][x]

    def swipe(self, direction):
        transposed_flag = False
        reversed_flag = False
        if direction == Direction.UP:
            self.board = self.get_transpose_board()
            transposed_flag = True
            direction = Direction.LEFT
        elif direction == Direction.DOWN:
            self.board = self.get_transpose_board()
            transposed_flag = True
            direction = Direction.RIGHT

        if direction == Direction.RIGHT:
            reversed_flag = True
            self.board = self.get_reverse_board()

        #タイル移動処理
        for y in range(self.height):
            print self.height, y
            print self.board
            for x in range(self.width):
                source_tile = self.get_tile_by_xy(x + 1, y)
                destination_tile = self.get_tile_by_xy(x, y)
                if Tile.is_movable(source_tile, destination_tile):
                    Tile.move(source_tile, destination_tile)

        if reversed_flag is True:
            self.board = self.get_reverse_board()
        if transposed_flag is True:
            self.board = self.get_transpose_board()

    def get_reverse_board(self):
        return [list(reversed(row)) for row in self.board]

    def get_transpose_board(self):
        return [list(row) for row in zip(*self.board)]

    def refresh(self):
        pass


class Tile(object):
    def __init__(self, x, y, number):
        self.x = x
        self.y = y
        self.number = number

    def __repr__(self):
        return str(self.number)

    def set_number(self, number):
        self.number = number

    @classmethod
    def is_movable(cls, source_tile, destination_tile):
        # 移動と結合判定
        if isinstance(source_tile, NullTile) or isinstance(destination_tile, NullTile):
            return False
        sn = source_tile.number
        dn = destination_tile.number
        if sn == 0 or dn == 0:
            return True
        elif (sn == 1 and dn == 2) or (sn == 2 and dn == 1):
            return True
        elif sn == dn and sn > 2 and dn > 2:
            return True
        else:
            return False
        # if sn == dn:
        #     return True
        # elif sn == 0 or dn == 0:
        #     return True
        # elif (sn == 1 and dn == 2) or (sn == 2 and dn == 1):
        #     return True
        # else:
        #     return False

    @classmethod
    def move(cls, source_tile, destination_tile):
        if (source_tile.number == 1 and destination_tile.number == 2) or (source_tile.number == 2 and destination_tile.number == 1):
            destination_tile.set_number(3)
            source_tile.set_number(0)
        else:
            destination_tile.set_number(destination_tile.number + source_tile.number)
            source_tile.set_number(0)


#TODO: NullTileの各種処理をちゃんとする
class NullTile(Tile):
    #盤外タイル
    #override
    def __init__(self):
        self.x = None
        self.y = None
        self.number = 0


class AI(object):
    def __init__(self):
        pass

    def get_score(self):
        pass

    def get_best_move(self):
        pass


if __name__ == "__main__":
    board = Board()
    board.show()
    while 1:
        input_str = raw_input()
        if input_str == "q":
            break
        elif input_str == "a":
            board.swipe(Direction.LEFT)
        elif input_str == "d":
            board.swipe(Direction.RIGHT)
        elif input_str == "w":
            board.swipe(Direction.UP)
        elif input_str == "s":
            board.swipe(Direction.DOWN)
        board.show()
