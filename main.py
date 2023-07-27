# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import copy
import Game
import TicTacToe
from Game import *

class GameStates:
    def __init__(self, game):
        self.game = game
        self.all_possible_states = None
        self.starting_states = []

    def enumerate_all_state(self):
        processed_states = []
        non_processed_states = []
        final_states = []

        #Add all initial states to the non_processed_states
        for starting_state in self.game.get_starting_states():
            non_processed_states.append(starting_state)
        self.starting_states.extend(non_processed_states)




        # For every non-processed states, prossess it:
        #Run until we have no longer any states to be processed
        while len(non_processed_states) > 0:
            new_non_processed_states = []

            # Find every canonical successor states and add them to be processed
            print(f"number of half moves: {non_processed_states[0].number_of_half_moves}")
            print(f"processing {len(non_processed_states)} states")
            for s in non_processed_states:

                has_successor_state = False
                for successor_state in s.get_canonical_successor_states():
                    has_successor_state = True


                    #If the successor_state is already in the new_non_processed_states, then we dont need to add it again
                    if successor_state not in new_non_processed_states:
                        #If the successor_state is already in the processed_states, then we need to do nothing
                        if successor_state not in processed_states:
                            #If the successor_state is already in the non_processed_states, then we also need to do nothing
                            if successor_state not in non_processed_states:
                                new_non_processed_states.append(successor_state)
                                s.successor_states.append(successor_state)
                            else:
                                for possible_successor in non_processed_states:
                                    if possible_successor == successor_state:
                                        s.successor_states.append(possible_successor)
                        else:
                            for possible_successor in processed_states:
                                if possible_successor == successor_state:
                                    s.successor_states.append(possible_successor)
                    else:
                        for possible_successor in new_non_processed_states:
                            if possible_successor == successor_state:
                                s.successor_states.append(possible_successor)

                if not has_successor_state:
                    final_states.append(s)

            processed_states.extend(non_processed_states)
            non_processed_states = new_non_processed_states



            print("\n")


        self.all_possible_states = processed_states
        #for state in final_states:
        #    state.print_state()
            #assert (not (state.number_of_half_moves < 9 and len(state.successor_states) == 0))

        print("Number of processed states:", len(processed_states))

    #Calculate the code of how many moves till win, loss, draw or kingmaker
    def calculate_codes(self):
        for starting_state in self.starting_states:
            self.set_best_winning_state(starting_state)
            starting_state.print_state()

    def set_best_winning_state(self, state):

        assert (state in self.all_possible_states)

        if state.winning_status != States.UNKNOWN:
            return state.winning_status

        winning_in = 10e10
        draw_in = 10e10
        loosing_in = 0

        for successor_state in state.successor_states:
            self.set_best_winning_state(successor_state)

            if successor_state.winning_status == States.LOOSE:
                if successor_state.end_in_number_of_turns + 1 < winning_in:
                    winning_in = successor_state.end_in_number_of_turns + 1
            elif successor_state.winning_status == States.DRAW:
                if successor_state.end_in_number_of_turns + 1 < draw_in:
                    draw_in = successor_state.end_in_number_of_turns + 1
            elif successor_state.winning_status == States.WON:
                if successor_state.end_in_number_of_turns + 1 > loosing_in:
                    loosing_in = successor_state.end_in_number_of_turns + 1

        if winning_in != 10e10:
            state.winning_status = States.WON
            state.end_in_number_of_turns = winning_in
        elif draw_in != 10e10:
            state.winning_status = States.DRAW
            state.end_in_number_of_turns = draw_in
        elif loosing_in != 0:
            state.winning_status = States.LOOSE
            state.end_in_number_of_turns = loosing_in

        assert(state.winning_status != States.UNKNOWN)

    def print_all_states(self, state):
        state.print_state()

        for successor_state in state.successor_states:
            self.print_all_states(successor_state)


if __name__ == '__main__':
    tictactoe_3_players = TicTacToe.TicTacToe(2)

    game_states = GameStates(tictactoe_3_players)
    game_states.enumerate_all_state()
    game_states.calculate_codes()

    print("What")
