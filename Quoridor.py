# Author: Maxim Belyaev
# Date: 7/28/2021
# Description: Quoridor board game
class Board:
    """
    Class that represents the game board
    """
    def __init__(self):
        self.board = [
            ["--", "|", "--", "|", "--", "|", "--", "|", "P1", "|", "--", "|", "--", "|", "--", "|", "--"],
            ["==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "=="],
            ["--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--"],
            ["==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "=="],
            ["--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--"],
            ["==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "=="],
            ["--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--"],
            ["==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "=="],
            ["--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--"],
            ["==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "=="],
            ["--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--"],
            ["==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "=="],
            ["--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--"],
            ["==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "=="],
            ["--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--", "|", "--"],
            ["==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "==", "*", "=="],
            ["--", "|", "--", "|", "--", "|", "--", "|", "P2", "|", "--", "|", "--", "|", "--", "|", "--"],
        ]

    def get_board(self):
        """returns board"""
        return self.board


class Player:
    """
    Class that represents a player that plays quoridor game.
    Class is called during initial method of QuarridorGame as part of setting up the board
    """

    def __init__(self, name, pawn_coord):
        """
        Initial method that creates a player from given name and starting pawn coordinates.
        Method sets up the amount of fences player has to play at the beginning of the game.
        """
        self._player_name = name
        self._player_pawn = pawn_coord
        self._player_fences = 10

    def get_player_name(self):
        """Returns player's name"""
        return self._player_name

    def set_player_name(self, new_name):
        """Sets player's name"""
        self._player_name = new_name

    def get_pawn(self):
        """Returns player's pawn coordinate"""
        return self._player_pawn

    def set_pawn(self, new_coord):
        """Sets player's pawn new coordinate"""
        self._player_pawn = new_coord

    def get_fences(self):
        """Returns number of fences left play for that player"""
        return self._player_fences

    def deduct_fence(self):
        """Removes one fence from player.Return True if number of fences left is greater than 0, else returns False"""
        if self.get_fences() - 1 < 0:
            return False
        self._player_fences -= 1
        return True


class Fence:
    """
    Class that represents fence object, which is one of the elements of QuorridorGame
    """
    def __init__(self, orientation, coordinate):
        """
        Initial method that creates a fence from given orientation, vertical or horizontal, and coordinate location
        :param orientation:
        :param coordinate:
        """
        self._orientation = orientation
        self._coordinate = coordinate

    def get_orientation(self):
        """Function returns orientation of a fence"""
        return self._orientation

    def get_coordinate(self):
        """Function returns coordinate of a fence"""
        return self._coordinate


class QuoridorGame:
    """
    Class that represents quoridor game. It sets up the board, makes moves - pawn and fence, keeps track of current
    player's turn and who is a winner
    """
    def __init__(self):
        """Initial method that starts the game and sets up the board by creates two player objects,
        36 fences on the perimeter of the board"""
        self._p1 = Player(1, (4, 0))  # Creates player 1 object
        self._p2 = Player(2, (4, 8))  # Creates player 2 object
        self._board_fences = list()  # List of fence objects
        for num_1 in [0, 9]:
            for num_2 in range(9):
                self._board_fences.append(Fence('v', (num_1, num_2)))
                self._board_fences.append(Fence('h', (num_2, num_1)))
        self._player_turn = 1  # Player name who has a turn to play right now
        self._winner = None  # Player who won the game
        self._board = Board()

    # Main function for user interactions
    def get_board(self):
        """Function to return board"""
        return self._board.get_board()

    def print_board(self):
        """Function to print out the board"""
        print("     x0   x1   x2   x3   x4   x5   x6   x7   x8")
        for y in range(9):
            fence_line = "   |"
            square_line = "y" + str(y) + " |"
            for x in range(9):
                if x > 0:
                    square_line += " "
                if (x, y) in self.get_board_fence_coord():
                    for f in self.get_fence_from_coord((x, y)):
                        if f.get_orientation() == 'v':
                            if len(self.get_fence_from_coord((x, y))) == 1:
                                square_line = (square_line[:-1] + "|")
                                fence_line += "    +"
                            else:
                                square_line = (square_line[:-1] + "|")
                        elif f.get_orientation() == "h":
                            fence_line += " == +"
                else:
                    fence_line += ("    " + "+")
                if x == 8:
                    fence_line = fence_line[:-1] + "|"

                if (x, y) == self._p1.get_pawn():
                    square_line += " P1 "
                elif (x, y) == self._p2.get_pawn():
                    square_line += " P2 "
                else:
                    square_line += "    "
            square_line += "|"
            print(fence_line)
            print(square_line)

    def place_fence(self, player, orientation, target_coord):
        """
        Function that checks validity of the fence move, makes the move if it's valid, and updates the board.
        :param player: player who makes the move
        :param orientation: orientation of the fence - vertical or horizontal
        :param target_coord: coordinate to which player wishes to place the fence
        :return: True if move valid, False otherwise
        """
        if self.initial_move_check("place_fence", player, target_coord, orientation) is False:
            return False
        if orientation not in ['v', 'h']:
            return False
        if self.get_player_from_name(player).get_fences() == 0:
            return False
        # Create desired fence and temporary place on board
        temp_fence = Fence(orientation, target_coord)
        self.add_fence_to_board(temp_fence)
        if self.fair_play(player) is False:
            self.remove_fence_from_board(temp_fence)
            return "breaks the fair play rule"
        self.get_player_from_name(player).deduct_fence()
        self.set_turn()
        return True

    def move_pawn(self, player_name, target_coordinate):
        """
        Function that checks validity of the pawn move, makes the move if it's valid, and updates the board.
        :param player_name: player who makes the move
        :param target_coordinate: coordinate to which player wishes to move its pawn
        :return: True if move valid, False otherwise
        """
        if self.initial_move_check("move_pawn", player_name, target_coordinate, None) is False:
            return False
        playing_player = self.get_player_from_name(player_name)
        if player_name == 1:
            opposing_player = self.get_player_from_name(2)
        else:
            opposing_player = self.get_player_from_name(1)
        if target_coordinate in self.ortho_adjacent(playing_player.get_pawn()):
            if self.fence_between_coord(playing_player.get_pawn(), target_coordinate) is True:
                return False
            if target_coordinate == opposing_player.get_pawn():
                return False
            playing_player.set_pawn(target_coordinate)
            self.set_turn()
            return True
        if opposing_player.get_pawn() not in self.ortho_adjacent(target_coordinate):
            return False
        # Checks complexity of the move - diagonal or over the opposing pawn
        move_direction = self.move_direction(playing_player.get_pawn(), opposing_player.get_pawn())
        x_coord = opposing_player.get_pawn()[0] + move_direction[0]
        y_coord = opposing_player.get_pawn()[1] + move_direction[1]
        if target_coordinate != (x_coord, y_coord):
            if self.fence_between_coord(opposing_player.get_pawn(), (x_coord, y_coord)) is False:
                return False
        # Checks if there are fences between coordinates
        if self.fence_between_coord(playing_player.get_pawn(), opposing_player.get_pawn()) is True:
            return False
        if self.fence_between_coord(opposing_player.get_pawn(), target_coordinate) is True:
            return False
        playing_player.set_pawn(target_coordinate)
        self.set_turn()
        return True

    def is_winner(self, player):
        """
        Function that checks if given player won the game.
        :param player: player name
        :return: True if given player won, False otherwise
        """
        if self._winner == player:
            return True
        return False

    # Getters and setters functions

    def get_turn(self):
        """Function to return a player who has a current turn"""
        return self._player_turn

    def add_fence_to_board(self, fence):
        """
        Function to add fence to a list of fences on the board
        :param fence: fence object
        :return: Function does not return anything
        """
        self._board_fences.append(fence)

    def remove_fence_from_board(self, fence):
        """
        Removes fence from the board, if move breaks fairplay rule
        :param fence: object
        :return: function does not return anything
        """
        self._board_fences.remove(fence)

    def get_board_fence_coord(self):
        """
        Function to return list of fence coordinates that has been places on the board
        :return: List of fence coordinates
        """
        return [i.get_coordinate() for i in self._board_fences]

    def get_fences_on_board(self):
        """Function to return list of fence objects that were placed on the board"""
        return self._board_fences

    def get_fence_from_coord(self, coord):
        """
        Function to return a list of fence objects from given coordinate
        :param coord:
        :return: list
        """
        return [obj for obj in self.get_fences_on_board() if obj.get_coordinate() == coord]

    def get_player_from_name(self, name):
        """
        Function to return player object from given player's name.
        :param name: player's name
        :return: Player Object
        """
        if self._p1.get_player_name() == name:
            return self._p1
        elif self._p2.get_player_name() == name:
            return self._p2
        return False

    def set_turn(self):
        """
        Function to check if move was winning and update _player_turn
        :return: Function does not return anything
        """
        # check if player won the game
        player = self.get_player_from_name(self.get_turn())
        if player.get_player_name() == 1 and player.get_pawn()[1] == 8:
            self._player_turn = None
            self._winner = player.get_player_name()
        elif player.get_player_name() == 2 and player.get_pawn()[1] == 0:
            self._player_turn = None
            self._winner = player.get_player_name()

        # if non of the players moves were winning update turn to next player
        else:
            if player.get_player_name() == 1:
                self._player_turn = 2
                return
            else:
                self._player_turn = 1

    # Below are the helper functions responsible for validating a move

    def ortho_adjacent(self, coord):
        """
        Function to generate a list of orthogonally adjacent coordinates to a given coordinate.
        :param coord:
        :return: List of orthogonally adjacent coordinates
        """
        list_of_adj_coordinates = list()
        if 0 <= coord[1] + 1 <= 8:
            list_of_adj_coordinates.append((coord[0], coord[1] + 1))
        if 0 <= coord[1] - 1 <= 8:
            list_of_adj_coordinates.append((coord[0], coord[1] - 1))
        if 0 <= coord[0] - 1 <= 8:
            list_of_adj_coordinates.append((coord[0] - 1, coord[1]))
        if 0 <= coord[0] + 1 <= 8:
            list_of_adj_coordinates.append((coord[0] + 1, coord[1]))
        return list_of_adj_coordinates

    def fence_between_coord(self, start_coord, target_coord):
        """
        Function to check if there is a fence between two give coordinates when pawn moves orthogonally.
        :param start_coord: coordinate from which we are trying to make a move
        :param target_coord: coordinate to which we are trying to land
        :return: True if there is a fence between coordinates,False otherwise
        """
        temp_coord = ()  # Potential fence coordinate
        for i in range(len(start_coord)):
            if start_coord[i] >= target_coord[i]:
                temp_coord += (start_coord[i],)
            elif start_coord[i] <= target_coord[i]:
                temp_coord += (target_coord[i],)
        if abs(start_coord[0] - target_coord[0]) == 1:
            orientation = "v"
        else:
            orientation = "h"
        # Check if fence coordinate and orientation exists on the board
        if temp_coord in self.get_board_fence_coord():
            if orientation in [o.get_orientation() for o in self.get_fence_from_coord(temp_coord)]:
                return True
            else:
                return False
        return False

    def initial_move_check(self, move_name, player_name, coordinate, orientation):
        """
        Function to check basic move requirements, such as check if game has been already won, if correct player is
        trying to make a turn, and if target move location is on the board
        :param move_name: move name - "move_pawn" or "place_fence"
        :param player_name: player name who is trying to make a move
        :param coordinate: fence or pawn coordinate
        :param orientation: orientation of the proposed fence move
        :return: True/False
        """
        if self.get_turn() is None:  # Check if game has been won
            return False
        if self.get_turn() != player_name:  # Check if correct player is making a turn
            return False
        # Check if coordinate is within board boundary
        if 0 <= coordinate[0] <= 8 and 0 <= coordinate[1] <= 8:
            if move_name == "move_pawn":
                # If it's a pawn move check if proposed move coordinate not the same as playing pawn coordinate
                # or occupied by opposing player
                if coordinate == self._p1.get_pawn() or coordinate == self._p2.get_pawn():
                    return False
            elif move_name == "place_fence":
                # If fence move check if proposed fence coordinate and orientation do not exist on the board yet
                if coordinate in self.get_board_fence_coord():
                    for f_obj in self.get_fence_from_coord(coordinate):
                        if orientation == f_obj.get_orientation():
                            return False
            else:
                return False
        else:
            return False
        return True

    def fair_play(self, player_name):
        """
        Helper function that checks if opponent pawn is locked up around fences,
        and therefore pawn cannot advance to a winning square.
        :return:"breaks the fair play rule"
        """
        visited_coord = list()
        if player_name == 1:
            opposing_pawn = self._p2
        else:
            opposing_pawn = self._p1
        return self.rec_faiplay(opposing_pawn.get_pawn(), opposing_pawn.get_player_name(), visited_coord)

    def rec_faiplay(self, coordinate, player_name, visited_coord_list):
        """
        Recursive fairplay function that iterates through possible moves to determine
        if opposing pawn can make a winning move
        :param coordinate:
        :param player_name:
        :param visited_coord_list:
        :return:
        """
        result = False
        visited_coord_list.append(coordinate)
        # Generate a list of possible orthogonal moves
        list_coord = self.ortho_adjacent(coordinate)
        # Iterate through the list of possible orthogonal moves
        for square in list_coord:
            # check if coordinate in the list of possible moves was previously visited
            if square not in visited_coord_list:
                # if coordinate was not visited yet, check if there is a fence in between two coordinates
                # to determing validity of a move
                if self.fence_between_coord(coordinate, square) is False:
                    # check if coordinate is a winning
                    if player_name == 1 and square[1] == 8:
                        return True
                    elif player_name == 2 and square[1] == 0:
                        return True
                    result = self.rec_faiplay(square, player_name, visited_coord_list)
            if result is True:
                return result
        return result

    def move_direction(self, pawn_coord, target_coord):
        """Function to determine the direction of the move"""
        x_direction = target_coord[0] - pawn_coord[0]
        y_direction = target_coord[1] - pawn_coord[1]
        coordinate = (x_direction, y_direction)
        return coordinate

gs = QuoridorGame()
#print(gs.get_board())
#print(gs.get_player_from_name(1))
# 1 h (6, 5)
#print(gs.place_fence(1, "h", (6, 5)))