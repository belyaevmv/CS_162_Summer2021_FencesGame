# Author: Maxim Belyaev
# Date: 7/28/2021
# Description: Quoridor board

import pygame as p
import Quoridor

width = 840  # board size horizontally
height = 520  # board size vertically
dimension = 13  # 9 squares + 8(half of square size) rectangles
sq_size = height//dimension
rec_width = sq_size//2
max_fps = 15
#images = {}

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color('black'))
    global gs
    gs = Quoridor.QuoridorGame()
    running = True
    sq_selected = ()  # no square is selected (row, column)
    player_clicks = []  # keeps track of player clicks (two tuples: [(0,4), (1,4)])
    player_moves_name = []
    player_making_move = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = click_location(p.mouse.get_pos())  # [(x,y) location of tile, tile shape(sq or fence)]
                col = location[0][0]  # column we clicked and what piece we've selected
                row = location[0][1]  # row we clicked and what piece we've selected
                # check is the same square selected
                if sq_selected == (col, row):
                    sq_selected = ()  # deselect
                    player_clicks = []  # clear player clicks
                    player_moves_name = []
                    player_making_move = []
                else:
                    sq_selected = (col, row)
                    player_clicks.append(sq_selected)
                    player_moves_name.append(location[-1])
                    player_making_move.append(location[2])

                # make a move
                if len(player_clicks) == 2 and player_moves_name[0] == player_moves_name[1] == "make move":
                    # check if first click selected a player tile who has a turn to make a move
                    player_turn = gs.get_player_from_name(gs.get_turn())
                    if player_clicks[0] == player_turn.get_pawn():
                        gs.move_pawn(player_turn.get_player_name(),player_clicks[1])
                    sq_selected = ()  # reset user clicks
                    player_clicks = []
                    player_moves = []
                    player_moves_name = []
                    player_making_move = []

                # place fence
                elif len(player_clicks) == 2 and player_moves_name[0] == 'place fence':
                    if gs.get_turn() == player_making_move[0]:
                        gs.place_fence(gs.get_turn(), location[1], player_clicks[1])
                        print(gs.get_player_from_name(player_making_move[0]).get_fences())
                    sq_selected = ()  # reset user clicks
                    player_clicks = []
                    player_moves = []
                    player_moves_name = []
                    player_making_move = []

        draw_game_state(screen)
        clock.tick(max_fps)
        p.display.flip()


def draw_game_state(screen):
    draw_board(screen)  # draw squares on the board
    # add highlighes
    draw_pieces(screen)


def draw_board(screen):
    """draw squares on the board"""
    colors = [p.Color(250, 250, 250), p.Color(150, 150, 150), p.Color(200, 200, 200)]
    row = 0
    for r in range(17):
        column = 0
        for c in range(17):
            if r % 2 == 0:
                color = colors[((r+c) % 2)]
                if c % 2 == 0:
                    p.draw.rect(screen, color, p.Rect(column, row, sq_size, sq_size))
                    column += sq_size
                else:
                    p.draw.rect(screen, color, p.Rect(column, row, rec_width, sq_size))
                    column += rec_width
            else:
                color = colors[(c % 2)+1]
                if c % 2 == 0:
                    p.draw.rect(screen, color, p.Rect(column, row, sq_size, rec_width))
                    column += sq_size
                else:
                    p.draw.rect(screen, color, p.Rect(column, row, rec_width, rec_width))
                    column += rec_width
        if r % 2 == 0:
            row += sq_size
        else:
            row += rec_width



def draw_pieces(screen):
    """draw pieces on the board"""
    #draw player positions
    p1 = gs.get_player_from_name(1)
    p2 = gs.get_player_from_name(2)
    p1_c = p1.get_pawn()
    p2_c = p2.get_pawn()
    colors = ["red", "blue", p.Color(100, 100, 100), "brown"]
    p.draw.circle(screen, colors[0], (p1_c[0] * 40 + p1_c[0] * 20 + 20, p1_c[1] * 40 + p1_c[1] * 20 + 20), 18)
    p.draw.circle(screen, colors[1], (p2_c[0] * 40 + p2_c[0] * 20 + 20, p2_c[1] * 40 + p2_c[1] * 20 + 20), 18)

    #draw placed fence
    if len(gs.get_fences_on_board()) > 36:
        for f in gs.get_fences_on_board():
            f_coord = f.get_coordinate()
            f_orientation = f.get_orientation()
            if (f_coord[0]>0 and f_coord[0]<9) and (f_coord[1]>0 and f_coord[1]<9):
                f_column = f_coord[0] * sq_size + (f_coord[0]) * sq_size / 2
                f_row = f_coord[1] * sq_size + (f_coord[1]) * sq_size / 2
                if f_orientation == "v":
                    p.draw.rect(screen, colors[3], p.Rect(f_column - 20, f_row, 20, 40))
                else:
                    p.draw.rect(screen, colors[3], p.Rect(f_column, f_row - 20, 40, 20))

    #draw not played fence positions
    column = 540
    p1_fences = p1.get_fences()
    for f in range(10):
        if f < p1_fences:
            p.draw.rect(screen, colors[2], p.Rect(column, 0, 20, 40))
        else:
            p.draw.rect(screen, "black", p.Rect(column, 0, 20, 40))
        column += 30

    column = 540
    p2_fences = p2.get_fences()
    for f in range(10):
        if f < p2_fences:
            p.draw.rect(screen, colors[2], p.Rect(column, 480, 20, 40))
        else:
            p.draw.rect(screen, "black", p.Rect(column, 480, 20, 40))
        column += 30

def click_location(mouse_coord):
    """function to find horizontal/vertical value of the click"""
    t_list = []
    click_coordinate = []
    orientation = None
    move = None
    for val in mouse_coord:
        if val <= 520:
            if val < 60:
                temp_1 = val
            else:
                temp_1 = val % 60
            if temp_1 <= 40:
                tile = "sq"
                coord = int(val // 60)
                move = "make move"
            else:
                coord = int(val // 60) + 1
                tile = "fence"
            t_list.append(tile)
            if t_list[0] == "fence":
                orientation = 'v'
            else:
                orientation = "h"
            click_coordinate.append(coord)
        else:
            return select_fence((mouse_coord[0]-520, mouse_coord[1]))

    if t_list[0] == t_list[1]:
        square = t_list[0]
        move = "make move"
    else:
        square = "fence"
        move = "place fence"
    return [(click_coordinate[0], click_coordinate[1]), orientation, None, move]

def select_fence(mouse_coord):
    """"""
    if mouse_coord[1] <= 40:
        # get player 1 not played fences
        if 20 + 30 * gs.get_player_from_name(1).get_fences() >= mouse_coord[0]:
            print("hi")
            if (mouse_coord[0] - 20) % 30 < 20:
                return [(None, None), None, 1, "place fence"]
            else:
                return [(None, None), None, None, "place fence"]
        else:
            return [(None, None), None, None, "place fence"]
    elif mouse_coord[1] >= 480:
        # get player 2 not played fences
        if 20 + 30 * gs.get_player_from_name(2).get_fences() >= mouse_coord[0]:
            if (mouse_coord[0] - 20) % 30 < 20:
                return [(None, None), None, 2, "place fence"]
            else:
                return [(None, None), None, None, "place fence"]
        else:
            return [(None, None), None, None, "place fence"]
    else:
        return [(None, None), None, None, "place fence"]





if __name__ == '__main__':
    main()


