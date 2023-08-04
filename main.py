# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import copy
import Game
import TicTacToe
import HeyDontgetAngry
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
                                        break
                        else:
                            for possible_successor in processed_states:
                                if possible_successor == successor_state:
                                    s.successor_states.append(possible_successor)
                                    break
                    else:
                        for possible_successor in new_non_processed_states:
                            if possible_successor == successor_state:
                                s.successor_states.append(possible_successor)
                                break

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
        # print(state.end_in_number_of_turns, end= " ")
        #
        # if len(state.successor_states) == 0:
        #     print()

        for successor_state in state.successor_states:
            if successor_state.winning_status == States.DRAW:
                self.print_all_states(successor_state)


    def print_gamestate_number_tree(self):
        already_found_states = self.starting_states
        next_states = self.starting_states

        layer_number = 0

        while len(next_states) > 0:

            number_of_gamestates = 0
            next_layer_states = []

            for state in next_states:
                number_of_gamestates += 1

                for successor_state in state.successor_states:
                    if successor_state not in next_layer_states:
                        if successor_state not in already_found_states:
                            next_layer_states.append(successor_state)


            print(f"Layer: {layer_number}  Number of Gamestates: {number_of_gamestates}")


            #Go on to next layer
            next_states = next_layer_states
            already_found_states.extend(next_layer_states)
            layer_number += 1

    def print_best_path(self, state):
        state.print_state()

        #Get the best first option
        for canonical_successor_state in state.successor_states:
            if canonical_successor_state.winning_status == state.winning_status:

                #self.print_best_path(canonical_successor_state)
                self.print_best_path(state.get_uncanonical_successor_state(canonical_successor_state))
                break


if __name__ == '__main__':
    #game = TicTacToe.TicTacToe(3)
    game = HeyDontgetAngry.HeyDontgetAngry(3)
    game.test()

    exit(1)
    game_states = GameStates(game)
    game_states.enumerate_all_state()
    game_states.calculate_codes()

    game_states.print_best_path(game_states.starting_states[0])
    game_states.print_gamestate_number_tree()
