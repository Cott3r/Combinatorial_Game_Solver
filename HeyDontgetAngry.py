from Game import *
import copy




class HeyDontgetAngry(Game):
    def __init__(self, number_of_players):
        self.game_name = "Hey, Don't Get Angry"

        self.number_of_players = number_of_players
        self.starting_player = 0

        self.empty_field_num = -1

    def test(self):
        starting_states = self.get_starting_states()

        for s in starting_states:
            s.print_state()


    def get_starting_states(self):
        starting_states = []

        board = Board(self)
        #Set one pawn to the starting spot
        for player_number in range(self.number_of_players):
            board.path[player_number * 10] = player_number
            board.players[player_number].number_of_pawns_at_start = player_number
        new_state = HDGA_GameState(self, board, 0)
        #starting_states.append(new_state.get_canonical_state())
        starting_states.append(new_state)

        return starting_states


class Board:

    class Player:
        def __init__(self, number_of_pawns_at_start):
            self.number_of_pawns_at_start = number_of_pawns_at_start
            self.finish_fields = [-1] * 4
    def __init__(self, game: HeyDontgetAngry):
        self.game = game
        self.path = [self.game.empty_field_num] * 40

        self.players = []
        for i in range(self.game.number_of_players):
            self.players.append(self.Player(0))

def get_successor_player_turn(self, player):
    return ((player + 1) % self.number_of_players)



class HDGA_GameState(GameState):
    def __init__(self, game: HeyDontgetAngry, board, player_turn):
        super().__init__(player_turn)

        self.game = game
        self.board = board

    def print_state(self):
        print(f"Move: {self.number_of_half_moves} \tTurn of Player: {self.player_turn} \tReachable: {self.reachable} \tWinner: {self.winning_status} in {self.end_in_number_of_turns}")

        for row in range(11):
            for column in range(11):
                index = None
                empty = True

                #Path
                if column == 4 and row >= 6:
                    index = 10 - row
                elif row == 6 and column < 4:
                    index = 3 - column + 5
                elif row == 5 and column == 0:
                    index = 9
                elif row == 4 and column < 4:
                    index = column + 10
                elif column == 4 and row <= 4:
                    index = 4 - row + 14
                elif row == 0 and column == 5:
                    index = 19
                elif column == 6 and row <= 4:
                    index = row + 20
                elif row == 4 and column > 6:
                    index = column + 18
                elif row == 5 and column == 10:
                    index = 29
                elif row == 6 and column > 6:
                    index = 10 - column + 30
                elif column == 6 and row >= 6:
                    index = row + 28
                elif row == 10 and column == 5:
                    index = 39

                if index != None:
                    empty = False
                    if self.board.path[index] == self.game.empty_field_num:
                        if index % 10 == 0:
                            print("== ", end='')
                        else:
                            print("-- ", end='')
                    else:
                        print("{:2d} ".format(self.board.path[index]), end='')



                #Starting Spots
                if row == 10 and column == 2 and self.game.number_of_players >= 1:
                    empty = False
                    print(" {:1d}:".format(self.board.players[0].number_of_pawns_at_start), end='')
                elif row == 2 and column == 0 and self.game.number_of_players >= 2:
                    empty = False
                    print(" {:1d}:".format(self.board.players[1].number_of_pawns_at_start), end='')
                elif row == 0 and column == 8 and self.game.number_of_players >= 3:
                    empty = False
                    print(":{:1d} ".format(self.board.players[2].number_of_pawns_at_start), end='')
                elif row == 8 and column == 10 and self.game.number_of_players >= 4:
                    empty = False
                    print(":{:1d} ".format(self.board.players[3].number_of_pawns_at_start), end='')


                #Finish fields
                finish_field = None
                if row >= 6 and row < 10 and column == 5 and self.game.number_of_players >= 1:
                    finish_field = self.board.players[0].finish_fields[9 - row]
                elif row == 5 and column <= 4 and column >= 1 and self.game.number_of_players >= 2:
                    finish_field = self.board.players[1].finish_fields[column-1]
                elif row <= 4 and row > 0 and column == 5 and self.game.number_of_players >= 3:
                    finish_field = self.board.players[2].finish_fields[row - 1]
                elif row == 5 and column >= 6 and column < 10 and self.game.number_of_players >= 4:
                    finish_field = self.board.players[3].finish_fields[9 - column]

                if finish_field != None:
                    empty = False
                    if finish_field == self.game.empty_field_num:
                        print(" . ", end='')
                    else:
                        print("{:2d} ".format(finish_field), end='')



                #empty Field
                if empty:
                    print(f"   ", end='')

            print()

    def rotate(self, rotation):
        pass

    def mirror(self, reflection):
        pass

    def invert(self, invert):
        pass

    def get_canonical_successor_states(self):
        pass

    def get_canonical_state(self, print_all_info=False):
        pass

    def get_uncanonical_successor_state(self, canonical_successor_goal):
        pass

    def get_winning_status(self):
        pass

    def __lt__(self, other):
        pass

    def __eq__(self, other):
        return self.player_turn == other.player_turn and self.board == other.board

    def copy(self):
        result = copy.deepcopy(self)
        return result



