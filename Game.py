from enum import Enum
import copy


class Game:
    game_name = "Name of the game"

    def __init__(self):
        pass

    def __str__(self):
        return self.game_name


class States(Enum):
    UNKNOWN = 0
    WON = 1
    LOOSE = 2
    DRAW = 3
    KINGMAKER = 4

    @classmethod
    def invert(cls, winning_status):
        if winning_status == States.WON:
            return States.LOOSE
        elif winning_status == States.LOOSE:
            return States.WON
        elif winning_status == States.KINGMAKER:
            assert(False) #TODO
        else:
            return winning_status


class GameState():

    def __init__(self, player_turn, status=States.UNKNOWN):
        self.number_of_half_moves = 0
        self.winning_status = States.UNKNOWN
        self.end_in_number_of_turns = 0
        self.player_turn = player_turn
        self.successor_states = []

        self.kingmaker_options = []
        self.reachable = True

    def copy(self):
        result = copy.deepcopy(self)
        result.successor_states = []
        return result