from Game import *
import copy


class TicTacToe(Game):
    def __init__(self, number_of_players):
        self.game_name = "TicTacToe"
        self.board_size = 3

        self.number_of_players = number_of_players
        self.starting_player = 0

        self.empty_field_num = -1

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
            for i in range(rotation):
                temp = self.board[0][0]
                self.board[0][0] = self.board[2][0]
                self.board[2][0] = self.board[2][2]
                self.board[2][2] = self.board[0][2]
                self.board[0][2] = temp

                temp = self.board[0][1]
                self.board[0][1] = self.board[1][0]
                self.board[1][0] = self.board[2][1]
                self.board[2][1] = self.board[1][2]
                self.board[1][2] = temp

        def mirror(self, reflection):
            # Same state
            if reflection == 0:
                return
            # Mirror on the y-axis
            if reflection == 1:
                for row in range(self.game.board_size):
                    temp = self.board[row][0]
                    self.board[row][0] = self.board[row][2]
                    self.board[row][2] = temp

            # Mirror on the diagonal axis
            if reflection == 2:
                temp = self.board[1][0]
                self.board[1][0] = self.board[0][1]
                self.board[0][1] = temp
                temp = self.board[2][0]
                self.board[2][0] = self.board[0][2]
                self.board[0][2] = temp
                temp = self.board[1][2]
                self.board[1][2] = self.board[2][1]
                self.board[2][1] = temp

        def invert(self, invert):
            for i in range(invert):

                # Invert the player turn
                self.player_turn = self.game.get_successor_player_turn(self.player_turn)
                self.winning_status = States.invert(self.winning_status)

                # Invert the board
                for row in range(self.game.board_size):
                    for column in range(self.game.board_size):
                        if self.board[row][column] != self.game.empty_field_num:
                            self.board[row][column] = self.game.get_successor_player_turn(self.board[row][column])

        def get_canonical_successor_states(self):
            if len(self.successor_states) > 0:
                return self.successor_states

            # If the game has ended, then no successor states exist
            if self.winning_status != States.UNKNOWN:
                return self.successor_states

            successor_states_local = []

            for row in range(self.game.board_size):
                for column in range(self.game.board_size):
                    # Check if the field is empty
                    if (self.board[row][column] == self.game.empty_field_num):
                        successor = self.copy()

                        # Calculate the successor state
                        successor.board[row][column] = successor.player_turn
                        successor.player_turn = self.game.get_successor_player_turn(successor.player_turn)
                        successor.number_of_half_moves = self.number_of_half_moves + 1

                        # successor.reachable = self.winning_status == None #TODO Check all previous states
                        # if successor.reachable:

                        successor = successor.get_canonical_state()
                        successor.winning_status = successor.get_winning_status()

                        if not successor in successor_states_local:
                            successor_states_local.append(successor)

            return successor_states_local

        def get_canonical_state(self):
            all_equivalent_states = []

            # Get all rotations
            for rotation in range(4):
                equivalent_state = self.copy()
                equivalent_state.rotate(rotation)

                # Get all reflections
                for reflections in range(3):
                    equivalent_state = equivalent_state.copy()
                    equivalent_state.mirror(reflections)

                    # Get all inversions (only 1 inversion exists)
                    for invert in range(2):
                        equivalent_state = equivalent_state.copy()
                        equivalent_state.invert(invert)
                        all_equivalent_states.append(equivalent_state)

            # Sort all equivalent_states to get the canonical state
            all_equivalent_states.sort()

            # print("Equivalent states:")
            # for s in all_equivalent_states:
            #    s.print_state()
            # print(len(all_equivalent_states))
            #all_equivalent_states[0].player_turn

            return all_equivalent_states[0]

        def get_winning_status(self):
            state_copy = self.copy()

            for i in range(2):
                # Rows
                for row in range(state_copy.game.board_size):
                    if state_copy.board[row][0] != state_copy.game.empty_field_num and \
                            state_copy.board[row][0] == state_copy.board[row][1] and \
                            state_copy.board[row][1] == state_copy.board[row][2]:
                        if state_copy.board[row][0] == state_copy.player_turn:
                            return States.WON
                        else:
                            return States.LOOSE

                # Diagonal
                if state_copy.board[0][0] != state_copy.game.empty_field_num and \
                        state_copy.board[0][0] == state_copy.board[1][1] and \
                        state_copy.board[1][1] == state_copy.board[2][2]:
                    if state_copy.board[0][0] == state_copy.player_turn:
                        return States.WON
                    else:
                        return States.LOOSE

                state_copy.rotate(1)

            # Draw
            empty_fields_exist = False
            for row in range(state_copy.game.board_size):
                for column in range(state_copy.game.board_size):
                    if state_copy.board[row][column] == state_copy.game.empty_field_num:
                        empty_fields_exist = True
                        break

            if not empty_fields_exist:
                return States.DRAW

            # State is none of the Endstates where the game stops
            return States.UNKNOWN

        def __lt__(self, other):
            lhs_copy = self.copy()
            rhs_copy = other.copy()

            # Normalize the list so that the sorting is easier
            if lhs_copy.player_turn != 0:
                lhs_copy.invert(self.game.number_of_players - lhs_copy.player_turn)
            if rhs_copy.player_turn != 0:
                rhs_copy.invert(self.game.number_of_players - rhs_copy.player_turn)

            assert (lhs_copy.player_turn == 0)
            assert (rhs_copy.player_turn == 0)

            # First sort by the gameboard
            # Then by the player turn
            if lhs_copy.board == rhs_copy.board:
                return self.player_turn < other.player_turn
            else:
                return lhs_copy.board < rhs_copy.board

        def __eq__(self, other):
            return self.player_turn == other.player_turn and self.board == other.board

        def copy(self):
            result = copy.deepcopy(self)
            result.successor_states = []
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
