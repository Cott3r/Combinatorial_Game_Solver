from Game import *
import copy




class HeyDontgetAngry(Game):
    def __init__(self, number_of_players):
        self.game_name = "Hey, Don't Get Angry"

        self.number_of_players = number_of_players
        self.starting_player = 0

        self.empty_field_num = -1


class Board:

    class Player:
        def __init__(self, number_of_pawns_at_start):
            self.number_of_pawns_at_start = number_of_pawns_at_start
            self.finish_fields = [None] * 4
    def __init__(self, game: HeyDontgetAngry):
        self.game = game
        self.path = [None] * 40
        self.players = [self.Player(0)] * self.game.number_of_players

def get_successor_player_turn(self, player):
    return ((player + 1) % self.number_of_players)



class TTT_GameState(GameState):
    def __init__(self, game, board, player_turn):
        super().__init__(player_turn)

        self.game = game
        self.board = board

    def print_state(self):
        print(f"Move: {self.number_of_half_moves} \tTurn of Player: {self.player_turn} \tReachable: {self.reachable} \tWinner: {self.winning_status} in {self.end_in_number_of_turns}")
        for row in self.board:
            print(row)

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

def get_starting_states(self):
    starting_states = []
    new_state = self.TTT_GameState(self,
                                  [[self.empty_field_num, self.empty_field_num, self.empty_field_num],
                                   [self.empty_field_num, self.empty_field_num, self.empty_field_num],
                                   [self.empty_field_num, self.empty_field_num, self.empty_field_num]],
                                  self.starting_player)
    starting_states.append(new_state.get_canonical_state())



    return starting_states
