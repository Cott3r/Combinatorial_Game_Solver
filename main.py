# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import copy



class Game:
    game_name = "Name of the game"

    def __init__(self):
        pass

    def __str__(self):
        return self.game_name


class TicTacToe(Game):
    def __init__(self, number_of_players):
        self.game_name = "TicTacToe"
        self.board_size = 3

        self.number_of_players = number_of_players
        self.starting_player = 0

        self.empty_field_num = -1


    def get_successor_player_turn(self, player):
        return (player + 1) % self.number_of_players


    class GameState:
        def __init__(self, game, board, player_turn):
            self.game = game
            self.board = board

            self.player_turn = player_turn
            self.number_of_half_moves = 0
            self.reachable = True
            self.winning_status = None

        def print_state(self):
            print(f"Move: {self.number_of_half_moves} \tTurn of Player: {self.player_turn} \tReachable: {self.reachable} \tWinner: {self.winning_status}")
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
            #Same state
            if reflection == 0:
                return
            #Mirror on the y axis
            if reflection == 1:
                for row in range(self.game.board_size):
                    temp = self.board[row][0]
                    self.board[row][0] = self.board[row][2]
                    self.board[row][2] = temp


            #Mirror on the diagonal axis
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

                #Invert the player turn
                self.player_turn = self.game.get_successor_player_turn(self.player_turn)

                #Invert the board
                for row in range(self.game.board_size):
                    for column in range(self.game.board_size):
                        if self.board[row][column] != self.game.empty_field_num:
                            self.board[row][column] = self.game.get_successor_player_turn(self.board[row][column])

        def get_successor_states(self):
            self.successor_states = []

            #If the game has ended, then no successor states exist
            if self.winning_status != None:
                return self.successor_states

            for row in range(self.game.board_size):
                for column in range(self.game.board_size):
                    #Check if the field is empty
                    if(self.board[row][column] == self.game.empty_field_num):
                        successor = copy.deepcopy(self)

                        #Calculate the successor state
                        successor.board[row][column] = successor.player_turn
                        successor.player_turn = self.game.get_successor_player_turn(successor.player_turn)

                        successor.number_of_half_moves = self.number_of_half_moves + 1
                        successor.reachable = self.winning_status == None #TODO Check all previous states
                        if successor.reachable:
                            successor.winning_status = successor.get_winning_status()

                        self.successor_states.append(successor)


            return self.successor_states

        def get_canonical_state(self):
            all_equivalent_states = []

            #Get all rotations
            for rotation in range(4):
                equivalent_state = copy.deepcopy(self)
                equivalent_state.rotate(rotation)

                #Get all reflections
                for reflections in range(3):
                    equivalent_state = copy.deepcopy(equivalent_state)
                    equivalent_state.mirror(reflections)

                    #Get all inversions (only 1 inversion exists)
                    for invert in range(2):
                        equivalent_state = copy.deepcopy(equivalent_state)
                        equivalent_state.invert(invert)
                        all_equivalent_states.append(equivalent_state)



            #Sort all equivalent_states to get the canonical state
            all_equivalent_states.sort()

            #print("Equivalent states:")
            #for s in all_equivalent_states:
            #    s.print_state()
            #print(len(all_equivalent_states))

            return all_equivalent_states[0]

        def get_winning_status(self):
            empty_fields_exist = False
            state_copy = copy.deepcopy(self)

            for row in range(state_copy.game.board_size):
                for column in range(state_copy.game.board_size):
                    if state_copy.board[row][column] == state_copy.game.empty_field_num:
                        empty_fields_exist = True
                        break

            for i in range(2):
                #Rows
                for row in range(state_copy.game.board_size):
                    if state_copy.board[row][0] != state_copy.game.empty_field_num and \
                        state_copy.board[row][0] == state_copy.board[row][1] and \
                        state_copy.board[row][1] == state_copy.board[row][2]:
                        return state_copy.board[row][0]

                #Diagonal
                if state_copy.board[0][0] != state_copy.game.empty_field_num and \
                    state_copy.board[0][0] == state_copy.board[1][1] and \
                    state_copy.board[1][1] == state_copy.board[2][2]:
                    return state_copy.board[0][0]

                state_copy.rotate(1)

            #Draw
            if not empty_fields_exist:
                return -1

            return None

        def __lt__(self, other):
            lhs_copy = copy.deepcopy(self)
            rhs_copy = copy.deepcopy(other)

            #Normalize the list so that the sorting is easier
            if lhs_copy.player_turn != 0:
                lhs_copy.invert(self.game.number_of_players - lhs_copy.player_turn)
            if rhs_copy.player_turn != 0:
                rhs_copy.invert(self.game.number_of_players - rhs_copy.player_turn)

            assert (lhs_copy.player_turn == 0)
            assert(rhs_copy.player_turn == 0)

            #First sort by the gameboard
            #Then by the player turn
            if lhs_copy.board == rhs_copy.board:
                return self.player_turn < other.player_turn
            else:
                return lhs_copy.board < rhs_copy.board

        def __eq__(self, other):
            return self.player_turn == other.player_turn and self.board == other.board

    def get_starting_states(self):
        starting_states = []
        starting_states.append(self.GameState(self, [[self.empty_field_num, self.empty_field_num, self.empty_field_num], [self.empty_field_num, self.empty_field_num, self.empty_field_num], [self.empty_field_num, self.empty_field_num, self.empty_field_num]], self.starting_player))
        return starting_states


class GameStates:
    def __init__(self, game):
        self.game = game
        self.all_possible_states = None

    def enumerate_all_state(self):
        processed_states = []
        non_processed_states = []
        final_states = []

        #Add all initial states to the non_processed_states
        for starting_state in self.game.get_starting_states():
            non_processed_states.append(starting_state.get_canonical_state())




        # For every non-processed states, prossess it:
        #Run until we have no longer any states to be processed
        while len(non_processed_states) > 0:
            new_non_processed_states = []

            # Find every canonical successor states and add them to be processed
            print(f"number of half moves: {non_processed_states[0].number_of_half_moves}")
            print(f"processing {len(non_processed_states)} states")
            for s in non_processed_states:

                has_successor_state = False
                for successor_state in s.get_successor_states():
                    has_successor_state = True
                    canonical_state = successor_state.get_canonical_state()

                    #If the canonical_state is already in the new_non_processed_states, then we dont need to add it again
                    if canonical_state not in new_non_processed_states:
                        #If the canonical_state is already in the processed_states, then we need to do nothing
                        if canonical_state not in processed_states:
                            #If the canonical_state is already in the non_processed_states, then we also need to do nothing
                            if canonical_state not in non_processed_states:
                                new_non_processed_states.append(canonical_state)

                if not has_successor_state:
                    final_states.append(s)

            processed_states.extend(non_processed_states)
            non_processed_states = new_non_processed_states


            #print(f"found {len(new_non_processed_states)} new states")
            print("\n")


        self.all_possible_states = processed_states
        #for state in processed_states:
        #    if state.reachable == False:
        #        state.print_state()

        print("Number of processed states:", len(processed_states))

    #Calculate the code of how many moves till win, loss, draw or kingmaker
    def calculate_codes(self):
        pass


if __name__ == '__main__':

    tictactoe_3_players = TicTacToe(2)

    game_states = GameStates(tictactoe_3_players)
    game_states.enumerate_all_state()
    game_states.calculate_codes()