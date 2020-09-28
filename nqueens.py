import random


def gen_board(n, static_x, static_y):
    board = []
    for i in range(n):
        if i == static_x:
            board.append(static_y)
            continue
        rand_y = random.randint(0, n)
        board.append(rand_y)
    return board


def succ(state, static_x, static_y):
    """
    Return list of successor states given the static point
    :param state: Parent state
    :param static_x: x coord of static point
    :param static_y: y coord of static point
    :return: list of successors
    """
    succ_list = []
    n = len(state)
    # Check static point
    if state[static_x] != static_y:
        return succ_list
    for i in range(n):
        state_cp = state.copy()
        x = i
        if x == static_x:
            continue
        y = state_cp[x]
        if y == 0:
            state_cp[x] = y+1
            succ_list.append(state_cp)
            continue
        elif y == n-1:
            state_cp[x] = y-1
            succ_list.append(state_cp)
            continue
        else:
            state_cp[x] = y+1
            succ_list.append(state_cp)
            state_cp = state.copy()
            state_cp[x] = y-1
            succ_list.append(state_cp)
    return sorted(succ_list)


def f(state):
    """
    For each queen on the board, increment score whenever another queen
    is in the same row or diagonal as current queen
    :param state: Positions of the queens
    :return: score
    """
    score = 0
    for q in range(len(state)):
        for i in range(len(state)):
            x_distance = abs(q - i)
            y_distance = abs(state[q] - state[i])
            if x_distance == 0:
                # Do nothing; it's the same queen
                continue
            if y_distance == 0 or x_distance == y_distance:  # Same row/diagonal
                score += 1
                break
    return score


def choose_next(curr, static_x, static_y):
    if curr[static_x] != static_y:
        return None
    succ_list = succ(curr, static_x, static_y)
    succ_list.append(curr)
    scores = []
    for i, suc in enumerate(succ_list):
        scores.append((f(suc), suc))
    scores_ord = sorted(scores)
    return scores_ord[0][1]


def n_queens(initial_state, static_x, static_y, print_path=True):
    state = initial_state
    new_f = f(initial_state)
    old_f = -1
    while new_f != 0:
        if print_path:
            print("{} - f={}".format(state, new_f))
        state = choose_next(state, static_x, static_y)
        old_f = new_f
        new_f = f(state)
        if new_f == old_f:
            break
    if print_path:
        print("{} - f={}".format(state, new_f))
    return state


def n_queens_restart(n, k, static_x, static_y):
    random.seed(1)
    best_sols = []
    for i in range(k):
        # Generate a valid initial board
        state = gen_board(n, static_x, static_y)
        result = n_queens(state, static_x, static_y, print_path=False)
        res_score = f(result)
        if res_score == 0:
            print("{} - f={}".format(result, res_score))
            return
        if not best_sols or res_score < best_sols[0][1]:
            best_sols = [(result, res_score)]
        elif res_score == best_sols[0][1]:
            best_sols.append((result, res_score))
    # Print best solutions
    for i, sol in enumerate(best_sols):
        print("{} - f={}".format(best_sols[i][0], best_sols[i][1]))


def main():
    n_queens(6, 10, 0, 0)


if __name__ == '__main__':
    main()
