from Game import *




class HeyDontgetAngry(Game):
    def __init__(self, number_of_players):
        self.game_name = "Hey, Don't Get Angry"

        self.number_of_players = number_of_players
        self.starting_player = 0

        self.empty_field_num = -1

    def test(self):
        starting_states = self.get_starting_states()

        for s in starting_states:
            #s.board.path[0] = -1
            #s.board.path[8] = 0

            s.print_state()

            print(s.get_winning_status())

            for successor_states in s.get_canonical_successor_states():
                successor_states.print_state()


    def get_starting_states(self):
        starting_states = []

        board = Board(self)
        #Set one pawn to the starting spot
        for player_number in range(self.number_of_players):
            board.path[player_number * 10] = player_number
        new_state = HDGA_GameState(self, board, 0)
        starting_states.append(new_state.get_canonical_state())

        return starting_states


    def get_successor_player_turn(self, player):
        return ((player + 1) % self.number_of_players)


class Board:

    class Player:
        def __init__(self, player_number, number_of_pawns_at_start):
            self.player_number = player_number
            self.start_index = player_number * 10
            self.finish_index = (self.start_index - 1) % 40
            self.number_of_pawns_at_start = number_of_pawns_at_start
            self.finish_fields = [-1] * 4

        def __eq__(self, other):
            return self.player_number == other.player_number and \
                self.number_of_pawns_at_start == other.number_of_pawns_at_start and \
                self.finish_fields == other.finish_fields

    def __init__(self, game: HeyDontgetAngry):
        self.game = game
        self.path = [self.game.empty_field_num] * 40

        self.players = []
        for i in range(self.game.number_of_players):
            self.players.append(self.Player(i, 3))

    def __eq__(self, other):
        return self.path == other.path and \
            self.players == other.players


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


    def get_canonical_successor_states(self):
        if len(self.successor_states) > 0:
            return self.successor_states

        # If the game has ended, then no successor states exist
        if self.winning_status != States.UNKNOWN:
            return self.successor_states

        successor_states_local = []
        player = self.board.players[self.player_turn]

        #All possible dice falls
        for dice_number in range(1, 7):
            if dice_number >= 2 and dice_number <= 5:
                continue

            #Start a new pawn
            if dice_number == 6 and player.number_of_pawns_at_start > 0 and self.board.path[player.start_index] != player.player_number:
                successor = self.copy()

                #Capture other pawns
                if self.board.path[player.start_index] != self.game.empty_field_num:
                    successor.board.players[self.board.path[player.start_index]].number_of_pawns_at_start += 1

                successor.board.players[self.player_turn].number_of_pawns_at_start -= 1
                successor.board.path[successor.board.players[self.player_turn].start_index] = self.player_turn
                successor.player_turn = self.game.get_successor_player_turn(successor.player_turn)
                successor.number_of_half_moves = self.number_of_half_moves + 1
                successor = successor.get_canonical_state()
                #successor.winning_status = successor.get_winning_status()

                if not successor in successor_states_local:
                    successor_states_local.append(successor)



            #For all the pawns on the path
            for index_on_path in range(40):
                if self.board.path[index_on_path] == self.player_turn:
                    successor = self.copy()

                    #Pick up pawn
                    successor.board.path[index_on_path] = self.game.empty_field_num

                    new_index = (index_on_path + dice_number) % 40


                    #Check if we can move to finish
                    finish_index = (new_index - player.finish_index) % 40 - 1
                    if index_on_path < player.finish_index and index_on_path >= player.finish_index - 6 and \
                            0 <= finish_index and finish_index < 4 and \
                            player.finish_fields[finish_index] == self.game.empty_field_num:
                        other_successor = successor.copy()
                        other_successor.board.players[self.player_turn].finish_fields[finish_index] = self.player_turn

                        other_successor.player_turn = self.game.get_successor_player_turn(other_successor.player_turn)
                        successor.number_of_half_moves = self.number_of_half_moves + 1
                        other_successor = other_successor.get_canonical_state()
                        #other_successor.winning_status = other_successor.get_winning_status()

                        if not other_successor in successor_states_local:
                            successor_states_local.append(other_successor)




                    #Are we passing a start field with a pawn on it
                    cannot_move_past_blocked_start = False
                    for blocking_player in self.board.players:
                        if self.board.path[blocking_player.start_index] == blocking_player.player_number:
                            blocking_index = blocking_player.start_index

                            if index_on_path < blocking_index and blocking_index <= new_index:
                                cannot_move_past_blocked_start = True
                            if blocking_index == 0 and index_on_path > 34 and new_index < 5:
                                cannot_move_past_blocked_start = True
                    if cannot_move_past_blocked_start:
                        continue


                    #Cannot move onto own pawn
                    if self.board.path[new_index] == self.player_turn:
                        continue

                    #Capture other pawns
                    if successor.board.path[new_index] != self.game.empty_field_num:
                        successor.board.players[successor.board.path[new_index]].number_of_pawns_at_start += 1

                    #Move to new field
                    successor.board.path[new_index] = self.player_turn

                    successor.player_turn = self.game.get_successor_player_turn(successor.player_turn)
                    successor.number_of_half_moves = self.number_of_half_moves + 1
                    successor = successor.get_canonical_state()
                    #successor.winning_status = successor.get_winning_status()

                    if not successor in successor_states_local:
                        successor_states_local.append(successor)

        return successor_states_local

    def get_canonical_state(self, print_all_info=False):
        return self

    def get_uncanonical_successor_state(self, canonical_successor_goal):
        return canonical_successor_goal

    def get_winning_status(self):
        #Check if current player has won
        if self.board.players[self.player_turn].finish_fields == [self.board.players[self.player_turn].player_number] * 4:
            return States.WON

        #Check if other players have won
        for player in self.board.players:
            if player.finish_fields == [player.player_number] * 4:
                return States.LOOSE

        # State is none of the Endstates where the game stops
        return States.UNKNOWN

    def __lt__(self, other):
        pass

    def __eq__(self, other):
        return self.player_turn == other.player_turn and self.board == other.board



