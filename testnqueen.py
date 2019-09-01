"""
N-Queen problem using Hill Climbing Approach.
"""

# Python imports
import random
from statistics import mean

# Global variables
HILL_CLIMBING_VARIANT = "sideways-move"

'''

Four Options
1. steepest-ascent 
2. sideways-move
3. random-restart
4. random-restart-sideways

'''
class Node:
    def __init__(self, state, depth, h_value):
        """
        Initialising an object with state, depth and f(n) value
        """
        self.state = state
        self.depth = depth
        self.h_value = h_value

    def generate_child(self):
        """
        Find the blank tile location and generate child nodes based on the poss.
        """
        children = []
        for i in range(0, board_size):
            for j in range(0, board_size):
                if self.state[i][j] == 'Q':
                    x, y = i, j
                    moves_list = []
                    for moves in range(0, board_size):
                        if moves != y:
                            moves_list.append([x, moves])
                    for m in moves_list:
                        child = self.move_queen(self.state, x, y, m[0], m[1])
                        if child is not None:
                            child_node = Node(child, self.depth+1, 0)
                            children.append(child_node)
        return children

    def move_queen(self, current_state, x1, y1, x2, y2):
        """
        Move the blank space in the given direction and if the position value are out
        of limits the return None
        """
        temp_puz = []
        temp_puz = self.copy(current_state)
        temp = temp_puz[x2][y2]
        temp_puz[x2][y2] = temp_puz[x1][y1]
        temp_puz[x1][y1] = temp
        return temp_puz

    def copy(self, root):
        """
        Copy function to create a similar matrix of the given node
        """
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp


def generate_initial_state(board_size):
    """
    :param board_size: choose board size Eg: 4*4/8*8/16*16
    :return initial_state : 2d matrix of initail state
    """
    initial_state = [['-' for i in range(board_size)] for j in range(board_size)]
    for i in range(board_size):
        j = random.randint(0, board_size-1)
        initial_state[i][j] = 'Q'
    return initial_state


def find_heuristic(current_board, board_size):
    """
    :param current_board: Current board configurations of queens
    :return: heuristic cost of the board, number of pairs of queens attacking
    """
    h = 0
    for row in range(0, board_size):
        for column in range(0, board_size):
            # if the current element is a queen, calculate all violations
            if current_board[row][column] == 'Q':
                # Check this row on left side
                queen = 1
                while queen < board_size:
                    if column+queen < board_size and current_board[row][column+queen] == 'Q':
                        h += 1
                    if row+queen < board_size and current_board[row+queen][column] == 'Q':
                        h += 1
                    if row+queen < board_size and column+queen < board_size and \
                            current_board[row+queen][column+queen] == 'Q':
                        h += 1
                    if row-queen >= 0 and column+queen < board_size and current_board[row-queen][column+queen] == 'Q':
                        h += 1
                    queen += 1
    return h

def printArrow():
    print("")
    print("  | ")
    print("  | ")
    print(" \\\'/ \n")


if __name__ == "__main__":

    # board_size = 8
    total = 50
    file_name = str(total) +"withboard"+ ".txt"
    f1 = open(file_name, 'w')

    board_size = input("Enter Board Size : ")
    board_size = int(board_size)

    '''
    Get User Input for the Variant to be used.
    '''
    print("Different Variants:\n1. steepest-ascent\n2. sideways-move\n3. random-restart\n4. random-restart-sideways")
    HILL_CLIMBING_VARIANT = input("Enter the Variant(Name not Number) to be used: ")

    '''
    Verifying user input
    '''
    if HILL_CLIMBING_VARIANT in ["steepest-ascent", "sideways-move", "random-restart", "random-restart-sideways"]:
        pass
    else:
        print("Re-run the program and enter a proper variant from the list.")


    # for HILL_CLIMBING_VARIANT in ["steepest-ascent", "sideways-move", "random-restart", "random-restart-sideways"]:
    print("HILL CLIMBING VARIANT : ", HILL_CLIMBING_VARIANT, file=f1)
    success_count = 0
    failure_count = 0
    success_step_count = []
    failure_step_count = []
    restart_count_list = []
    print_number = 0
    for run in range(0, total):
        initial_board = generate_initial_state(board_size)

        restart_count = 0

        # To print 4 boards
        if print_number < 4:
            print("\n", file=f1)
            print("Initial state:", file=f1)
            for i in initial_board:
                    for j in i:
                        print(j, end=" ", file=f1)
                    print("", file=f1)
            print("\n", file=f1)

        print("Heuristic of Initial State: ", find_heuristic(initial_board, board_size))
        print("Value is", find_heuristic(initial_board, board_size))

        frontier = []
        explored = []

        sideways_move = 0

        initial_node = Node(initial_board, 0, 0)
        initial_node.h_value = find_heuristic(initial_board, board_size)

        frontier.append(initial_node)

        print("\n")

        while True:
            cur = frontier[0]
            printArrow()
            for i in cur.state:
                for j in i:
                    print(j, end=" ")
                print("")
            print("h = ", cur.h_value)
            if cur.h_value == 0:
                    success_count += 1
                    if print_number < 4:
                        print("Goal state!!! - ", run, file=f1)
                        for i in cur.state:
                            for j in i:
                                print(j, end=" ", file=f1)
                            print("", file=f1)
                        print(" \n", file=f1)
                        print("Number of steps - ", cur.depth, file=f1)
                        print("--------------------------------", file=f1)
                        print_number += 1
                    success_step_count.append(cur.depth)
                    if restart_count:
                        restart_count_list.append(restart_count)
                    break

            current_level = []
            children = cur.generate_child()
            for i in children:
                    i.h_value = find_heuristic(i.state, board_size)
                    if i.state not in frontier:
                        frontier.append(i)
                        current_level.append(i)

            frontier.pop(0)
            explored.append(cur)

            frontier.sort(key=lambda x: x.h_value, reverse=False)

            if frontier[0].h_value >= cur.h_value:
                """
                In Steepest Slop we stop the algorithm if the Previous Heuristic Value 
                is more than or Equal to current one.
                """
                if HILL_CLIMBING_VARIANT == "steepest-ascent":
                    if print_number < 4:
                        print("No Solution Found: ", run, file=f1)
                        print("--------------------------------", file=f1)
                        print_number += 1
                    failure_count += 1
                    failure_step_count.append(cur.depth)
                    break

                """
                In Random Restart if the Previous Heuristic is greater than or Equal to the 
                Current Heuristic Value then we restart the board till we get the solution.
                """
                if HILL_CLIMBING_VARIANT == "random-restart":
                    restart_count += 1
                    frontier = []
                    initial_board = generate_initial_state(board_size)
                    initial_node = Node(initial_board, 0, 0)
                    initial_node.h_value = find_heuristic(initial_board, board_size)
                    frontier.append(initial_node)
                """
                If the Previous Heuristic in the Frontier is equal to the current Heuristic then 
                we allow sideways moves, It picks up a node from the frontier to check if 
                it has a better heuristic value, If it finds a better heuristic in 100 iterations 
                it uses it to find the solution
                """
                if frontier[0].h_value == cur.h_value:
                    if HILL_CLIMBING_VARIANT == "sideways-move" or HILL_CLIMBING_VARIANT == "random-restart-sideways":
                        if frontier[0].h_value == cur.h_value:
                            rand_fr = []
                            for fr in frontier:
                                if fr.h_value == cur.h_value:
                                    rand_fr.append(fr)
                            r = random.choice(rand_fr)
                            index = frontier.index(r)
                            frontier[0], frontier[index] = frontier[index], frontier[0]
                            sideways_move += 1
                        if sideways_move > 100 or frontier[0].h_value > cur.h_value:
                            if HILL_CLIMBING_VARIANT == "random-restart-sideways":
                                restart_count += 1
                                frontier = []
                                initial_board = generate_initial_state(board_size)
                                initial_node = Node(initial_board, 0, 0)
                                initial_node.h_value = find_heuristic(initial_board, board_size)
                                frontier.append(initial_node)
                            else:
                                if print_number < 4:
                                    print("No solution found at sideways move - ", run, file=f1)
                                    print("--------------------------------", file=f1)
                                    print_number += 1
                                failure_count += 1
                                failure_step_count.append(cur.depth)
                                break
    print("==========================================================", file=f1)
    print("Success percentage", (success_count/total)*100, file=f1)
    print("Average number of steps in success", mean(success_step_count), file=f1)
    print("Failure percentage", (failure_count/total)*100, file=f1)
    if failure_count:
        print("Average number of steps in failure", mean(failure_step_count), file=f1)
    if HILL_CLIMBING_VARIANT == "random-restart-sideways" or HILL_CLIMBING_VARIANT == "random-restart":
        print("Average number of restarts", mean(restart_count_list), file=f1)
    print("==========================================================", file=f1)

    print("==========================================================")
    print("Success percentage", (success_count/total)*100)
    print("Average number of steps in success", mean(success_step_count))
    print("Failure percentage", (failure_count/total)*100)
    if failure_count:
        print("Average number of steps in failure", mean(failure_step_count))
    if HILL_CLIMBING_VARIANT == "random-restart-sideways" or HILL_CLIMBING_VARIANT == "random-restart":
        print("Average number of restarts", mean(restart_count_list))
    print("==========================================================")
